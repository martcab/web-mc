# Guía de la columna

## Formato del archivo

Cada columna es un archivo de texto en `contenido/columnas/`, con una cabecera entre dos líneas `---`:

```text
---
titulo: El Congreso y la agenda corta
fecha: 2026-10-12
resumen: Una o dos líneas con la tesis.
etiquetas: Congreso, Agenda legislativa
estado: borrador
---
Primer párrafo…
```

| Campo | Obligatorio | Uso |
| --- | --- | --- |
| `titulo` | Sí | Título de la página, de la portada y del RSS. |
| `fecha` | Sí | Formato `AAAA-MM-DD`. Ordena las columnas y define si está programada. |
| `resumen` | Recomendado | Bajada bajo el título; también descripción para buscadores y redes. |
| `etiquetas` | No | Separadas por comas. |
| `estado` | Sí | `borrador` o `publicado`. |
| `slug` | No | Dirección de la página. Si falta, se deriva del título. |
| `medio_original`, `url_original` | No | Para una columna que salió primero en un medio: añade «Publicada originalmente en…». Reproduce el texto completo solo si el medio lo permite. |

Los archivos cuyo nombre empieza con `_` nunca se publican.

## Markdown admitido

- Párrafos separados por una línea en blanco.
- `## Subtítulo` y `### Subtítulo menor`.
- `**negrita**`, `*cursiva*`, `[texto](https://enlace)`.
- Citas: líneas que empiezan con `>`.
- Listas con `-` o `1.`.
- Separador: una línea con `---` dentro del texto.

## Comandos

```sh
python3 herramientas/publicar.py               # publica
python3 herramientas/publicar.py --borradores  # además, vista previa de borradores y programadas
```

La vista previa queda en `columnas/_vista-previa/`, con aviso de borrador y `noindex`. Esa carpeta está en `.gitignore` y en `robots.txt`; no la subas al alojamiento.

Si hay un error en la cabecera, el script no publica nada e indica qué corregir.

## Ritmo semanal o diario

El sistema no limita la frecuencia. Para una columna semanal, conviene escribir con fecha fija (por ejemplo, el lunes) y dejarla programada; para notas diarias breves, el mismo formato funciona con textos de 300 a 500 palabras. La portada muestra las tres más recientes y el archivo las agrupa por año.

## Publicación automática (opcional, pendiente)

Hoy hay que ejecutar el script y subir los archivos. Si más adelante el sitio se aloja en un servicio con integración de Git (por ejemplo, GitHub Pages, Netlify o Cloudflare Pages), se puede ejecutar el script en cada cambio para publicar con solo guardar el archivo `.md`. No se configuró porque requiere decidir el alojamiento.
