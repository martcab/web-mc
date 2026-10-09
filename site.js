'use strict';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navegacion');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menuButton.addEventListener('click', () => {
  const willOpen = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(willOpen));
  navigation.classList.toggle('is-open', willOpen);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
document.querySelector('[data-copy-email]').addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText('martin@cabrera.pe');
    status.textContent = 'Correo copiado.';
  } catch {
    status.textContent = 'Puedes seleccionar y copiar martin@cabrera.pe.';
  }
});
document.querySelector('#consulta').addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const topic = document.querySelector('#tema').value;
  const organization = document.querySelector('#organizacion').value.trim();
  const context = document.querySelector('#contexto').value.trim();
  if (!context) {
    document.querySelector('#contexto').setCustomValidity('Describe brevemente el contexto.');
    form.reportValidity();
    return;
  }
  const body = 'Hola, Martín:\n\n' + (organization ? 'Nombre u organización: ' + organization + '\n\n' : '') + 'Tema: ' + topic + '\n\n' + context + '\n\nQuedo atento para conversar.\n';
  document.querySelector('#form-status').textContent = 'Consulta preparada. Revisa y envía el mensaje desde tu aplicación de correo. Si no se abre, escribe directamente a martin@cabrera.pe.';
  window.location.href = 'mailto:martin@cabrera.pe?subject=' + encodeURIComponent('Consulta: ' + topic) + '&body=' + encodeURIComponent(body);
});
document.querySelector('#contexto').addEventListener('input', event => event.target.setCustomValidity(''));
