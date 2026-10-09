#!/usr/bin/env python3
"""Publica el repositorio de publicaciones de Martín Cabrera como páginas estáticas.

Cada columna, entrevista, declaración u opinión es un archivo de texto en
contenido/publicaciones/*.md. El script genera:
  - publicaciones/<slug>.html     una página permanente por publicación
  - publicaciones/index.html      archivo completo, agrupado por año
  - publicaciones/<tipo>.html     archivo filtrado (columnas, entrevistas…)
  - feed.xml                      canal RSS
  - sitemap.xml, robots.txt       indicaciones para buscadores
  - index.html                    actualiza los bloques generados de la portada

Solo usa la biblioteca estándar de Python 3. El resultado son archivos HTML
que se suben a cualquier alojamiento estático.

Uso:
  python3 herramientas/publicar.py               publica lo que tenga «estado: publicado»
  python3 herramientas/publicar.py --borradores  además genera vistas previas de borradores
                                                 en publicaciones/_vista-previa/ (no se enlazan ni se indexan)
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass, field
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / 'contenido' / 'publicaciones'
SALIDA = RAIZ / 'publicaciones'
VISTA_PREVIA = SALIDA / '_vista-previa'
PORTADA = RAIZ / 'index.html'
AUTOR = 'Martín Cabrera Marchán'
CORREO = 'martin@cabrera.pe'

# tipo: (singular, plural, archivo del filtro)
TIPOS = {
    'columna': ('Columna', 'Columnas', 'columnas.html'),
    'entrevista': ('Entrevista', 'Entrevistas', 'entrevistas.html'),
    'declaracion': ('Declaración', 'Declaraciones', 'declaraciones.html'),
    'opinion': ('Opinión', 'Opiniones', 'opiniones.html'),
}
RESERVADOS = {'index'} | {v[2][:-5] for v in TIPOS.values()}

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'setiembre', 'octubre', 'noviembre', 'diciembre']
MESES_CORTOS = ['ene.', 'feb.', 'mar.', 'abr.', 'may.', 'jun.', 'jul.', 'ago.',
                'set.', 'oct.', 'nov.', 'dic.']


# Fechas parciales -------------------------------------------------------

@dataclass(frozen=True)
class Fecha:
    """Fecha completa (AAAA-MM-DD), parcial (AAAA-MM o AAAA) o desconocida."""
    anio: int | None = None
    mes: int | None = None
    dia: int | None = None

    @classmethod
    def leer(cls, texto: str) -> 'Fecha':
        texto = texto.strip()
        if not texto:
            return cls()
        m = re.fullmatch(r'(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?', texto)
        if not m:
            raise ValueError('la fecha debe ser AAAA-MM-DD, AAAA-MM, AAAA o quedar vacía')
        anio, mes, dia = (int(g) if g else None for g in m.groups())
        dt.date(anio, mes or 1, dia or 1)  # valida
        return cls(anio, mes, dia)

    @property
    def completa(self) -> bool:
        return self.dia is not None

    @property
    def clave(self) -> tuple[int, int, int]:
        return (self.anio or 0, self.mes or 0, self.dia or 0)

    @property
    def iso(self) -> str:
        if not self.anio:
            return ''
        return '-'.join([f'{self.anio:04d}'] + [f'{v:02d}' for v in (self.mes, self.dia) if v])

    def larga(self) -> str:
        if not self.anio:
            return 'Fecha por confirmar'
        if not self.mes:
            return str(self.anio)
        if not self.dia:
            return f'{MESES[self.mes - 1]} de {self.anio}'
        return f'{self.dia} de {MESES[self.mes - 1]} de {self.anio}'

    def corta(self) -> str:
        if not self.anio:
            return 'Sin fecha'
        if not self.mes:
            return str(self.anio)
        if not self.dia:
            return f'{MESES_CORTOS[self.mes - 1]} {self.anio}'
        return f'{self.dia} {MESES_CORTOS[self.mes - 1]} {self.anio}'

    def como_date(self) -> dt.date | None:
        return dt.date(self.anio, self.mes or 1, self.dia or 1) if self.anio else None


@dataclass
class Publicacion:
    origen: Path
    titulo: str
    tipo: str
    fecha: Fecha
    resumen: str
    cuerpo_md: str
    slug: str
    estado: str = 'borrador'
    etiquetas: list[str] = field(default_factory=list)
    medio: str = ''
    programa: str = ''
    url_original: str = ''
    nota_medio: str = ''
    video_youtube: str = ''
    cita: str = ''

    @property
    def singular(self) -> str:
        return TIPOS[self.tipo][0]

    @property
    def palabras(self) -> int:
        return len(re.findall(r'\w+', self.cuerpo_md))

    @property
    def lectura(self) -> str:
        return f'{max(1, round(self.palabras / 200))} min de lectura' if self.palabras >= 60 else ''

    @property
    def fuente(self) -> str:
        return ' · '.join(x for x in (self.medio, self.programa) if x) or 'Este sitio'

    @property
    def descripcion(self) -> str:
        return self.resumen or self.cita or f'{self.singular} de {AUTOR} en {self.fuente}.'


# Utilidades -------------------------------------------------------------

def e(texto: str) -> str:
    return html.escape(texto, quote=True)


def slugify(texto: str) -> str:
    base = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    base = re.sub(r'[^a-zA-Z0-9]+', '-', base).strip('-').lower()
    return base[:80].strip('-') or 'publicacion'


def url_sitio() -> str:
    """Toma el dominio de la URL canónica de la portada para no duplicar configuración."""
    m = re.search(r'<link rel="canonical" href="([^"]+)"', PORTADA.read_text(encoding='utf-8'))
    return (m.group(1) if m else 'https://example.com/').rstrip('/') + '/'


def ordenar(items: list[Publicacion]) -> list[Publicacion]:
    return sorted(items, key=lambda p: (p.fecha.clave, p.titulo), reverse=True)


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
    """Párrafos, ## y ### subtítulos, listas con - o 1., citas con > y separadores ---."""
    bloques: list[str] = []
    for bloque in re.split(r'\n\s*\n', md.strip()):
        if not bloque.strip():
            continue
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
            items = ''.join('<li>' + en_linea(re.sub(r'^\s*[-*] ', '', l)) + '</li>' for l in lineas)
            bloques.append(f'<ul>{items}</ul>')
        elif all(re.match(r'\s*\d+[.)] ', l) for l in lineas):
            items = ''.join('<li>' + en_linea(re.sub(r'^\s*\d+[.)] ', '', l)) + '</li>' for l in lineas)
            bloques.append(f'<ol>{items}</ol>')
        else:
            bloques.append(f'<p>{en_linea(" ".join(l.strip() for l in lineas))}</p>')
    return '\n'.join(bloques)


