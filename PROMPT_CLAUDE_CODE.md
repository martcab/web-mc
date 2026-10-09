# Prompt para continuar el sitio de Martin Cabrera en Claude Code

Actúa como desarrollador web senior y diseñador editorial. Quiero que retomes un sitio personal que ya fue diseñado y desarrollado. Trabaja sobre el código adjunto: conserva la identidad y reproduce primero la versión existente antes de proponer cambios.

## Material de partida

El paquete `proyecto_martin_cabrera.zip` contiene una carpeta `martin-cabrera` con el código real: `index.html`, `styles.css`, `site.js`, `favicon.svg`, `assets/martin-cabrera.jpg`, instrucciones y este prompt. Si la carpeta ya está extraída, trabaja directamente en ella. La versión `martin_cabrera_autonomo.html` reúne el mismo sitio y sus recursos en un solo archivo y sirve para revisarlo sin instalación. Usa los archivos separados para mantenerlo.

Referencia alojada: https://martin-cabrera-estrategia.martcab.chatgpt.site. Tiene acceso privado; si no puedes verla, utiliza los archivos como fuente de verdad y continúa. No necesitas recuperar código del sitio alojado.

## Contexto y objetivo

Soy Martin Cabrera Marchán, abogado, consultor y árbitro peruano, natural de Tumbes y radicado en Lima. Soy socio fundador de IPOC Consultores. Mi experiencia incluye asesoría parlamentaria en el Congreso, asesoría y relaciones interinstitucionales en la Contraloría General, y asesoría en la Defensoría del Pueblo.

El sitio debe posicionarme ante empresas, gremios e instituciones como un profesional que integra criterio jurídico, lectura política y estrategia pública, y facilitar consultas profesionales. Mantén el tono formal, claro, analítico y natural; evita grandilocuencia y lenguaje genérico de marketing.

Preserva el contenido actual. No inventes cargos vigentes, clientes, reconocimientos, testimonios, publicaciones, cifras de experiencia, resultados ni grados académicos. No incorpores información familiar o datos personales ajenos al propósito profesional. Mi correo de contacto es `martin@cabrera.pe`.

## Identidad visual y estructura

Mantén el diseño editorial sobrio: azul profundo `#102735`, azul oscuro `#0b1e29`, blanco, gris claro `#f5f7f8` y cobre `#d1a580`, con cobre oscuro `#845638` para texto sobre fondos claros. Titulares serif con Georgia y cuerpo sans serif con Arial/Helvetica; amplios espacios, líneas finas, esquinas discretas y contraste legible. Conserva mi fotografía real y el monograma MC. No sustituyas mi rostro con una imagen generada.

Conserva la página única y sus secciones:

1. Inicio: «Criterio jurídico. Lectura política. Estrategia aplicada.», fotografía, presentación y llamada a conversar.
2. Especialidades desplegables: asuntos parlamentarios; gestión pública y control; relaciones interinstitucionales; arbitraje y controversias.
3. Trayectoria: biografía, formación y experiencia institucional, sin implicar respaldo de las entidades mencionadas.
4. Enfoque de IPOC: instituciones, política y comunicaciones.
5. Contacto: correo profesional y preparación de una consulta.

## Comportamiento y alcance técnico

El proyecto es HTML, CSS y JavaScript nativos, sin dependencias, servidor de aplicación ni base de datos. Mantén esa sencillez. No migres a React, Next.js u otro framework salvo que yo lo solicite posteriormente.

Preserva la navegación por anclas, menú móvil accesible, desplegables nativos, botón para copiar el correo y formulario que prepara un enlace `mailto:`. El visitante revisa y envía el mensaje en su propia aplicación de correo. La página no envía mensajes por sí sola ni almacena los datos: no muestres una confirmación de envío. Mantén validación, codificación de caracteres y alternativa cuando falle el portapapeles.

El acceso privado del alojamiento original es una función de esa plataforma; el código exportado no incluye autenticación propia. El paquete tampoco contiene credenciales ni configuración interna del alojamiento original.

## Trabajo que debes ejecutar ahora

1. Lee `README.md` y los archivos existentes; identifica su estructura sin rehacer el proyecto.
2. Inicia una vista local usando un servidor estático disponible y comunícame cómo abrirla.
3. Comprueba recursos, enlaces, JavaScript y funciones. Si dispones de navegador, revisa escritorio de 1440 y 1024 píxeles, móviles de 390 y 360 píxeles, navegación por teclado y ampliación de texto al 200 %. Corrige defectos reproducibles conservando el diseño.
4. Mantén español peruano (`es-PE`), metadatos, favicon, textos alternativos, estados de foco y preferencia de movimiento reducido. Cuando defina un nuevo dominio, actualiza la URL canónica y `og:url` a ese dominio real.
5. Deja el proyecto funcionando localmente y listo para alojarse como sitio estático. Documenta los cambios y las comprobaciones realizadas; distingue las que realmente ejecutaste de las que quedaron pendientes.

No cambies el sitio original alojado ni publiques esta copia automáticamente. En esta primera etapa, retoma el proyecto local y entrégame una base fiel y editable. No añadas blog, panel legislativo, analítica, bases de datos ni servicios externos sin una instrucción posterior.
