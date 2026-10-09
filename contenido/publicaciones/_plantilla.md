---
titulo: Título de la publicación
tipo: columna
fecha: 2026-10-12
resumen: Una o dos líneas con la tesis o el tema. Aparece bajo el título, en la portada, en el archivo y en el RSS.
etiquetas: Congreso, Gestión pública
estado: borrador
# tipo: columna | entrevista | declaracion | opinion
# fecha: AAAA-MM-DD; si no se conoce el día, AAAA-MM o AAAA; vacía si no hay fecha confirmada.
# Opcionales:
# medio: El Comercio                  (vacío = publicada primero en este sitio)
# programa: La voz del 21              (sección o programa del medio)
# url_original: https://...            (enlace al medio original)
# nota_medio: Reproducida en Lampadia.
# video_youtube: Gtj2sfF3A3Y           (identificador del video: se reproduce en la página)
# cita: Frase textual destacada.
# slug: titulo-corto-para-la-direccion
---
Esta es la plantilla de publicaciones. Cópiala con un nombre nuevo, por ejemplo `2026-10-12-titulo-corto.md`, sin el guion bajo inicial. Los archivos que empiezan con guion bajo nunca se publican.

Si la publicación salió en un medio y no vas a reproducir el texto, deja el cuerpo vacío: la página mostrará el resumen y el enlace al original. Si tienes derechos para reproducirlo, pega aquí el texto completo.

## Subtítulo de sección

Los párrafos se separan con una línea en blanco. Se admiten **negritas**, *cursivas* y [enlaces](https://example.com).

> Una cita destacada empieza la línea con el signo «mayor que».

- Las listas usan guiones.
- Cada elemento va en su propia línea.

### Para publicar

Cambia `estado: borrador` por `estado: publicado` y ejecuta `python3 herramientas/publicar.py`.