# Lectura de fuentes -----------------------------------------------------

def leer(ruta: Path) -> Publicacion:
    texto = ruta.read_text(encoding='utf-8').replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n?(.*)', texto, re.S)
    if not m:
        raise ValueError(f'{ruta.name}: falta la cabecera entre líneas «---».')
    meta: dict[str, str] = {}
    for linea in m.group(1).split('\n'):
        if ':' in linea and not linea.lstrip().startswith('#'):
            clave, valor = linea.split(':', 1)
            meta[clave.strip().lower()] = valor.strip().strip('"').strip("'")
    if not meta.get('titulo'):
        raise ValueError(f'{ruta.name}: falta «titulo» en la cabecera.')
    tipo = (meta.get('tipo') or 'columna').lower().replace('ó', 'o').replace('í', 'i')
    if tipo not in TIPOS:
        raise ValueError(f'{ruta.name}: «tipo» debe ser uno de: {", ".join(TIPOS)}.')
    try:
        fecha = Fecha.leer(meta.get('fecha', ''))
    except ValueError as err:
        raise ValueError(f'{ruta.name}: {err}.') from None
    estado = meta.get('estado', 'borrador').lower()
    if estado not in ('publicado', 'borrador'):
        raise ValueError(f'{ruta.name}: «estado» debe ser «publicado» o «borrador».')
    video = meta.get('video_youtube', '')
    if video and not re.fullmatch(r'[\w-]{6,20}', video):
        raise ValueError(f'{ruta.name}: «video_youtube» debe ser solo el identificador del video (por ejemplo, Gtj2sfF3A3Y).')
    url = meta.get('url_original', '')
    if url and not url.startswith(('https://', 'http://')):
        raise ValueError(f'{ruta.name}: «url_original» debe empezar con https://.')
    slug = slugify(meta.get('slug') or meta['titulo'])
    if slug in RESERVADOS:
        slug += '-1'
    return Publicacion(
        origen=ruta, titulo=meta['titulo'], tipo=tipo, fecha=fecha,
        resumen=meta.get('resumen', ''), cuerpo_md=m.group(2).strip(), slug=slug, estado=estado,
        etiquetas=[t.strip() for t in meta.get('etiquetas', '').split(',') if t.strip()],
        medio=meta.get('medio', ''), programa=meta.get('programa', ''), url_original=url,
        nota_medio=meta.get('nota_medio', ''), video_youtube=video, cita=meta.get('cita', ''),
    )


