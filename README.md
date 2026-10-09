# Martin Cabrera Marchán — sitio personal

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
| `assets/` | Retratos de estudio recortados en JPG y WebP (portada y trayectoria), avatar e imagen para redes (`og-martin-cabrera.jpg`). |
| `assets/originales/` | Fotografías originales sin modificar: los tres retratos de estudio y la foto anterior en el hall. |
| `assets/fonts/` | Archivo (titulares) y Public Sans (texto), fuentes libres (licencia OFL) alojadas en el propio sitio: no se descargan de servicios externos. |
| `contenido/publicaciones/` | **Aquí agregas cada columna, entrevista, declaración u opinión**, un archivo `.md` por pieza. `_plantilla.md` explica el formato. |
| `publicaciones/` | Páginas generadas: una por publicación, el archivo completo y los filtros por tipo. No se editan a mano. |
| `feed.xml`, `sitemap.xml`, `robots.txt` | Generados por el script de publicación. |
| `herramientas/publicar.py` | Publica el repositorio (Python 3, solo biblioteca estándar). |
| `herramientas/qa/` | Comprobaciones automáticas con Playwright. |
| `herramientas/generar_autonomo.py` | Regenera la versión en un solo archivo. |
| `herramientas/armar_sitio.py` | Arma `_site/` con solo los archivos públicos (lo usa GitHub Pages). |
| `.github/workflows/publicar.yml`, `CNAME` | Publicación automática en GitHub Pages con el dominio `cabrera.pe`. |
| `docs/` | Benchmark y propuesta de diseño, comprobaciones realizadas, guía de publicaciones y capturas antes/después. |

## Publicar (columna semanal o diaria, entrevistas, declaraciones, opiniones)

1. Copia `contenido/publicaciones/_plantilla.md` con un nombre nuevo sin guion bajo, por ejemplo `2026-10-12-reforma-del-reglamento.md`.
2. Completa la cabecera (`titulo`, `tipo`, `fecha`, `medio`, `url_original`, `resumen`…) y, si corresponde, el texto en Markdown sencillo.
3. Para revisar antes: `python3 herramientas/publicar.py --borradores` y abre `http://localhost:8000/publicaciones/_vista-previa/`.
4. Con `estado: publicado`, ejecuta `python3 herramientas/publicar.py`.
5. Sube los cambios a la rama `main` de GitHub: la web se actualiza sola en uno o dos minutos.

El script crea la página de cada publicación, el archivo por año con filtros por tipo, los bloques de la portada, el RSS y el sitemap. Detalles en `docs/PUBLICACIONES.md`.

## Redes sociales

Tus perfiles (LinkedIn, X, Instagram, Facebook y TikTok) aparecen en «Sígueme en redes» (sección En medios), en el pie de todas las páginas y en los datos estructurados para buscadores (`sameAs`). Para cambiar uno, edita la lista `REDES` al inicio de `herramientas/publicar.py` (pie de las publicaciones) y los mismos enlaces en `index.html`.

Se usan enlaces, no muros incrustados: incrustar los perfiles de X, Instagram, Facebook o TikTok exige cargar sus scripts, que rastrean a los visitantes y hacen más lenta la página. Si más adelante quieres un muro concreto, se puede añadir con carga al pulsar, como los videos.

## Contacto y datos

El formulario prepara un correo `mailto:` dirigido a `martin@cabrera.pe`. El visitante revisa y envía el mensaje desde su propia aplicación. La página no envía, no almacena datos y no muestra confirmación de envío. No hay analítica, cookies propias ni autenticación.

## Publicación en GitHub Pages con cabrera.pe

El repositorio incluye todo lo necesario:

- `.github/workflows/publicar.yml`: cada vez que se suben cambios a la rama `main`, GitHub ejecuta `herramientas/publicar.py`, arma la carpeta pública con `herramientas/armar_sitio.py` y la publica. También corre cada mañana (06:17 en Lima), para que las publicaciones programadas con fecha futura aparezcan solas ese día, y se puede lanzar a mano desde la pestaña **Actions**.
- `CNAME`: el dominio `cabrera.pe`.
- Solo se publican los archivos del sitio (`index.html`, estilos, script, `assets/`, `publicaciones/`, RSS, sitemap). Las fuentes en Markdown, las herramientas, la documentación y las fotos originales no se suben a la web.

### Pasos (una sola vez)

1. **Visibilidad del repositorio.** `martcab/web-mc` es privado. GitHub Pages en repositorios privados requiere GitHub Pro (o un plan de pago). La alternativa gratuita es hacerlo público (*Settings → General → Change visibility*); no contiene contraseñas ni datos privados, solo el sitio y sus herramientas.
2. **Rama `main`.** El flujo publica desde `main`. Crea `main` a partir de la rama de trabajo y márcala como predeterminada (*Settings → Branches*), o fusiona la solicitud de cambios en `main`.
3. **Activar Pages.** *Settings → Pages → Build and deployment → Source: GitHub Actions*.
4. **Dominio.** En la misma pantalla, *Custom domain*: `cabrera.pe`. Cuando el DNS responda, marca **Enforce HTTPS**.
5. **Verificar el dominio** (recomendado, evita que otra cuenta lo use en Pages): perfil de GitHub → *Settings → Pages → Add a domain*, y crea el registro TXT que indique.

### DNS de cabrera.pe

En el panel donde administras el dominio (registrador `.pe` o tu proveedor de DNS):

| Tipo | Nombre | Valor |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `martcab.github.io` |

- **No borres ni cambies los registros MX** (ni los TXT de SPF/DKIM del correo): son los que hacen funcionar `martin@cabrera.pe`.
- Si ya existe un registro A o CNAME para `@` o `www` que apunte a otro servicio, reemplázalo por los de la tabla.
- La propagación puede tardar de minutos a 24 horas. GitHub emite el certificado HTTPS automáticamente cuando el DNS ya apunta bien.

### Revisar antes de publicar

```sh
python3 herramientas/publicar.py
python3 herramientas/armar_sitio.py
python3 -m http.server 8000 --directory _site
```

Muestra en `http://localhost:8000` exactamente lo que se subirá.

## Dominio: cabrera.pe


El sitio está configurado para `https://cabrera.pe/`: URL canónica, `og:url`, `og:image` y datos estructurados en `index.html`; el script toma ese dominio para las páginas de publicaciones, el RSS, el sitemap y robots.txt. Si algún día cambia, edita esas líneas en `index.html` y vuelve a ejecutar `python3 herramientas/publicar.py` y `python3 herramientas/generar_autonomo.py`.

Con la tabla de DNS anterior, GitHub redirige `www.cabrera.pe` a `cabrera.pe` automáticamente.
