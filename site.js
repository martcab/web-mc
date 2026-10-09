'use strict';
/* Martín Cabrera Marchán — comportamiento del sitio.
   Sin dependencias. Cada bloque comprueba que sus elementos existan,
   porque este archivo también se usa en las páginas de columnas. */

const EMAIL = 'martin@cabrera.pe';
const MOBILE_QUERY = window.matchMedia('(max-width: 760px)');

/* Menú móvil ------------------------------------------------------------ */
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navegacion');

if (menuButton && navigation) {
  const isOpen = () => menuButton.getAttribute('aria-expanded') === 'true';
  const setMenu = open => {
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  };

  menuButton.addEventListener('click', () => {
    const willOpen = !isOpen();
    setMenu(willOpen);
    if (willOpen) navigation.querySelector('a')?.focus();
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && isOpen()) {
      setMenu(false);
      menuButton.focus();
    }
  });
  // Cierra el menú al hacer clic fuera de él o al salir del menú con el teclado.
  document.addEventListener('click', event => {
    if (isOpen() && !navigation.contains(event.target) && !menuButton.contains(event.target)) setMenu(false);
  });
  navigation.addEventListener('focusout', event => {
    if (isOpen() && MOBILE_QUERY.matches && event.relatedTarget && !navigation.contains(event.relatedTarget) && event.relatedTarget !== menuButton) setMenu(false);
  });
  // Al pasar a escritorio, el estado del menú móvil deja de aplicar.
  MOBILE_QUERY.addEventListener('change', event => { if (!event.matches) setMenu(false); });
}

/* Copiar correo --------------------------------------------------------- */
const copyButton = document.querySelector('[data-copy-email]');
const copyStatus = document.querySelector('#copy-status');

if (copyButton && copyStatus) {
  copyButton.addEventListener('click', async () => {
    copyStatus.textContent = '';
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error('Portapapeles no disponible');
      // Algunos navegadores tardan en rechazar el permiso; no se espera más de 1,5 s.
      await Promise.race([
        navigator.clipboard.writeText(EMAIL),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Tiempo agotado')), 1500)),
      ]);
      copyStatus.textContent = 'Correo copiado.';
    } catch {
      // Alternativa visible: el texto queda seleccionado para copiarlo a mano.
      copyStatus.textContent = 'No se pudo copiar automáticamente. Selecciona y copia: ';
      const fallback = document.createElement('span');
      fallback.className = 'copy-fallback';
      fallback.textContent = EMAIL;
      copyStatus.append(fallback);
      const range = document.createRange();
      range.selectNodeContents(fallback);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }
  });
}

/* Formulario: prepara un correo (mailto). No envía ni almacena datos. ---- */
const form = document.querySelector('#consulta');

if (form) {
  const topic = form.querySelector('#tema');
  const organization = form.querySelector('#organizacion');
  const context = form.querySelector('#contexto');
  const error = form.querySelector('#contexto-error');
  const counter = form.querySelector('[data-count]');
  const status = form.querySelector('#form-status');

  const setError = show => {
    error.hidden = !show;
    if (show) context.setAttribute('aria-invalid', 'true');
    else context.removeAttribute('aria-invalid');
  };

  context.addEventListener('input', () => {
    if (counter) counter.textContent = String(context.value.length);
    if (context.value.trim()) setError(false);
  });

  form.addEventListener('submit', event => {
    event.preventDefault();
    const text = context.value.trim();
    if (!text) {
      setError(true);
      status.textContent = '';
      context.focus();
      return;
    }
    setError(false);
    const org = organization.value.trim();
    const body = 'Hola, Martín:\n\n'
      + (org ? 'Nombre u organización: ' + org + '\n\n' : '')
      + 'Tema: ' + topic.value + '\n\n'
      + text
      + '\n\nQuedo atento para conversar.\n';
    const href = 'mailto:' + EMAIL
      + '?subject=' + encodeURIComponent('Consulta: ' + topic.value)
      + '&body=' + encodeURIComponent(body.replace(/\n/g, '\r\n')); // RFC 6068: saltos de línea CRLF
    status.textContent = 'Consulta preparada. Revisa y envía el mensaje desde tu aplicación de correo. Si no se abre, escribe directamente a ' + EMAIL + '.';
    window.location.href = href;
  });
}

/* Videos: el reproductor de YouTube se carga solo al pulsar --------------
   Hasta entonces no se conecta con YouTube (privacidad y velocidad). */
document.querySelectorAll('[data-youtube]').forEach(frame => {
  const poster = frame.querySelector('.video-poster');
  if (!poster) return;
  poster.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey) return; // permite abrir en otra pestaña
    event.preventDefault();
    const iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(frame.dataset.youtube) + '?autoplay=1&rel=0';
    iframe.title = frame.dataset.title || 'Video';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    poster.replaceWith(iframe);
    iframe.focus();
  });
});