# Piezas comunes ---------------------------------------------------------

def cabecera(titulo: str, descripcion: str, url: str, prefijo: str, indexable: bool,
             tipo_og: str = 'website', extra: str = '') -> str:
    robots = '' if indexable else '\n  <meta name="robots" content="noindex, nofollow">'
    return f'''<!doctype html>
<html lang="es-PE">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101215">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descripcion)}">{robots}
  <link rel="canonical" href="{e(url)}">
  <meta property="og:type" content="{tipo_og}">
  <meta property="og:locale" content="es_PE">
  <meta property="og:site_name" content="{AUTOR}">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:image" content="{e(url_sitio())}assets/og-martin-cabrera.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefijo}favicon.svg" type="image/svg+xml">
  <link rel="alternate" type="application/rss+xml" title="Publicaciones de Martín Cabrera" href="{prefijo}feed.xml">
  <link rel="preload" href="{prefijo}assets/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin>
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
        <a href="{prefijo}index.html#especialidades">Especialidades</a><a href="{prefijo}index.html#trayectoria">Trayectoria</a><a href="{prefijo}index.html#enfoque">Enfoque</a><a href="{prefijo}publicaciones/index.html" aria-current="page">Publicaciones</a><a href="{prefijo}index.html#medios">En medios</a><a class="nav-contact" href="{prefijo}index.html#contacto">Conversemos</a>
      </nav>
    </div>
  </header>
'''


def pie(prefijo: str) -> str:
    return f'''  <footer class="site-footer">
    <div class="container footer-inner">
      <a class="footer-brand" href="{prefijo}index.html">Martín Cabrera<span>Marchán</span></a>
      <p>Gestión pública · Asuntos parlamentarios · Relaciones interinstitucionales · Arbitraje</p>
      <nav class="footer-nav" aria-label="Enlaces del pie de página"><a href="{prefijo}publicaciones/index.html">Publicaciones</a><a href="{prefijo}feed.xml">RSS</a><a href="mailto:{CORREO}">Correo</a></nav>
      <span class="footer-copy">© {dt.date.today().year} Martín Cabrera</span>
    </div>
  </footer>
</body>
</html>
'''


def meta_linea(p: Publicacion, con_tipo: bool = True) -> str:
    partes = []
    if con_tipo:
        partes.append(f'<span class="badge {p.tipo}">{p.singular}</span>')
    partes.append(f'<span>{e(p.fuente)}</span>')
    fecha = f'<time datetime="{p.fecha.iso}">{p.fecha.corta()}</time>' if p.fecha.anio else f'<span>{p.fecha.corta()}</span>'
    partes.append(fecha)
    return f'<span class="press-meta">{"".join(partes)}</span>'


def tarjeta(p: Publicacion, enlace: str, nivel: str = 'h3', destacada: bool = False) -> str:
    clase = 'column-card is-lead' if destacada else 'column-card'
    resumen = f'<p>{e(p.resumen or p.cita)}</p>' if (p.resumen or p.cita) else ''
    return (f'<article class="{clase}">{meta_linea(p)}'
            f'<{nivel}><a href="{enlace}">{e(p.titulo)}</a></{nivel}>{resumen}</article>')


def fila(p: Publicacion, enlace: str) -> str:
    return f'<li><a href="{enlace}">{meta_linea(p)}<span class="press-title">{e(p.titulo)}</span></a></li>'


