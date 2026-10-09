# Sitio de Martin Cabrera Marchán — reglas del proyecto

Reglas confirmadas por el titular. Respétalas en cualquier cambio.

## Identidad

- El nombre se escribe **Martin**, sin tilde en la «i»: «Martin Cabrera Marchán». Nunca «Martín». La regla es solo para su nombre: nombres propios de terceros conservan su tilde (por ejemplo, «Universidad de San Martín de Porres»).
- Lema de la portada: **«Criterio jurídico. Lectura política. Estrategia aplicada.»**
- Orden de la profesión: «Abogado · Árbitro · Consultor».
- Correo de contacto: `martin@cabrera.pe`. Dominio: `https://cabrera.pe/`.
- Redes: LinkedIn `linkedin.com/in/martcab`, X `@martcab`, Instagram `martcab`, Facebook `martcab`, TikTok `@martcab9`.
- Gerencia general de ASEPRI: confirmada para mostrarse.

## Contenido

- No inventar cargos, clientes, cifras, reconocimientos, publicaciones ni fechas. Si un dato no está verificado, se deja sin fecha o se pregunta.
- Publicaciones (columnas, entrevistas, declaraciones, opiniones): un archivo por pieza en `contenido/publicaciones/`; las páginas se generan con `python3 herramientas/publicar.py`. No editar a mano los bloques generados de `index.html` ni la carpeta `publicaciones/`.
- Tono formal, claro y directo; sin lenguaje genérico de marketing.

## Diseño y técnica

- Diseño elegido: estructura «Tribuna» (propuesta A) con los colores de «Despacho» (B). Fondo blanco, tinta `#15191E`, azul IPOC `#1F4E79` para bloques y botones, amarillo `#F2B705` solo como resaltador bajo el texto y en filetes (nunca texto amarillo sobre blanco), rojo sangre `#8E1B1B` en antetítulos, gris `#595959` en texto secundario; una sola banda oscura (Enfoque). Titulares en mayúsculas, Archivo condensada y extranegrita; texto en Public Sans. Fuentes en `assets/fonts/`.
- Retratos: los de estudio en `assets/originales/`; no generar ni alterar el rostro.
- HTML, CSS y JavaScript nativos; sin frameworks ni dependencias. El formulario solo prepara un `mailto:`.
- Publicación: GitHub Pages desde la rama `main` (`.github/workflows/publicar.yml`). Antes de subir, ejecutar `herramientas/qa/comprobar.mjs`.
