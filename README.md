# Martín Cabrera — proyecto portátil

Exportación del sitio personal desarrollado el 6 de octubre de 2026.

Referencia alojada: https://martin-cabrera-estrategia.martcab.chatgpt.site

## Retomarlo en Claude Code

1. Descomprime `proyecto_martin_cabrera.zip`.
2. Abre la carpeta `martin-cabrera` como carpeta de trabajo de Claude Code.
3. Copia el texto de `PROMPT_CLAUDE_CODE.md` en la conversación, o indica: «Lee PROMPT_CLAUDE_CODE.md y ejecuta sus instrucciones».

## Archivos

| Archivo | Función |
| --- | --- |
| `index.html` | Estructura, contenido y metadatos de la página. |
| `styles.css` | Diseño, colores y adaptación a distintos tamaños de pantalla. |
| `site.js` | Menú móvil, copia del correo y preparación de consultas. |
| `favicon.svg` | Icono del sitio con el monograma MC. |
| `assets/martin-cabrera.jpg` | Fotografía utilizada en la versión alojada. |
| `martin_cabrera_autonomo.html` | Copia completa en un archivo: incluye estilos, JavaScript, fotografía y favicon. |
| `PROMPT_CLAUDE_CODE.md` | Contexto e instrucciones para continuar el proyecto. |
| `SOURCE_MANIFEST.json` | Procedencia y huellas SHA-256 de los archivos originales exportados. |

## Abrirlo

La versión `martin_cabrera_autonomo.html` puede abrirse directamente en un navegador. No necesita descargar fuentes, bibliotecas ni imágenes. Para trabajar con los archivos separados, usa un servidor estático desde esta carpeta, porque sus rutas de recursos empiezan en `/`.

Si tienes Python 3:

```sh
python3 -m http.server 8000
```

Abre `http://localhost:8000`. Si el puerto está ocupado, utiliza otro puerto libre. No se necesitan Node.js, instalación de paquetes ni compilación. El portapapeles depende de los permisos y del contexto del navegador; existe una alternativa visible si no está disponible.

## Contacto y datos

El formulario prepara un enlace `mailto:` dirigido a `martin@cabrera.pe`. El usuario revisa y envía el mensaje desde su aplicación de correo. No existe envío automático, backend, almacenamiento de consultas, analítica ni autenticación propia.

El acceso privado de la versión alojada depende del proveedor original, no de estos archivos. Para un nuevo alojamiento, configura allí la audiencia que corresponda. Actualiza `canonical` y `og:url` en `index.html` al nuevo dominio real antes de publicar; si utilizas la versión autónoma, actualízalos también en ella.

Esta exportación conserva el código del sitio, sus estilos y recursos. No incluye historial Git, credenciales ni configuración interna de la plataforma original. El sitio alojado no ha sido modificado por la exportación.

## Comprobaciones de esta entrega

Se verificaron integridad del ZIP, correspondencia de los archivos exportados con los originales, anclas, etiquetas del formulario, existencia de recursos, sintaxis de JavaScript y recursos incrustados de la versión autónoma. No se ejecutó una revisión visual en navegador en esta exportación; el prompt solicita hacerla al retomar el trabajo si el entorno lo permite.
