# Guía del repositorio de publicaciones

El sitio es el repositorio oficial de tus columnas, entrevistas, declaraciones y opiniones. Cada pieza tiene una página permanente en `publicaciones/`, aunque se haya publicado primero en otro medio. El archivo `publicaciones/index.html` las reúne por año y se puede filtrar por tipo.

## Agregar una publicación

1. Copia `contenido/publicaciones/_plantilla.md` con un nombre nuevo sin guion bajo, por ejemplo `2026-10-12-reforma-del-reglamento.md`.
2. Completa la cabecera y, si corresponde, el texto.
3. Ejecuta `python3 herramientas/publicar.py`.
4. Sube los archivos al alojamiento.

## Cabecera

```text
---
titulo: El Congreso y la agenda corta
tipo: columna
fecha: 2026-10-12
medio: El Comercio
url_original: https://elcomercio.pe/...
resumen: Una o dos líneas con la tesis.
etiquetas: Congreso, Agenda legislativa
estado: publicado
---
```

| Campo | Uso |
| --- | --- |
| `titulo` | Obligatorio. |
| `tipo` | `columna`, `entrevista`, `declaracion` u `opinion`. Define la etiqueta de color y el filtro. |
| `fecha` | `AAAA-MM-DD`. Si no se conoce el día, `AAAA-MM` o `AAAA`. Vacía: se agrupa en «Sin fecha confirmada». |
| `medio`, `programa` | Dónde salió (El Comercio · Cara y Sello; Perú21 TV · La voz del 21). Vacío: «Este sitio». |
| `url_original` | Enlace al medio. Sin texto propio, la página muestra el resumen y un botón «Leer en…» o «Ver en…». |
| `nota_medio` | Texto breve, por ejemplo «Reproducida en Lampadia». |
| `video_youtube` | Identificador del video (lo que va después de `v=`). El video se reproduce en tu página; antes de pulsar no hay conexión con YouTube. |
| `cita` | Frase textual destacada. En entrevistas aparece sobre el reproductor. |
| `resumen`, `etiquetas` | Bajada, descripción para buscadores y RSS; etiquetas separadas por comas. |
| `estado` | `publicado` o `borrador`. |
| `slug` | Opcional: dirección de la página. Si falta, se deriva del título. |

## Texto

Si tienes derechos para reproducir la columna, pega el texto debajo de la cabecera; la página la mostrará completa, con la nota «Publicada originalmente en…». Markdown admitido: párrafos separados por línea en blanco, `## Subtítulo`, `### Subtítulo menor`, `**negrita**`, `*cursiva*`, `[texto](https://enlace)`, citas con `>`, listas con `-` o `1.`, separador `---`.

## Comandos

```sh
python3 herramientas/publicar.py               # publica
python3 herramientas/publicar.py --borradores  # además, vista previa de borradores y programadas
```

La vista previa queda en `publicaciones/_vista-previa/` con aviso de borrador y `noindex`; está en `.gitignore` y `robots.txt`, no la subas.

El script también actualiza la portada (cuatro últimas columnas, cinco últimas opiniones o declaraciones y cuatro últimas entrevistas), el RSS (`feed.xml`), `sitemap.xml` y `robots.txt`. Si hay un error en una cabecera no publica nada e indica qué corregir. Una fecha completa futura deja la publicación programada hasta que el script se ejecute desde ese día.

## Ritmo semanal o diario

No hay límite de frecuencia. Para una columna semanal conviene fijar un día y dejarla programada; para opiniones diarias breves usa `tipo: opinion` con textos de 300 a 500 palabras.

## Publicación automática (pendiente)

Hoy hay que ejecutar el script y subir los archivos. Si el sitio se aloja en un servicio con integración de Git (GitHub Pages, Netlify, Cloudflare Pages), el script puede correr en cada cambio. No se configuró porque requiere decidir el alojamiento.
