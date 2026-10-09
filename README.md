# Martín Cabrera Marchán — sitio personal

Sitio estático de una página, con columna de opinión y sección de medios. HTML, CSS y JavaScript nativos, sin dependencias, sin base de datos y sin servidor de aplicación. Se aloja en cualquier servicio de archivos estáticos.

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
| `index.html` | Portada: inicio, especialidades, trayectoria, enfoque, columna, en medios y contacto. |
| `styles.css` | Diseño, paleta, tipografía y adaptación a pantallas. Variables de color al inicio. |
| `site.js` | Menú móvil, copia del correo, preparación de la consulta (`mailto:`) y carga de videos al pulsar. |
| `favicon.svg` | Monograma MC. |
| `assets/` | Retrato (recortes 3:4 en JPG y WebP), avatar e imagen para redes (`og-martin-cabrera.jpg`). `martin-cabrera.jpg` es la fotografía original sin tocar. |
| `contenido/columnas/` | **Aquí escribes la columna**, un archivo `.md` por texto. `_plantilla.md` explica el formato. |
| `columnas/` | Páginas generadas de la columna y su archivo. No se editan a mano. |
| `feed.xml`, `sitemap.xml`, `robots.txt` | Generados por el script de publicación. |
| `herramientas/publicar.py` | Publica la columna (Python 3, solo biblioteca estándar). |
| `herramientas/generar_autonomo.py` | Regenera la versión en un solo archivo. |
| `docs/` | Benchmark y propuesta de diseño, comprobaciones realizadas, guía de la columna y capturas antes/después. |

## Publicar una columna (semanal o diaria)

1. Copia `contenido/columnas/_plantilla.md` con un nombre nuevo sin guion bajo, por ejemplo `2026-10-12-reforma-del-reglamento.md`.
2. Completa la cabecera (`titulo`, `fecha`, `resumen`, `etiquetas`) y escribe el texto en Markdown sencillo.
3. Para revisarla antes de publicar: `python3 herramientas/publicar.py --borradores` y abre `http://localhost:8000/columnas/_vista-previa/`.
4. Cambia `estado: borrador` por `estado: publicado` y ejecuta `python3 herramientas/publicar.py`.
5. Sube los archivos al alojamiento.

El script crea la página de la columna, actualiza el archivo, las tres más recientes en la portada, el RSS y el sitemap. Una fecha futura deja la columna programada hasta que el script se ejecute desde ese día. Detalles en `docs/COLUMNA.md`.

## Medios y redes

- **Columnas en medios** (sección 04) y **entrevistas y declaraciones** (sección 05) están en `index.html`. Para añadir una entrada, copia un `<li>` o un `<article class="video-card">` existente.
- **Videos de YouTube**: basta con poner el identificador del video en `data-youtube="…"`. El reproductor (dominio `youtube-nocookie.com`) solo se carga cuando el visitante pulsa; antes no hay conexión con YouTube.
- **Redes sociales**: en la lista «Sígueme» hay entradas ocultas para LinkedIn, X y YouTube. Reemplaza `REEMPLAZAR` por tu usuario real y borra el atributo `hidden`. Se dejaron ocultas porque no se pudo verificar la dirección de tus perfiles.

## Contacto y datos

El formulario prepara un correo `mailto:` dirigido a `martin@cabrera.pe`. El visitante revisa y envía el mensaje desde su propia aplicación. La página no envía, no almacena datos y no muestra confirmación de envío. No hay analítica, cookies propias ni autenticación.

## Antes de publicar en un dominio propio

La URL canónica aún apunta a `https://martin-cabrera-estrategia.martcab.chatgpt.site/`. Cuando definas el dominio real, cámbiala en `index.html` (`canonical`, `og:url`, `og:image` y el bloque JSON-LD) y vuelve a ejecutar `python3 herramientas/publicar.py`: el script toma el dominio de la URL canónica para el RSS, el sitemap, robots.txt y las columnas. Después regenera el autónomo.
