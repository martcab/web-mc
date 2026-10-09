# Cambios y comprobaciones

## Revisión 2 — 9 de octubre de 2026: paleta IPOC, tipografía y repositorio de publicaciones

**Cambios**

- Paleta afín a IPOC Consultores (azul `#1F4E79`, gris `#595959`, azul claro `#D6E4F0`, tomados de sus plantillas de documentos) con negro, amarillo y rojo sangre. Detalles en `docs/BENCHMARK.md`.
- Tipografía: Archivo (titulares) y Public Sans (texto), alojadas en `assets/fonts/` con su licencia OFL.
- Favicon e imagen para redes rehechos con la nueva identidad.
- El sitio pasa a ser el **repositorio oficial**: cada columna, entrevista, declaración u opinión es un archivo en `contenido/publicaciones/` y tiene su página en `publicaciones/`, con archivo por año, filtros por tipo, RSS y sitemap. Admite fechas parciales (solo año o año y mes) y publicaciones sin fecha confirmada.
- Las listas de la portada (columnas, opiniones y declaraciones, entrevistas) ya no se escriben a mano: las genera el script a partir de esos archivos.
- Se cargaron las diez publicaciones verificadas en la revisión 1. La antigua carpeta `columnas/` se reemplazó por `publicaciones/` (no tenía textos publicados).
- Defectos visuales corregidos en esta ronda: leyenda del retrato poco legible sobre la parte clara de la foto (degradado reforzado); botón y reproductor dentro de las páginas de publicación heredaban el color y subrayado de los enlaces del texto; la cita de una entrevista se repetía dos veces.

**Comprobaciones ejecutadas** (`herramientas/qa/comprobar.mjs`): **195 de 195 correctas**, sobre la portada, el archivo, un filtro, una columna y una entrevista:

- Sin desplazamiento horizontal, errores de JavaScript ni recursos con error en 1440, 1024, 390 y 360 px.
- Enlaces internos, anclas, fragmentos entre páginas, ids únicos, `alt` en imágenes; RSS, sitemap, robots, fuentes e imágenes responden 200.
- Las fuentes Archivo y Public Sans cargan desde el propio sitio.
- Menú móvil, navegación sin JavaScript, desplegables, teclado y foco visible, texto y zoom al 200 %, formulario y `mailto:` (`herramientas/qa/mailto.mjs`), copia del correo, video sin conexión previa a YouTube, movimiento reducido: sin cambios respecto de la revisión 1 y todo correcto.
- Contraste WCAG de la nueva paleta: todos los pares de texto ≥ 4,77:1 (amarillo sobre azul, solo en titulares grandes); el resto entre 6,6:1 y 10,3:1.
- Versión autónoma regenerada con las fuentes incrustadas.

**Pendientes**: los mismos de la revisión 1 (lectores de pantalla, Safari y Firefox, enlaces externos, validador W3C).

---

## Revisión 1 — 9 de octubre de 2026

### 1. Punto de partida

- Se extrajo `proyecto_martin_cabrera.zip` y se confirmó que las huellas SHA-256 de `index.html`, `styles.css`, `site.js`, `favicon.svg` y `assets/martin-cabrera.jpg` coinciden con `SOURCE_MANIFEST.json`.
- La versión original se guardó sin cambios como primera revisión del repositorio (`Importa el sitio original exportado`) y se sirvió en local para capturarla antes de modificar nada (`docs/capturas/antes-*`).

### 2. Defectos reproducibles corregidos

