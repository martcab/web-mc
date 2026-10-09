#!/usr/bin/env python3
"""Genera martin_cabrera_autonomo.html: la portada en un solo archivo.

Incrusta estilos, JavaScript, favicon y retrato para revisar el sitio sin
servidor (doble clic en el archivo). Los enlaces a columnas/ y feed.xml solo
funcionan si el archivo está junto a la carpeta del proyecto.

Uso: python3 herramientas/generar_autonomo.py
"""
import base64
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def data_uri(ruta: Path, tipo: str) -> str:
    return f'data:{tipo};base64,' + base64.b64encode(ruta.read_bytes()).decode()


def main() -> None:
    html = (RAIZ / 'index.html').read_text(encoding='utf-8')
    css = (RAIZ / 'styles.css').read_text(encoding='utf-8')
    js = (RAIZ / 'site.js').read_text(encoding='utf-8')
    retrato = data_uri(RAIZ / 'assets' / 'martin-cabrera-retrato-900.jpg', 'image/jpeg')
    icono = data_uri(RAIZ / 'favicon.svg', 'image/svg+xml')

    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>\n{css}</style>')
    html = html.replace('<script src="site.js" defer></script>', '')
    html = html.replace('</body>', f'<script>\n{js}</script>\n</body>')
    html = html.replace('href="favicon.svg"', f'href="{icono}"')
    html = re.sub(r'\s*<link rel="preload" as="image"[^>]*>', '', html)
    html = re.sub(r'<picture>.*?</picture>',
                  lambda m: re.sub(r'<img src="[^"]+" srcset="[^"]+" sizes="[^"]+"', f'<img src="{retrato}"',
                                   re.search(r'<img [^>]+>', m.group(0)).group(0)),
                  html, flags=re.S)
    destino = RAIZ / 'martin_cabrera_autonomo.html'
    destino.write_text(html, encoding='utf-8')
    print(f'Generado {destino.name} ({destino.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
