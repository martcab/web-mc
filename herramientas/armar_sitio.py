#!/usr/bin/env python3
"""Arma la carpeta _site/ con solo los archivos públicos del sitio.

La usa GitHub Actions para publicar en GitHub Pages, y sirve para revisar
localmente exactamente lo que se subirá:

  python3 herramientas/publicar.py
  python3 herramientas/armar_sitio.py
  python3 -m http.server 8000 --directory _site

Quedan fuera las fuentes y herramientas (contenido/, herramientas/, docs/),
las vistas previas de borradores, las fotografías originales y la versión
autónoma.
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / '_site'
ARCHIVOS = ['index.html', 'styles.css', 'site.js', 'favicon.svg', 'feed.xml', 'sitemap.xml', 'robots.txt', 'CNAME']
CARPETAS = ['assets', 'publicaciones']
EXCLUIR = shutil.ignore_patterns('_vista-previa', 'originales', '.DS_Store')


def main() -> None:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    DESTINO.mkdir()
    for nombre in ARCHIVOS:
        origen = RAIZ / nombre
        if not origen.exists():
            raise SystemExit(f'Falta {nombre}. Ejecuta antes python3 herramientas/publicar.py.')
        shutil.copy2(origen, DESTINO / nombre)
    for nombre in CARPETAS:
        shutil.copytree(RAIZ / nombre, DESTINO / nombre, ignore=EXCLUIR)
    (DESTINO / '.nojekyll').touch()  # GitHub Pages sirve los archivos tal cual, sin Jekyll
    archivos = [p for p in DESTINO.rglob('*') if p.is_file()]
    peso = sum(p.stat().st_size for p in archivos)
    print(f'_site/ listo: {len(archivos)} archivos, {peso / 1024 / 1024:.1f} MB')


if __name__ == '__main__':
    main()
