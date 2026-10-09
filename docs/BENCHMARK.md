# Benchmark y propuesta de diseño

## Alcance y método

Se revisaron patrones de sitios personales y páginas de autor de referencia para profesionales que combinan práctica profesional y opinión pública. **Limitación:** desde el entorno de trabajo no fue posible abrir esos sitios en vivo (el proxy de red bloquea la navegación general), de modo que el análisis se basa en el conocimiento de su estructura conocida y no en una auditoría actual. Antes de copiar un detalle concreto, conviene volver a mirarlos.

## Referencias

| Referencia | Qué hace bien | Qué se tomó para este sitio |
| --- | --- | --- |
| **Stratechery** (Ben Thompson) | La columna es el producto: cadencia fija, archivo ordenado, suscripción visible. | Las publicaciones como sección propia con archivo, RSS y las últimas entregas en portada. |
| **Paul Graham — Essays** | Texto primero, sin ruido; un índice simple de ensayos. | Archivo de columnas como lista sobria agrupada por año. |
| **Seth Godin — blog** | Publicación diaria y breve; el formato no castiga la frecuencia. | El sistema admite cadencia semanal o diaria con el mismo archivo `.md`. |
| **Craig Mod** | Tipografía editorial, márgenes amplios, medida de línea cómoda. | Páginas de publicación con medida de lectura cómoda (~70 caracteres), capitular y cita destacada. |
| **Páginas de expertos de think tanks** (Brookings, CSIS, Wilson Center) | Biografía, áreas de especialidad, publicaciones y «en los medios» en una sola página. | Estructura: especialidades → trayectoria → enfoque → columna → en medios → contacto. |
| **Páginas de autor de diarios** (El País, The Atlantic) | Firma con foto, bajada, fecha y tiempo de lectura; bloque de autor al final. | Metadatos de columna (fecha, tiempo de lectura, etiquetas) y recuadro de autor con retrato. |
| **Perfiles de socios en firmas de abogados** | Áreas de práctica con alcance concreto, sin adjetivos. | Especialidades desplegables con entregables reales (ayudas memoria, cuadros comparativos, mapas de actores). |
| **Substack / Ghost** | Captación de suscriptores por correo. | **No se adoptó**: requiere un servicio externo. Se ofrece RSS; un boletín queda como decisión futura. |

## Decisiones de diseño

> Revisión 2 (9 de octubre de 2026): a pedido tuyo se reemplazó la paleta azul profundo, blanco y cobre por una afín a IPOC Consultores, y Georgia/Arial por Archivo y Public Sans.

### Paleta afín a IPOC

El azul `#1F4E79`, el azul claro `#D6E4F0`, el gris `#595959` y el fondo `#F5F8FC` son los de las plantillas de documentos de IPOC. Negro, amarillo y rojo sangre se añadieron como acentos, según tu indicación.

| Token | Valor | Uso | Contraste |
| --- | --- | --- | --- |
| `--black` | `#101215` | Encabezado, portada, «En medios», pie, cabecera de publicaciones. | Blanco 18,9:1 |
| `--blue` | `#1F4E79` | Sección Enfoque, etiquetas de áreas, subtítulos destacados, etiqueta «Columna». | Sobre blanco 8,7:1 |
| `--grey` | `#595959` | Texto secundario. | Sobre blanco 7,0:1 |
| `--yellow` | `#F2B705` | Acento sobre negro y azul: lema, botón principal, marco del retrato. Nunca como texto sobre blanco. | Sobre negro 10,3:1; sobre azul 4,8:1 |
| `--blood` | `#8E1B1B` | Acento sobre fondos claros: antetítulos, enlaces, foco, etiqueta «Entrevista». | Sobre blanco 9,0:1 |
| `--paper` / `--blue-pale` | `#F5F8FC` / `#D6E4F0` | Fondos de trayectoria y formulario; etiqueta «Declaración». | — |

Detalle de identidad: una franja superior azul, amarillo y rojo en el encabezado, que se repite en el favicon y en la imagen para redes.

Ritmo de secciones: negro (inicio) → blanco (especialidades) → gris azulado (trayectoria) → azul IPOC (enfoque) → blanco (publicaciones) → negro (en medios) → blanco (contacto).

### Tipografía

- **Archivo** (titulares, extra negrita y algo condensada): voz firme, de titular de prensa, pensada para lectura en pantalla.
- **Public Sans** (texto): diseñada para el sistema de diseño del gobierno de Estados Unidos; neutra y muy legible, coherente con un sitio sobre asuntos públicos.

Ambas tienen licencia libre (OFL) y se alojan en `assets/fonts/` (unos 145 KB en total), sin depender de servicios externos. Si alguna no carga, el navegador usa Arial.

### Fotografía

Se usan tus retratos de estudio (fondo gris, terno azul), que encajan con la paleta: el azul del terno conversa con el azul IPOC y el fondo gris con el gris de la marca. Brazos cruzados en la portada y en la imagen para redes, manos juntas en Trayectoria y el primer plano como firma de las publicaciones. Los originales se conservan sin cambios en `assets/originales/`.

### Cambios por sección

1. **Encabezado fijo** con dos entradas nuevas: Publicaciones y En medios.
2. **Inicio**: orden «Abogado · Árbitro · Consultor», etiquetas con las cuatro áreas, segunda franja «Opinión publicada en: El Comercio · Lampadia · Perú21 TV».
3. **Especialidades**: se añadieron entregables que forman parte de tu práctica (ayudas memoria de proyectos de ley, cuadros comparativos de textos normativos, correlación de fuerzas, planes de incidencia, comunicaciones formales ante autoridades).
4. **Trayectoria**: se añadieron ASEPRI y la condición de columnista en El Comercio, y una nota de que la mención de entidades no implica respaldo.
5. **Publicaciones** (nueva): repositorio oficial de columnas, entrevistas, declaraciones y opiniones; cada una con su página, archivo por año, filtros por tipo y RSS.
6. **En medios** (nueva): entrevistas con video que carga al pulsar y enlaces a perfiles.
7. **Contacto**: validación accesible, contador de caracteres y texto que aclara que la página no envía ni almacena datos.

## Capturas

| Antes | Después |
| --- | --- |
| ![Antes, escritorio](capturas/antes-escritorio.jpg) | ![Después, escritorio](capturas/despues-escritorio.jpg) |
| ![Antes, móvil](capturas/antes-movil.jpg) | ![Después, móvil](capturas/despues-movil.jpg) |

Página completa: [antes](capturas/antes-pagina-completa.jpg) · [después](capturas/despues-pagina-completa.jpg) · [archivo de publicaciones](capturas/publicaciones-archivo.jpg) · [página de una entrevista](capturas/publicacion-entrevista.jpg).