| Defecto | Cómo se reprodujo | Corrección |
| --- | --- | --- |
| Sin JavaScript, la navegación móvil quedaba oculta e inaccesible. | Chromium sin JS a 390 px: `nav` con `display:none` y botón inútil. | El menú solo se oculta si `<html>` tiene la clase `js`; sin JS, los enlaces se muestran bajo la marca. |
| Contorno de foco cobre `#d1a580` sobre fondos claros: contraste 2,2:1 (WCAG 1.4.11 pide 3:1). | Cálculo de contraste y Tab por la página. | Foco cobre oscuro `#845638` (6,2:1) en fondos claros; cobre en fondos azules (6,9:1). |
| Rutas absolutas (`/styles.css`, `/site.js`): la página se rompe abierta con doble clic o alojada en una subcarpeta. | Abrir `index.html` por `file://`. | Rutas relativas en todo el sitio. |
| Copiar correo: en algunos navegadores la promesa del portapapeles tarda varios segundos en rechazarse y no se ve ninguna respuesta. | Chromium sin permiso de portapapeles: estado vacío al instante. | Tiempo máximo de 1,5 s; después se muestra el correo seleccionado para copiarlo a mano. |
| `mailto:` con saltos de línea `\n`; RFC 6068 indica CRLF. | Inspección de la URL generada. | Saltos convertidos a `%0D%0A`. |
| Consultas largas podían superar el largo de URL que aceptan algunos clientes de correo (2500 caracteres codificados ≈ 7500). | Cálculo de la URL con el máximo anterior. | Máximo de 1500 caracteres con contador visible. |
| Retrato con la figura pequeña dentro del encuadre (recorte de 485×555 sobre una foto vertical completa). | Captura a 1440 px. | Recorte editorial 3:4 y tamaños responsivos (JPG/WebP). |
| Menú móvil abierto: no se cerraba al tocar fuera ni al salir con el teclado; el foco no entraba al menú. | Prueba en 390 y 360 px. | Cierre por clic fuera, por Escape (devuelve el foco) y al salir con Tab; el foco pasa al primer enlace al abrir. |

### 3. Comprobaciones ejecutadas

Herramientas: servidor `python3 -m http.server 8000`, Chromium (Playwright 1.56) en modo *headless*. El guion está en `herramientas/qa/comprobar.mjs` y puede repetirse. Resultado de la última ejecución: **85 de 85 correctas**, más la verificación del `mailto:`.

**Ejecutadas realmente**

- Anchos de 1440, 1024, 390 y 360 px en portada y archivo de columnas: sin desplazamiento horizontal, sin errores de JavaScript en consola, sin recursos con error 4xx/5xx.
- Enlaces internos (portada, archivo, RSS, sitemap, imágenes) con respuesta 200; anclas con destino existente; fragmentos que apuntan desde subpáginas a la portada; ids únicos; todas las imágenes con `alt`.
- Menú móvil en 390 y 360 px: abre, `aria-expanded` correcto, foco al primer enlace, Escape cierra y devuelve el foco, elegir un enlace cierra, clic fuera cierra, la sección destino no queda bajo el encabezado fijo, al volver a escritorio el menú se restablece.
- Sin JavaScript: navegación visible a 390 px.
- Desplegables nativos `<details>`: Enter abre y Espacio cierra.
- Teclado: el primer Tab muestra «Ir al contenido» y el salto lleva el foco a `<main>`; todos los elementos enfocables muestran contorno de al menos 2 px.
- Ampliación: texto al 200 % en 720 y 512 px y zoom de página al 200 % (1440 → 720 px CSS) sin desplazamiento horizontal. En pantallas bajas (≤ 520 px de alto) el encabezado deja de ser fijo para no ocupar la vista.
- Formulario: un contexto con solo espacios muestra error visible, `aria-invalid` y devuelve el foco; no aparece mensaje de envío; el error desaparece al escribir; el contador se actualiza; el mensaje final dice «Consulta preparada», nunca «enviada». La URL `mailto:` lleva destinatario `martin@cabrera.pe`, asunto y cuerpo codificados correctamente con tildes, «», ñ, &, %, # y + (`herramientas/qa/mailto.mjs`).
- Copiar correo: con permiso copia y confirma; sin permiso muestra la alternativa en menos de 2 s.
- Videos: ninguna conexión a YouTube al cargar la página; al pulsar se inserta el reproductor de `youtube-nocookie.com`.
- `prefers-reduced-motion`: desplazamiento sin animación y transiciones desactivadas.
- Contraste de los pares de color principales (cálculo WCAG): todos ≥ 4,6:1; el más bajo es el texto de ejemplo de los campos (4,65:1).
- Script de columna: publicación, vista previa de borradores, archivo, bloque de portada, RSS y sitemap, probado con una columna de prueba que luego se eliminó.
- Versión autónoma: abre por `file://` sin solicitudes fallidas, el retrato carga y el menú funciona.
- Sintaxis: `node --check site.js`.

