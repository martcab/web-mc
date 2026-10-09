#!/usr/bin/env python3
"""Publica la columna de Martín Cabrera como páginas estáticas.

Lee los textos de contenido/columnas/*.md y genera:
  - columnas/<slug>.html       una página por columna publicada
  - columnas/index.html        archivo de columnas, agrupado por año
  - feed.xml                   canal RSS para lectores y suscriptores
  - sitemap.xml, robots.txt    mapa del sitio e indicaciones para buscadores
  - index.html                 actualiza el bloque «En este sitio» de la portada

Solo usa la biblioteca estándar de Python 3. No hay base de datos ni servidor:
el resultado son archivos HTML que se suben a cualquier alojamiento estático.

Uso:
  python3 herramientas/publicar.py               publica las columnas con estado «publicado»
  python3 herramientas/publicar.py --borradores  además genera vistas previas de borradores
                                                 en columnas/_vista-previa/ (no se enlazan ni se indexan)
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import sys
from dataclasses import dataclass, field
from email.utils import format_datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / 'contenido' / 'columnas'
SALIDA = RAIZ / 'columnas'
VISTA_PREVIA = SALIDA / '_vista-previa'
PORTADA = RAIZ / 'index.html'
MARCA_INICIO = '<!-- COLUMNAS:INICIO'
MARCA_FIN = '<!-- COLUMNAS:FIN -->'
AUTOR = 'Martín Cabrera Marchán'
EN_PORTADA = 3

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'setiembre', 'octubre', 'noviembre', 'diciembre']
MESES_CORTOS = ['ene.', 'feb.', 'mar.', 'abr.', 'may.', 'jun.', 'jul.', 'ago.',
                'set.', 'oct.', 'nov.', 'dic.']


@dataclass
class Columna:
    origen: Path
    titulo: str
    fecha: dt.date
    resumen: str
    cuerpo_md: str
    slug: str
    estado: str = 'borrador'
    etiquetas: list[str] = field(default_factory=list)
    medio_original: str = ''
    url_original: str = ''

    @property
    def palabras(self) -> int:
        return len(re.findall(r'\w+', self.cuerpo_md))

    @property
    def lectura(self) -> str:
        return f'{max(1, round(self.palabras / 200))} min de lectura'


# Utilidades -------------------------------------------------------------

def e(texto: str) -> str:
    return html.escape(texto, quote=True)


def fecha_larga(f: dt.date) -> str:
    return f'{f.day} de {MESES[f.month - 1]} de {f.year}'


def fecha_corta(f: dt.date) -> str:
    return f'{f.day} {MESES_CORTOS[f.month - 1]} {f.year}'


def slugify(texto: str) -> str:
    import unicodedata
    base = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    base = re.sub(r'[^a-zA-Z0-9]+', '-', base).strip('-').lower()
    return base[:80].strip('-') or 'columna'


def url_sitio() -> str:
    """Toma el dominio de la URL canónica de la portada para no duplicar configuración."""
    m = re.search(r'<link rel="canonical" href="([^"]+)"', PORTADA.read_text(encoding='utf-8'))
    return (m.group(1) if m else 'https://example.com/').rstrip('/') + '/'


# Markdown mínimo --------------------------------------------------------

def en_linea(texto: str) -> str:
    """Negrita, cursiva y enlaces sobre texto ya escapado."""
    texto = e(texto)
    texto = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*|#[^)\s]*)\)',
                   lambda m: f'<a href="{m.group(2)}"'
                   + (' rel="noopener" target="_blank"' if m.group(2).startswith('http') else '')
                   + f'>{m.group(1)}</a>', texto)
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    texto = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', texto)
    texto = re.sub(r'(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)', r'<em>\1</em>', texto)
    return texto


def markdown_a_html(md: str) -> str:
    """Convierte un subconjunto de Markdown: párrafos, ## y ### subtítulos,
    listas con - o 1., citas con > y separadores ---."""
    bloques: list[str] = []
    for bloque in re.split(r'\n\s*\n', md.strip()):
        lineas = [l.rstrip() for l in bloque.strip('\n').split('\n')]
        primera = lineas[0].lstrip()
        if primera.startswith('### '):
            bloques.append(f'<h3>{en_linea(primera[4:])}</h3>')
        elif primera.startswith('## '):
            bloques.append(f'<h2>{en_linea(primera[3:])}</h2>')
        elif primera in ('---', '***'):
            bloques.append('<hr>')
        elif all(l.lstrip().startswith('>') for l in lineas):
            texto = ' '.join(l.lstrip()[1:].strip() for l in lineas)
            bloques.append(f'<blockquote><p>{en_linea(texto)}</p></blockquote>')
        elif all(re.match(r'\s*[-*] ', l) for l in lineas):
            items = ''.join(f'<li>{en_linea(re.sub(r"^\s*[-*] ", "", l))}</li>' for l in lineas)
            bloques.append(f'<ul>{items}</ul>')
        elif all(re.match(r'\s*\d+[.)] ', l) for l in lineas):
            items = ''.join(f'<li>{en_linea(re.sub(r"^\s*\d+[.)] ", "", l))}</li>' for l in lineas)
            bloques.append(f'<ol>{items}</ol>')
        else:
            bloques.append(f'<p>{en_linea(" ".join(l.strip() for l in lineas))}</p>')
    return '\n'.join(bloques)


# Lectura de fuentes -----------------------------------------------------

def leer(ruta: Path) -> Columna:
    texto = ruta.read_text(encoding='utf-8').replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n(.*)', texto, re.S)
    if not m:
        raise ValueError(f'{ruta.name}: falta la cabecera entre líneas «---».')
    meta: dict[str, str] = {}
    for linea in m.group(1).split('\n'):
        if ':' in linea and not linea.lstrip().startswith('#'):
            clave, valor = linea.split(':', 1)
            meta[clave.strip().lower()] = valor.strip().strip('"').strip("'")
    for requerido in ('titulo', 'fecha'):
        if not meta.get(requerido):
            raise ValueError(f'{ruta.name}: falta «{requerido}» en la cabecera.')
    try:
        fecha = dt.date.fromisoformat(meta['fecha'])
    except ValueError:
        raise ValueError(f'{ruta.name}: la fecha debe tener el formato AAAA-MM-DD.') from None
    estado = meta.get('estado', 'borrador').lower()
    if estado not in ('publicado', 'borrador'):
        raise ValueError(f'{ruta.name}: «estado» debe ser «publicado» o «borrador».')
    return Columna(
        origen=ruta,
        titulo=meta['titulo'],
        fecha=fecha,
        resumen=meta.get('resumen', ''),
        cuerpo_md=m.group(2),
        slug=slugify(meta.get('slug') or meta['titulo']),
        estado=estado,
        etiquetas=[t.strip() for t in meta.get('etiquetas', '').split(',') if t.strip()],
        medio_original=meta.get('medio_original', ''),
        url_original=meta.get('url_original', ''),
    )


# Plantillas -------------------------------------------------------------

def cabecera(titulo: str, descripcion: str, url: str, prefijo: str, indexable: bool,
             tipo: str = 'website', extra: str = '') -> str:
    robots = '' if indexable else '\n  <meta name="robots" content="noindex, nofollow">'
    return f'''<!doctype html>
<html lang="es-PE">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#102735">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descripcion)}">{robots}
  <link rel="canonical" href="{e(url)}">
  <meta property="og:type" content="{tipo}">
  <meta property="og:locale" content="es_PE">
  <meta property="og:site_name" content="{AUTOR}">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:image" content="{e(url_sitio())}assets/og-martin-cabrera.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefijo}favicon.svg" type="image/svg+xml">
  <link rel="alternate" type="application/rss+xml" title="Columna de Martín Cabrera" href="{prefijo}feed.xml">
  <link rel="stylesheet" href="{prefijo}styles.css">
  <script>document.documentElement.classList.add('js');</script>
  <script src="{prefijo}site.js" defer></script>{extra}
</head>
<body>
  <a class="skip-link" href="#contenido">Ir al contenido</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{prefijo}index.html" aria-label="Martín Cabrera, inicio"><span class="monogram" aria-hidden="true">MC<span>.</span></span><span class="brand-name">Martín Cabrera<span>ESTRATEGIA Y ASUNTOS PÚBLICOS</span></span></a>
      <button class="menu-toggle" type="button" aria-controls="navegacion" aria-expanded="false"><span>Menú</span><span class="menu-lines" aria-hidden="true"></span></button>
      <nav id="navegacion" aria-label="Navegación principal">
        <a href="{prefijo}index.html#especialidades">Especialidades</a><a href="{prefijo}index.html#trayectoria">Trayectoria</a><a href="{prefijo}index.html#enfoque">Enfoque</a><a href="{prefijo}columnas/index.html" aria-current="page">Columna</a><a href="{prefijo}index.html#medios">En medios</a><a class="nav-contact" href="{prefijo}index.html#contacto">Conversemos</a>
      </nav>
    </div>
  </header>
'''


def pie(prefijo: str) -> str:
    return f'''  <footer class="site-footer">
    <div class="container footer-inner">
      <a class="footer-brand" href="{prefijo}index.html">Martín Cabrera<span>Marchán</span></a>
      <p>Gestión pública · Asuntos parlamentarios · Relaciones interinstitucionales · Arbitraje</p>
      <nav class="footer-nav" aria-label="Enlaces del pie de página"><a href="{prefijo}columnas/index.html">Columnas</a><a href="{prefijo}feed.xml">RSS</a><a href="mailto:martin@cabrera.pe">Correo</a></nav>
      <span class="footer-copy">© {dt.date.today().year} Martín Cabrera</span>
    </div>
  </footer>
</body>
</html>
'''


def pagina_columna(c: Columna, base: str, borrador: bool) -> str:
    prefijo = '../../' if borrador else '../'
    url = f'{base}columnas/{c.slug}.html'
    descripcion = c.resumen or f'Columna de {AUTOR}.'
    datos = f'''
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "OpinionNewsArticle", "headline": {jsonstr(c.titulo)}, "description": {jsonstr(descripcion)}, "datePublished": "{c.fecha.isoformat()}", "inLanguage": "es-PE", "url": {jsonstr(url)}, "author": {{"@type": "Person", "name": "{AUTOR}", "url": {jsonstr(base)}}}}}
  </script>'''
    aviso = '<div class="draft-banner" role="note">Vista previa de borrador: no está publicada, no aparece en el archivo ni en los buscadores.</div>\n' if borrador else ''
    etiquetas = ''.join(f'<span>{e(t)}</span>' for t in c.etiquetas)
    original = ''
    if c.url_original:
        medio = e(c.medio_original or 'el medio original')
        original = f'<p class="original-source">Publicada originalmente en <a href="{e(c.url_original)}" rel="noopener" target="_blank">{medio}</a>.</p>'
    elif c.medio_original:
        original = f'<p class="original-source">Publicada originalmente en {e(c.medio_original)}.</p>'
    return (cabecera(f'{c.titulo} | Columna de Martín Cabrera', descripcion, url, prefijo,
                     indexable=not borrador, tipo='article', extra=datos)
            + f'''  {aviso}<main id="contenido" tabindex="-1">
    <article>
      <header class="article-hero">
        <div class="container">
          <p class="breadcrumb"><a href="{prefijo}columnas/index.html">Columna</a> · {fecha_larga(c.fecha)}</p>
          <h1>{e(c.titulo)}</h1>
          {f'<p class="article-dek">{e(c.resumen)}</p>' if c.resumen else ''}
          <p class="article-meta"><span>Por <strong>{AUTOR}</strong></span><time datetime="{c.fecha.isoformat()}">{fecha_larga(c.fecha)}</time><span>{c.lectura}</span>{etiquetas}</p>
        </div>
      </header>
      <div class="container article-body">
{markdown_a_html(c.cuerpo_md)}
      </div>
      <footer class="container article-foot">
        <div class="author-box">
          <img src="{prefijo}assets/martin-cabrera-avatar.jpg" width="88" height="88" alt="" loading="lazy">
          <p><strong>{AUTOR}</strong>Abogado, árbitro y consultor en gestión pública, asuntos parlamentarios y relaciones interinstitucionales.</p>
        </div>
        {original}
        <div class="article-actions"><a class="text-link" href="{prefijo}columnas/index.html">Más columnas</a><a class="text-link" href="mailto:martin@cabrera.pe?subject={quote('Sobre la columna: ' + c.titulo)}">Comentar por correo</a><a class="text-link" href="{prefijo}feed.xml">RSS</a></div>
      </footer>
    </article>
  </main>
''' + pie(prefijo))


def pagina_archivo(columnas: list[Columna], base: str) -> str:
    cuerpo = []
    anio = None
    for c in columnas:
        if c.fecha.year != anio:
            if anio is not None:
                cuerpo.append('</div>')
            anio = c.fecha.year
            cuerpo.append(f'<h2 class="archive-year">{anio}</h2><div>')
        cuerpo.append(tarjeta(c, prefijo_enlace='', nivel='h3'))
    if cuerpo:
        cuerpo.append('</div>')
    else:
        cuerpo.append('<p class="empty-state">Aún no hay columnas publicadas en este sitio.</p>')
    return (cabecera('Columna | Martín Cabrera Marchán',
                     'Columnas de Martín Cabrera Marchán sobre Congreso, gestión pública, control y relaciones interinstitucionales.',
                     f'{base}columnas/', '../', indexable=True)
            + f'''  <main id="contenido" tabindex="-1">
    <header class="article-hero">
      <div class="container">
        <p class="breadcrumb"><a href="../index.html">Inicio</a> · Columna</p>
        <h1>Lectura de <em>la coyuntura.</em></h1>
        <p class="article-dek">Análisis sobre Congreso, gestión pública, control y relaciones entre el Estado y el sector privado.</p>
        <p class="article-meta"><a href="../feed.xml">Suscríbete por RSS</a><a href="../index.html#columna">Columnas publicadas en medios</a></p>
      </div>
    </header>
    <section class="section column-section" aria-label="Archivo de columnas">
      <div class="container archive-list">
{chr(10).join(cuerpo)}
      </div>
    </section>
  </main>
''' + pie('../'))


def tarjeta(c: Columna, prefijo_enlace: str, nivel: str = 'h4', destacada: bool = False) -> str:
    clase = 'column-card is-lead' if destacada else 'column-card'
    resumen = f'<p>{e(c.resumen)}</p>' if c.resumen else ''
    return (f'<article class="{clase}"><span class="press-meta"><time datetime="{c.fecha.isoformat()}">{fecha_corta(c.fecha)}</time> · {c.lectura}</span>'
            f'<{nivel}><a href="{prefijo_enlace}{c.slug}.html">{e(c.titulo)}</a></{nivel}>{resumen}</article>')


def jsonstr(texto: str) -> str:
    import json
    return json.dumps(texto, ensure_ascii=False)


def quote(texto: str) -> str:
    from urllib.parse import quote as q
    return q(texto, safe='')


def feed(columnas: list[Columna], base: str) -> str:
    items = []
    for c in columnas[:30]:
        fecha = dt.datetime.combine(c.fecha, dt.time(8, 0), tzinfo=dt.timezone(dt.timedelta(hours=-5)))
        url = f'{base}columnas/{c.slug}.html'
        items.append(f'''    <item>
      <title>{e(c.titulo)}</title>
      <link>{e(url)}</link>
      <guid isPermaLink="true">{e(url)}</guid>
      <pubDate>{format_datetime(fecha)}</pubDate>
      <description>{e(c.resumen)}</description>
      <content:encoded><![CDATA[{markdown_a_html(c.cuerpo_md).replace(']]>', ']]&gt;')}]]></content:encoded>
    </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Columna de Martín Cabrera Marchán</title>
    <link>{e(base)}columnas/</link>
    <atom:link href="{e(base)}feed.xml" rel="self" type="application/rss+xml"/>
    <description>Análisis sobre Congreso, gestión pública, control y relaciones interinstitucionales.</description>
    <language>es-PE</language>
{chr(10).join(items)}
  </channel>
</rss>
'''


def sitemap(columnas: list[Columna], base: str) -> str:
    urls = [(base, None), (f'{base}columnas/', columnas[0].fecha if columnas else None)]
    urls += [(f'{base}columnas/{c.slug}.html', c.fecha) for c in columnas]
    filas = '\n'.join(f'  <url><loc>{e(u)}</loc>' + (f'<lastmod>{f.isoformat()}</lastmod>' if f else '') + '</url>' for u, f in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{filas}\n</urlset>\n'


def actualizar_portada(columnas: list[Columna]) -> None:
    texto = PORTADA.read_text(encoding='utf-8')
    ini = texto.find(MARCA_INICIO)
    fin = texto.find(MARCA_FIN)
    if ini < 0 or fin < 0:
        raise ValueError('index.html: no se encontraron las marcas COLUMNAS:INICIO / COLUMNAS:FIN.')
    ini = texto.index('-->', ini) + 3
    if columnas:
        bloque = '\n'.join('            ' + tarjeta(c, 'columnas/', destacada=(i == 0)) for i, c in enumerate(columnas[:EN_PORTADA]))
    else:
        bloque = '            <p class="empty-state">La primera columna de este sitio se publicará próximamente. Mientras tanto, puedes leer las columnas publicadas en medios.</p>'
    texto = texto[:ini] + '\n' + bloque + '\n            ' + texto[fin:]
    PORTADA.write_text(texto, encoding='utf-8')


# Principal --------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--borradores', action='store_true', help='genera vistas previas de borradores en columnas/_vista-previa/')
    args = parser.parse_args()

    base = url_sitio()
    hoy = dt.date.today()
    todas: list[Columna] = []
    errores = []
    for ruta in sorted(FUENTES.glob('*.md')):
        if ruta.name.startswith('_') and not args.borradores:
            continue
        try:
            todas.append(leer(ruta))
        except ValueError as err:
            errores.append(str(err))
    if errores:
        print('No se publicó nada. Corrige lo siguiente:', *errores, sep='\n  - ', file=sys.stderr)
        return 1

    slugs = {}
    for c in todas:
        if c.slug in slugs:
            print(f'Dos columnas generan la misma dirección «{c.slug}»: {slugs[c.slug]} y {c.origen.name}. Añade «slug:» a una de ellas.', file=sys.stderr)
            return 1
        slugs[c.slug] = c.origen.name

    publicadas = sorted((c for c in todas if c.estado == 'publicado' and c.fecha <= hoy and not c.origen.name.startswith('_')),
                        key=lambda c: (c.fecha, c.titulo), reverse=True)
    programadas = [c for c in todas if c.estado == 'publicado' and c.fecha > hoy]
    borradores = [c for c in todas if c.estado == 'borrador' or c.origen.name.startswith('_')]

    SALIDA.mkdir(exist_ok=True)
    # Elimina páginas generadas antes que ya no correspondan (por ejemplo, una columna retirada).
    vigentes = {f'{c.slug}.html' for c in publicadas} | {'index.html'}
    for vieja in SALIDA.glob('*.html'):
        if vieja.name not in vigentes:
            vieja.unlink()
    for c in publicadas:
        (SALIDA / f'{c.slug}.html').write_text(pagina_columna(c, base, borrador=False), encoding='utf-8')
    (SALIDA / 'index.html').write_text(pagina_archivo(publicadas, base), encoding='utf-8')
    (RAIZ / 'feed.xml').write_text(feed(publicadas, base), encoding='utf-8')
    (RAIZ / 'sitemap.xml').write_text(sitemap(publicadas, base), encoding='utf-8')
    (RAIZ / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /columnas/_vista-previa/\n\nSitemap: {base}sitemap.xml\n', encoding='utf-8')
    actualizar_portada(publicadas)

    if VISTA_PREVIA.exists():
        shutil.rmtree(VISTA_PREVIA)
    if args.borradores and (borradores or programadas):
        VISTA_PREVIA.mkdir(parents=True)
        for c in borradores + programadas:
            (VISTA_PREVIA / f'{c.slug}.html').write_text(pagina_columna(c, base, borrador=True), encoding='utf-8')

    print(f'Columnas publicadas: {len(publicadas)}')
    for c in publicadas:
        print(f'  · {c.fecha.isoformat()}  columnas/{c.slug}.html')
    if programadas:
        print(f'Programadas (se publicarán al ejecutar el script desde su fecha): {len(programadas)}')
        for c in programadas:
            print(f'  · {c.fecha.isoformat()}  {c.titulo}')
    if borradores:
        print(f'Borradores sin publicar: {len(borradores)}' + (' (vista previa en columnas/_vista-previa/)' if args.borradores else ''))
        for c in borradores:
            print(f'  · {c.origen.name}' + (f'  →  columnas/_vista-previa/{c.slug}.html' if args.borradores else ''))
    print(f'Dominio usado en RSS y sitemap: {base}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
