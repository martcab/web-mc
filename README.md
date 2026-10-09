# Martín Cabrera Marchán — sitio personal

Sitio estático con portada de una página y repositorio oficial de columnas, entrevistas, declaraciones y opiniones. HTML, CSS y JavaScript nativos, sin dependencias, sin base de datos y sin servidor de aplicación. Se aloja en cualquier servicio de archivos estáticos.

Origen: exportación del 6 de octubre de 2026 (`SOURCE_MANIFEST.json` conserva las huellas de los archivos originales). La primera revisión del repositorio guarda esa base sin cambios.

## Verlo en local

```sh
python3 -m http.server 8000
```

Abre `http://localhost:8000`. Si el puerto está ocupado, usa otro (`8080`, `8001`…). Las rutas son relativas, así que `index.html` también se puede abrir con doble clic, aunque el servidor local reproduce mejor el alojamiento real.

`martin_cabrera_autonomo.html` es la portada en un solo archivo (estilos, JavaScript y retrato incrustados) para revisarla sin instalar nada. Se regenera con `python3 herramientas/generar_autonomo.py`. Los cambios se hacen en los archivos separados, no en el autónomo.

## Estructura

| Archivo | Función |
| --- | --- |
| `index.html` | Portada: inicio, especialidades, trayectoria, enfoque, publicaciones, en medios y contacto. |
| `styles.css` | Diseño, paleta (afín a IPOC: azul, negro, gris, amarillo y rojo sangre), tipografía y adaptación a pantallas. Variables al inicio. |
| `site.js` | Menú móvil, copia del correo, preparación de la consulta (`mailto:`) y carga de videos al pulsar. |
| `favicon.svg` | Monograma MC. |
| `assets/` | Retrato (recortes 3:4 en JPG y WebP), avatar e imagen para redes (`og-martin-cabrera.jpg`). `martin-cabrera.jpg` es la fotografía original sin tocar. |
| `assets/fonts/` | Archivo (titulares) y Public Sans (texto), fuentes libres (licencia OFL) alojadas en el propio sitio: no se descargan de servicios externos. |
| `contenido/publicaciones/` | **Aquí agregas cada columna, entrevista, declaración u opinión**, un archivo `.md` por pieza. `_plantilla.md` explica el formato. |
| `publicaciones/` | Páginas generadas: una por publicación, el archivo completo y los filtros por tipo. No se editan a mano. |
| `feed.xml`, `sitemap.xml`, `robots.txt` | Generados por el script de publicación. |
| `herramientas/publicar.py` | Publica el repositorio (Python 3, solo biblioteca estándar). |
| `herramientas/qa/` | Comprobaciones automáticas con Playwright. |
| `herramientas/generar_autonomo.py` | Regenera la versión en un solo archivo. |
| `docs/` | Benchmark y propuesta de diseño, comprobaciones realizadas, guía de publicaciones y capturas antes/después. |

## Publicar (columna semanal o diaria, entrevistas, declaraciones, opiniones)

1. Copia `contenido/publicaciones/_plantilla.md` con un nombre nuevo sin guion bajo, por ejemplo `2026-10-12-reforma-del-reglamento.md`.
2. Completa la cabecera (`titulo`, `tipo`, `fecha`, `medio`, `url_original`, `resumen`…) y, si corresponde, el texto en Markdown sencillo.
3. Para revisar antes: `python3 herramientas/publicar.py --borradores` y abre `http://localhost:8000/publicaciones/_vista-previa/`.
4. Con `estado: publicado`, ejecuta `python3 herramientas/publicar.py`.
5. Sube los archivos al alojamiento.

El script crea la página de cada publicación, el archivo por año con filtros por tipo, los bloques de la portada, el RSS y el sitemap. Detalles en `docs/PUBLICACIONES.md`.

## Redes sociales

Tus perfiles (LinkedIn, X, Instagram, Facebook y TikTok) aparecen en «Sígueme en redes» (sección En medios), en el pie de todas las páginas y en los datos estructurados para buscadores (`sameAs`). Para cambiar uno, edita la lista `REDES` al inicio de `herramientas/publicar.py` (pie de las publicaciones) y los mismos enlaces en `index.html`.

Se usan enlaces, no muros incrustados: incrustar los perfiles de X, Instagram, Facebook o TikTok exige cargar sus scripts, que rastrean a los visitantes y hacen más lenta la página. Si más adelante quieres un muro concreto, se puede añadir con carga al pulsar, como los videos.

## Contacto y datos

El formulario prepara un correo `mailto:` dirigido a `martin@cabrera.pe`. El visitante revisa y envía el mensaje desde su propia aplicación. La página no envía, no almacena datos y no muestra confirmación de envío. No hay analítica, cookies propias ni autenticación.

## Antes de publicar en un dominio propio

La URL canónica aún apunta a `https://martin-cabrera-estrategia.martcab.chatgpt.site/`. Cuando definas el dominio real, cámbiala en `index.html` (`canonical`, `og:url`, `og:image` y el bloque JSON-LD) y vuelve a ejecutar `python3 herramientas/publicar.py`: el script toma el dominio de la URL canónica para el RSS, el sitemap, robots.txt y las páginas de publicaciones. Después regenera el autónomo.