**No ejecutadas o pendientes**

- Lectores de pantalla reales (NVDA, VoiceOver): no disponibles en el entorno. La estructura de encabezados, etiquetas y regiones `aria-live` se revisó en el código.
- Safari y Firefox, y dispositivos físicos: solo se probó Chromium.
- Enlaces externos (El Comercio, Lampadia, Perú21, YouTube): el proxy del entorno bloquea esos dominios, así que no se comprobó su respuesta HTTP. Las direcciones provienen de resultados de búsqueda.
- Apertura real del cliente de correo: el navegador *headless* no tiene uno; se verificó la URL `mailto:` generada.
- Validación formal con el validador del W3C: sin acceso a la red.

### 4. Información añadida y su fuente

No se inventaron cargos, clientes, cifras ni reconocimientos. Lo nuevo proviene de:

| Dato | Fuente | Estado |
| --- | --- | --- |
| Columnas en El Comercio (2023–2026) y reproducción en Lampadia | Páginas de autor y artículos en elcomercio.pe y lampadia.com (resultados de búsqueda). | Verificado por título y fecha. Para «El Congreso que juró por sus muertos» y «Porque mudos están» no se encontró la URL exacta: enlazan a la página de autor. Sin fecha confirmada: «Cara y Sello», «Mochasueldos» y la entrevista de Perú21; la entrevista de YouTube figura como 2023 (aproximada). |
| Entrevista Perú21 TV («La voz del 21») sobre la asignación congresal | peru21.pe | Verificado por título. Fecha no disponible. |
| Declaraciones en El Comercio (nueva Cámara de Diputados; casos «mochasueldos») | elcomercio.pe | Verificado por título y cita. |
| Video de YouTube `Gtj2sfF3A3Y`, «Martín Cabrera: Congreso es una organización que aún no consigue espacios de consensos» (aprox. 2023) | youtube.com | **Por confirmar**: el título coincide con tu nombre y tema, pero no se pudo ver el canal. Si no eres tú, borra `contenido/publicaciones/2023-congreso-espacios-de-consensos.md` y vuelve a publicar. |
| Gerencia general de ASEPRI | Tu guía de voz de marca. | **Por confirmar** que quieras mostrarlo y que siga vigente. |
| Entregables de las especialidades (ayudas memoria, cuadros comparativos, mapas de actores, planes de incidencia) | Tus plantillas de trabajo habituales. | Redactados como servicios, sin clientes ni resultados. |

Se encontró en un directorio de terceros (RocketReach) una mención a «Preciso Comunicación Integral»; **no se incluyó** porque no es una fuente confiable.

### 5. Pendientes para ti

1. Confirmar o retirar el video de YouTube y la mención a ASEPRI.
2. Indicar tus perfiles de LinkedIn, X o YouTube para activar la lista «Sígueme».
3. Indicar URLs de otras entrevistas en televisión o radio (con el identificador de YouTube basta para incrustarlas).
4. Definir el dominio real y actualizar la URL canónica (ver README).
5. Escribir la primera columna propia en `contenido/publicaciones/`.
6. Confirmar fechas y URLs exactas de las publicaciones marcadas arriba; basta con editar su archivo `.md`.