def marco_video(p: Publicacion, enlace_alterno: str, nivel_texto: str = 'Ver') -> str:
    cita = f'<span class="video-quote">«{e(p.cita.rstrip("."))}»</span>' if p.cita else f'<span class="video-quote">{e(p.titulo)}</span>'
    fuente = f'<span class="video-source">{e(p.fuente)}</span>'
    if p.video_youtube:
        return (f'<div class="video-frame" data-youtube="{e(p.video_youtube)}" data-title="{e(p.titulo)}">'
                f'<a class="video-poster" href="https://www.youtube.com/watch?v={e(p.video_youtube)}" rel="noopener" target="_blank">'
                f'<span class="play" aria-hidden="true"></span>{fuente}<span class="visually-hidden">Reproducir el video: </span>{cita}</a></div>')
    externo = enlace_alterno.startswith('http')
    destino = ' rel="noopener" target="_blank"' if externo else ''
    aviso = '<span class="visually-hidden"> (se abre en otra pestaña)</span>' if externo else ''
    return (f'<div class="video-frame"><a class="video-poster" href="{e(enlace_alterno)}"{destino}>'
            f'<span class="play" aria-hidden="true"></span>{fuente}<span class="visually-hidden">{nivel_texto}: </span>{cita}{aviso}</a></div>')


def tarjeta_video(p: Publicacion, enlace: str) -> str:
    return (f'<article class="video-card">{marco_video(p, enlace)}'
            f'<h3><a href="{enlace}">{e(p.titulo)}</a></h3>'
            + (f'<p>{e(p.resumen)}</p>' if p.resumen else '') + '</article>')


# Páginas ----------------------------------------------------------------

def pagina_publicacion(p: Publicacion, base: str, borrador: bool) -> str:
    prefijo = '../../' if borrador else '../'
    url = f'{base}publicaciones/{p.slug}.html'
    esquema = {'columna': 'OpinionNewsArticle', 'opinion': 'OpinionNewsArticle', 'declaracion': 'NewsArticle', 'entrevista': 'CreativeWork'}[p.tipo]
    datos = {'@context': 'https://schema.org', '@type': esquema, 'headline': p.titulo, 'description': p.descripcion,
             'inLanguage': 'es-PE', 'url': url, 'author': {'@type': 'Person', 'name': AUTOR, 'url': base}}
    if p.fecha.anio:
        datos['datePublished'] = p.fecha.iso
    if p.url_original:
        datos['sameAs'] = p.url_original
    if p.medio:
        datos['publisher'] = {'@type': 'Organization', 'name': p.medio}
    extra = '\n  <script type="application/ld+json">' + json.dumps(datos, ensure_ascii=False) + '</script>'

    aviso = '<div class="draft-banner" role="note">Vista previa de borrador: no está publicada, no aparece en el archivo ni en los buscadores.</div>\n' if borrador else ''
    etiquetas = ''.join(f'<span>{e(t)}</span>' for t in p.etiquetas)
    lectura = f'<span>{p.lectura}</span>' if p.lectura else ''
    fecha = f'<time datetime="{p.fecha.iso}">{p.fecha.larga()}</time>' if p.fecha.anio else f'<span>{p.fecha.larga()}</span>'
    filtro = TIPOS[p.tipo][2]

    cuerpo = []
    con_video = p.tipo == 'entrevista' or bool(p.video_youtube)
    if con_video:
        cuerpo.append(marco_video(p, p.url_original or '#', 'Ver la entrevista'))
    if p.cita and not con_video:  # en las entrevistas la cita ya aparece en el reproductor
        cuerpo.append(f'<blockquote><p>«{e(p.cita.rstrip("."))}»</p></blockquote>')
    if p.cuerpo_md:
        cuerpo.append(f'<div class="prose">\n{markdown_a_html(p.cuerpo_md)}\n</div>')
    if p.url_original and not p.cuerpo_md:
        verbo = 'Ver' if p.tipo == 'entrevista' else 'Leer'
        sitio = p.medio or 'el medio original'
        nota = f' {e(p.nota_medio)}' if p.nota_medio else ''
        cuerpo.append(f'<div class="external-box"><p>{p.singular} publicada en <strong>{e(p.fuente)}</strong>. El contenido completo está en el sitio del medio.{nota}</p>'
                      f'<a class="button dark" href="{e(p.url_original)}" rel="noopener" target="_blank">{verbo} en {e(sitio)}<span class="visually-hidden"> (se abre en otra pestaña)</span></a></div>')
    original = ''
    if p.url_original and p.cuerpo_md:
        nota = f' {e(p.nota_medio)}' if p.nota_medio else ''
        original = f'<p class="original-source">Publicada originalmente en <a href="{e(p.url_original)}" rel="noopener" target="_blank">{e(p.fuente)}</a>.{nota}</p>'

    return (cabecera(f'{p.titulo} | {AUTOR}', p.descripcion, url, prefijo, indexable=not borrador, tipo_og='article', extra=extra)
            + f'''  {aviso}<main id="contenido" tabindex="-1">
    <article>
      <header class="article-hero">
        <div class="container">
          <p class="breadcrumb"><a href="{prefijo}publicaciones/index.html">Publicaciones</a> · <a href="{prefijo}publicaciones/{filtro}">{TIPOS[p.tipo][1]}</a></p>
          <h1>{e(p.titulo)}</h1>
          {f'<p class="article-dek">{e(p.resumen)}</p>' if p.resumen else ''}
          <p class="article-meta"><span class="badge {p.tipo}">{p.singular}</span><span>{e(p.fuente)}</span>{fecha}{lectura}{etiquetas}</p>
        </div>
      </header>
      <div class="container article-body">
{chr(10).join(cuerpo)}
      </div>
      <footer class="container article-foot">
        <div class="author-box">
          <img src="{prefijo}assets/martin-cabrera-avatar.jpg" width="88" height="88" alt="" loading="lazy">
          <p><strong>{AUTOR}</strong>Abogado, árbitro y consultor en gestión pública, asuntos parlamentarios y relaciones interinstitucionales.</p>
        </div>
        {original}
        <div class="article-actions"><a class="text-link" href="{prefijo}publicaciones/index.html">Todas las publicaciones</a><a class="text-link" href="mailto:{CORREO}?subject={quote('Sobre: ' + p.titulo, safe='')}">Comentar por correo</a><a class="text-link" href="{prefijo}feed.xml">RSS</a></div>
      </footer>
    </article>
  </main>
''' + pie(prefijo))


