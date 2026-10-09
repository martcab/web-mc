---
titulo: Título de la columna
fecha: 2026-10-12
resumen: Una o dos líneas que resumen la tesis. Aparece bajo el título, en la portada, en el archivo y en el RSS.
etiquetas: Congreso, Gestión pública
estado: borrador
# Opcionales:
# slug: titulo-corto-para-la-direccion
# medio_original: El Comercio
# url_original: https://elcomercio.pe/...
---
Esta es la plantilla de la columna. Cópiala con un nombre nuevo, por ejemplo `2026-10-12-titulo-corto.md`, sin el guion bajo inicial. Los archivos que empiezan con guion bajo nunca se publican.

El primer párrafo abre con letra capitular. Conviene que entre directo al punto: la hipótesis primero, el contexto después.

## Subtítulo de sección

Los párrafos se separan con una línea en blanco. Se admiten **negritas**, *cursivas* y [enlaces](https://example.com).

> Una cita destacada se escribe empezando la línea con el signo «mayor que».

- Las listas usan guiones.
- Cada elemento va en su propia línea.

1. También se admiten listas numeradas.
2. Útiles para escenarios o pasos.

### Para publicar

Cambia `estado: borrador` por `estado: publicado` y ejecuta `python3 herramientas/publicar.py`. Si la fecha es futura, la columna queda programada y se publica la primera vez que ejecutes el script desde ese día.