def pagina_archivo(items: list[Publicacion], todas: list[Publicacion], base: str, tipo: str | None) -> str:
    nombre = TIPOS[tipo][1] if tipo else 'Publicaciones'
    archivo = TIPOS[tipo][2] if tipo else 'index.html'
    url = f'{base}publicaciones/' + ('' if not tipo else archivo)
    filtros = [('Todas', 'index.html', len(todas), tipo is None)]
    for clave, (_, plural, destino) in TIPOS.items():
        n = sum(1 for p in todas if p.tipo == clave)
        if n:
            filtros.append((plural, destino, n, tipo == clave))
    chips = ''.join(f'<li><a href="{d}"' + (' aria-current="page"' if actual else '') + f'>{nombre_f} <span>{n}</span></a></li>'
                    for nombre_f, d, n, actual in filtros)
    cuerpo: list[str] = []
    grupo: object = object()
    for p in items:
        g = p.fecha.anio
        if g != grupo:
            if cuerpo:
                cuerpo.append('</div>')
            grupo = g
            cuerpo.append(f'<h2 class="archive-year">{g or "Sin fecha confirmada"}</h2><div>')
        cuerpo.append(tarjeta(p, f'{p.slug}.html'))
    cuerpo.append('</div>' if cuerpo else '<p class="empty-state">Aún no hay publicaciones de este tipo.</p>')
    descripcion = ('Repositorio oficial de columnas, entrevistas, declaraciones y opiniones de Martín Cabrera Marchán '
                   'sobre Congreso, gestión pública, control y relaciones interinstitucionales.')
    miga = 'Publicaciones' if not tipo else f'<a href="index.html">Publicaciones</a> · {nombre}'
    titulo = 'Columnas, entrevistas <em>y opiniones.</em>' if not tipo else f'{e(nombre)}<em>.</em>'
    return (cabecera(f'{nombre} | {AUTOR}', descripcion, url, '../', indexable=True)
            + f'''  <main id="contenido" tabindex="-1">
    <header class="article-hero wide">
      <div class="container">
        <p class="breadcrumb"><a href="../index.html">Inicio</a> · {miga}</p>
        <h1>{titulo}</h1>
        <p class="article-dek">Repositorio oficial de lo que he escrito y dicho sobre Congreso, gestión pública, control y relaciones entre el Estado y el sector privado. Cada publicación tiene aquí su página y el enlace al medio original.</p>
        <p class="article-meta"><a href="../feed.xml">Suscríbete por RSS</a><span>{len(todas)} publicaciones</span></p>
      </div>
    </header>
    <section class="section" aria-label="Archivo de {nombre.lower()}">
      <div class="container archive-list">
        <nav aria-label="Filtrar por tipo"><ul class="archive-filters">{chips}</ul></nav>
{chr(10).join(cuerpo)}
      </div>
    </section>
  </main>
''' + pie('../'))


def feed(items: list[Publicacion], base: str) -> str:
    filas = []
    for p in items[:40]:
        url = f'{base}publicaciones/{p.slug}.html'
        fecha = p.fecha.como_date()
        pub = f'\n      <pubDate>{format_datetime(dt.datetime.combine(fecha, dt.time(8, 0), tzinfo=dt.timezone(dt.timedelta(hours=-5))))}</pubDate>' if fecha else ''
        contenido = markdown_a_html(p.cuerpo_md) if p.cuerpo_md else f'<p>{e(p.descripcion)}</p>'
        if p.url_original:
            contenido += f'<p><a href="{e(p.url_original)}">{e(p.fuente)}</a></p>'
        filas.append(f'''    <item>
      <title>{e(p.titulo)}</title>
      <link>{e(url)}</link>
      <guid isPermaLink="true">{e(url)}</guid>{pub}
      <category>{p.singular}</category>
      <description>{e(p.descripcion)}</description>
      <content:encoded><![CDATA[{contenido.replace(']]>', ']]&gt;')}]]></content:encoded>
    </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Publicaciones de Martín Cabrera Marchán</title>
    <link>{e(base)}publicaciones/</link>
    <atom:link href="{e(base)}feed.xml" rel="self" type="application/rss+xml"/>
    <description>Columnas, entrevistas, declaraciones y opiniones sobre Congreso, gestión pública, control y relaciones interinstitucionales.</description>
    <language>es-PE</language>
{chr(10).join(filas)}
  </channel>
</rss>
'''


def sitemap(items: list[Publicacion], base: str, filtros: list[str]) -> str:
    urls = [(base, None), (f'{base}publicaciones/', None)] + [(f'{base}publicaciones/{f}', None) for f in filtros]
    urls += [(f'{base}publicaciones/{p.slug}.html', p.fecha.iso if p.fecha.completa else None) for p in items]
    filas = '\n'.join(f'  <url><loc>{e(u)}</loc>' + (f'<lastmod>{f}</lastmod>' if f else '') + '</url>' for u, f in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{filas}\n</urlset>\n'


def reemplazar_bloque(texto: str, nombre: str, contenido: str, sangria: str) -> str:
    inicio = f'<!-- {nombre}:INICIO'
    fin = f'<!-- {nombre}:FIN -->'
    i, f = texto.find(inicio), texto.find(fin)
    if i < 0 or f < 0:
        raise ValueError(f'index.html: no se encontraron las marcas {nombre}:INICIO / {nombre}:FIN.')
    i = texto.index('-->', i) + 3
    return texto[:i] + '\n' + contenido + '\n' + sangria + texto[f:]


def actualizar_portada(items: list[Publicacion]) -> None:
    texto = PORTADA.read_text(encoding='utf-8')
    s = '            '
    columnas = [p for p in items if p.tipo == 'columna'][:4]
    opiniones = [p for p in items if p.tipo in ('declaracion', 'opinion')][:5]
    entrevistas = [p for p in items if p.tipo == 'entrevista'][:4]
    vacio = f'{s}<p class="empty-state">Pronto habrá publicaciones en esta sección.</p>'
    texto = reemplazar_bloque(texto, 'PUBLICACIONES:COLUMNAS',
                              '\n'.join(s + tarjeta(p, f'publicaciones/{p.slug}.html', 'h4', i == 0) for i, p in enumerate(columnas)) or vacio, s)
    texto = reemplazar_bloque(texto, 'PUBLICACIONES:OPINIONES',
                              (f'{s}<ul class="press-list">\n' + '\n'.join(s + '  ' + fila(p, f'publicaciones/{p.slug}.html') for p in opiniones) + f'\n{s}</ul>') if opiniones else vacio, s)
    texto = reemplazar_bloque(texto, 'PUBLICACIONES:ENTREVISTAS',
                              '\n'.join(s + tarjeta_video(p, f'publicaciones/{p.slug}.html') for p in entrevistas) or vacio, s)
    PORTADA.write_text(texto, encoding='utf-8')


# Principal --------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--borradores', action='store_true', help='genera vistas previas en publicaciones/_vista-previa/')
    args = parser.parse_args()

    base = url_sitio()
    hoy = dt.date.today()
    todas: list[Publicacion] = []
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

    vistos: dict[str, str] = {}
    for p in todas:
        if p.slug in vistos:
            print(f'Dos publicaciones generan la misma dirección «{p.slug}»: {vistos[p.slug]} y {p.origen.name}. Añade «slug:» a una de ellas.', file=sys.stderr)
            return 1
        vistos[p.slug] = p.origen.name

    def programada(p: Publicacion) -> bool:
        return p.fecha.completa and p.fecha.como_date() > hoy

    publicadas = ordenar([p for p in todas if p.estado == 'publicado' and not programada(p) and not p.origen.name.startswith('_')])
    programadas = [p for p in todas if p.estado == 'publicado' and programada(p)]
    borradores = [p for p in todas if p.estado == 'borrador' or p.origen.name.startswith('_')]

    SALIDA.mkdir(exist_ok=True)
    filtros = [TIPOS[t][2] for t in TIPOS if any(p.tipo == t for p in publicadas)]
    vigentes = {f'{p.slug}.html' for p in publicadas} | {'index.html'} | set(filtros)
    for vieja in SALIDA.glob('*.html'):
        if vieja.name not in vigentes:
            vieja.unlink()
    for p in publicadas:
        (SALIDA / f'{p.slug}.html').write_text(pagina_publicacion(p, base, borrador=False), encoding='utf-8')
    (SALIDA / 'index.html').write_text(pagina_archivo(publicadas, publicadas, base, None), encoding='utf-8')
    for t in TIPOS:
        items = [p for p in publicadas if p.tipo == t]
        if items:
            (SALIDA / TIPOS[t][2]).write_text(pagina_archivo(items, publicadas, base, t), encoding='utf-8')
    (RAIZ / 'feed.xml').write_text(feed(publicadas, base), encoding='utf-8')
    (RAIZ / 'sitemap.xml').write_text(sitemap(publicadas, base, filtros), encoding='utf-8')
    (RAIZ / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /publicaciones/_vista-previa/\n\nSitemap: {base}sitemap.xml\n', encoding='utf-8')
    actualizar_portada(publicadas)

    if VISTA_PREVIA.exists():
        shutil.rmtree(VISTA_PREVIA)
    if args.borradores and (borradores or programadas):
        VISTA_PREVIA.mkdir(parents=True)
        for p in borradores + programadas:
            (VISTA_PREVIA / f'{p.slug}.html').write_text(pagina_publicacion(p, base, borrador=True), encoding='utf-8')

    print(f'Publicaciones: {len(publicadas)}')
    for t, (_, plural, _) in TIPOS.items():
        n = sum(1 for p in publicadas if p.tipo == t)
        if n:
            print(f'  · {plural}: {n}')
    sin_fecha = [p for p in publicadas if not p.fecha.anio]
    if sin_fecha:
        print(f'Sin fecha confirmada: {len(sin_fecha)} ({", ".join(p.origen.name for p in sin_fecha)})')
    if programadas:
        print(f'Programadas (se publicarán al ejecutar el script desde su fecha): {len(programadas)}')
        for p in programadas:
            print(f'  · {p.fecha.iso}  {p.titulo}')
    if borradores:
        print(f'Borradores sin publicar: {len(borradores)}' + (' (vista previa en publicaciones/_vista-previa/)' if args.borradores else ''))
        for p in borradores:
            print(f'  · {p.origen.name}' + (f'  →  publicaciones/_vista-previa/{p.slug}.html' if args.borradores else ''))
    print(f'Dominio usado en RSS y sitemap: {base}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
