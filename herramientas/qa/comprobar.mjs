// Comprobaciones automáticas del sitio con Playwright.
// Requiere un servidor local: python3 -m http.server 8000 (desde la raíz del proyecto).
// Uso: node herramientas/qa/comprobar.mjs  (o PLAYWRIGHT_MODULE=/ruta/a/playwright/index.mjs node ...)
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000';
const out = [];
const log = (ok, msg) => { out.push((ok ? 'PASS ' : 'FAIL ') + msg); };
const b = await chromium.launch();
const pages = ['/', '/columnas/'];

// 1. Desbordamiento horizontal y errores de consola en 4 anchos
for (const w of [1440, 1024, 390, 360]) for (const p of pages) {
  const pg = await b.newPage({ viewport: { width: w, height: 800 } });
  const errs = []; pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => m.type()==='error' && errs.push(m.text()));
  const failed = []; pg.on('response', r => r.status() >= 400 && failed.push(r.status() + ' ' + r.url()));
  await pg.goto(BASE + p, { waitUntil: 'networkidle' });
  const ov = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  log(ov <= 0, `${w}px ${p}: sin scroll horizontal (exceso ${ov}px)`);
  log(!errs.length, `${w}px ${p}: sin errores JS ${errs.join(' | ')}`);
  log(!failed.length, `${w}px ${p}: recursos sin error ${failed.join(' | ')}`);
  await pg.close();
}

// 2. Enlaces internos, anclas y recursos
{
  const pg = await b.newPage();
  for (const p of pages) {
    await pg.goto(BASE + p);
    const info = await pg.evaluate(() => ({
      anchors: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h)),
      internal: [...new Set([...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin)).map(h => h.split('#')[0]))],
      imgsNoAlt: [...document.querySelectorAll('img:not([alt])')].length,
      ids: (() => { const s = {}; document.querySelectorAll('[id]').forEach(e => s[e.id] = (s[e.id]||0)+1); return Object.keys(s).filter(k => s[k] > 1); })(),
    }));
    log(!info.anchors.length, `${p}: anclas con destino ${info.anchors.join(',')}`);
    log(!info.imgsNoAlt, `${p}: imágenes con alt`);
    log(!info.ids.length, `${p}: ids únicos ${info.ids.join(',')}`);
    for (const u of info.internal) { const r = await pg.request.get(u); log(r.ok(), `${p}: enlace interno ${u.replace(BASE,'')} → ${r.status()}`); }
    // Fragmentos hacia la portada desde subpáginas
    const frags = await pg.evaluate(() => [...document.querySelectorAll('a[href*="index.html#"]')].map(a => a.hash));
    if (frags.length) { const home = await b.newPage(); await home.goto(BASE + '/'); for (const f of new Set(frags)) log(await home.$(f) !== null, `${p}: fragmento ${f} existe en portada`); await home.close(); }
  }
  for (const f of ['/feed.xml', '/sitemap.xml', '/favicon.svg', '/assets/og-martin-cabrera.jpg', '/assets/martin-cabrera-avatar.jpg']) { const r = await pg.request.get(BASE + f); log(r.ok(), `recurso ${f} → ${r.status()}`); }
  await pg.close();
}

// 3. Menú móvil
for (const w of [390, 360]) {
  const pg = await b.newPage({ viewport: { width: w, height: 800 } });
  await pg.goto(BASE + '/');
  const btn = pg.locator('.menu-toggle'); const nav = pg.locator('#navegacion');
  log(await btn.isVisible() && !(await nav.isVisible()), `${w}px: botón de menú visible y navegación cerrada`);
  await btn.click();
  log(await nav.isVisible() && await btn.getAttribute('aria-expanded') === 'true', `${w}px: el menú abre y aria-expanded=true`);
  log(await pg.evaluate(() => document.activeElement.closest('#navegacion') !== null), `${w}px: el foco pasa al primer enlace del menú`);
  await pg.keyboard.press('Escape');
  log(!(await nav.isVisible()) && await pg.evaluate(() => document.activeElement.classList.contains('menu-toggle')), `${w}px: Escape cierra y devuelve el foco al botón`);
  await btn.click(); await pg.locator('#navegacion a[href="#medios"]').click(); await pg.waitForTimeout(800);
  log(!(await nav.isVisible()), `${w}px: elegir un enlace cierra el menú`);
  const top = await pg.evaluate(() => document.querySelector('#medios').getBoundingClientRect().top);
  log(top >= 40 && top < 140, `${w}px: la sección destino no queda tapada por el encabezado fijo (top=${Math.round(top)})`);
  await btn.click(); await pg.mouse.click(w/2, 700);
  log(!(await nav.isVisible()), `${w}px: clic fuera cierra el menú`);
  await pg.setViewportSize({ width: 1200, height: 800 });
  log(await nav.isVisible() && !(await btn.isVisible()), `${w}px→1200px: navegación de escritorio visible`);
  await pg.close();
}
// Sin JavaScript: la navegación debe ser accesible
{
  const ctx = await b.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 800 } });
  const pg = await ctx.newPage(); await pg.goto(BASE + '/');
  log(await pg.locator('#navegacion').isVisible() && !(await pg.locator('.menu-toggle').isVisible()), '390px sin JS: navegación visible, botón oculto');
  await ctx.close();
}

// 4. Desplegables nativos y teclado
{
  const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await pg.goto(BASE + '/');
  const s2 = pg.locator('.service').nth(1);
  await s2.locator('summary').focus(); await pg.keyboard.press('Enter');
  log(await s2.evaluate(d => d.open), 'Enter abre el desplegable «Gestión pública y control»');
  await pg.keyboard.press('Space');
  log(!(await s2.evaluate(d => d.open)), 'Espacio lo cierra');
  await pg.goto(BASE + '/');
  await pg.keyboard.press('Tab');
  log(await pg.evaluate(() => document.activeElement.classList.contains('skip-link')), 'Primer Tab: enlace «Ir al contenido»');
  const sl = await pg.evaluate(() => document.activeElement.getBoundingClientRect().top);
  log(sl >= 0, 'El enlace de salto se ve al enfocarlo');
  await pg.keyboard.press('Enter');
  log(await pg.evaluate(() => document.activeElement.id === 'contenido'), 'El salto mueve el foco a <main>');
  const order = [];
  for (let i = 0; i < 60; i++) { await pg.keyboard.press('Tab'); order.push(await pg.evaluate(() => { const e = document.activeElement; if (e === document.body) return { t: 'fin del documento', outline: true }; const cs = getComputedStyle(e); return { t: (e.textContent||e.id||e.tagName).trim().slice(0,30), outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2 }; })); }
  log(order.every(o => o.outline), 'Todos los elementos enfocados muestran contorno de foco (' + order.filter(o => !o.outline).map(o => o.t).join(', ') + ')');
  await pg.close();
}

// 5. Zoom de texto 200 % (equivale a 720 px CSS en una pantalla de 1440)
for (const w of [720, 512]) {
  const pg = await b.newPage({ viewport: { width: w, height: 450 } });
  await pg.goto(BASE + '/');
  await pg.evaluate(() => document.documentElement.style.fontSize = '200%');
  const ov = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  log(ov <= 0, `Texto al 200 % en ${w}px: sin scroll horizontal (exceso ${ov}px)`);
  await pg.close();
}
{
  const pg = await b.newPage({ viewport: { width: 720, height: 450 }, deviceScaleFactor: 2 });
  await pg.goto(BASE + '/');
  const ov = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  log(ov <= 0, `Zoom de página 200 % (1440→720 CSS px): sin scroll horizontal`);
  await pg.close();
}

// 6. Formulario y copia
{
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const pg = await ctx.newPage();
  const msgs = []; pg.on('console', m => msgs.push(m.text()));
  await pg.goto(BASE + '/');
  await pg.locator('#contexto').fill('   ');
  await pg.locator('#consulta button[type=submit]').click();
  log(await pg.locator('#contexto').getAttribute('aria-invalid') === 'true' && await pg.locator('#contexto-error').isVisible(), 'Contexto solo con espacios: error visible y aria-invalid');
  log(await pg.evaluate(() => document.activeElement.id) === 'contexto', 'El foco vuelve al campo con error');
  log((await pg.locator('#form-status').textContent()) === '', 'Sin confirmación de envío cuando hay error');
  await pg.locator('#organizacion').fill('Gremio & Asociados «Ñandú»');
  await pg.selectOption('#tema', 'Arbitraje y controversias');
  await pg.locator('#contexto').fill('Necesito evaluar un arbitraje: ¿plazos? 100% & más\nSegunda línea.');
  log(await pg.locator('#contexto-error').isHidden(), 'El error desaparece al escribir');
  log((await pg.locator('[data-count]').textContent()) === String('Necesito evaluar un arbitraje: ¿plazos? 100% & más\nSegunda línea.'.length), 'Contador de caracteres actualizado');
  await pg.locator('#consulta button[type=submit]').click();
  await pg.waitForTimeout(800);
  const status = await pg.locator('#form-status').textContent();
  log(status.startsWith('Consulta preparada') && !/enviad/i.test(status), 'Mensaje: «Consulta preparada», sin afirmar envío');
  // Copiar correo sin permisos de portapapeles → alternativa visible
  await pg.locator('[data-copy-email]').click();
  await pg.waitForTimeout(1800);
  const cs = await pg.locator('#copy-status').textContent();
  log(cs.includes('martin@cabrera.pe'), 'Copiar correo: confirmación o alternativa visible → «' + cs + '»');
  await ctx.close();
  const ctx2 = await b.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
  const pg2 = await ctx2.newPage(); await pg2.goto(BASE + '/');
  await pg2.locator('[data-copy-email]').click();
  log(await pg2.evaluate(() => navigator.clipboard.readText()) === 'martin@cabrera.pe' && (await pg2.locator('#copy-status').textContent()) === 'Correo copiado.', 'Copiar correo con permiso: copia y confirma');
  await ctx2.close();
}

// 7. Video: no se conecta a YouTube hasta pulsar
{
  const pg = await b.newPage();
  const yt = []; pg.on('request', r => /youtube/.test(r.url()) && yt.push(r.url()));
  await pg.route(/youtube/, r => r.abort());
  await pg.goto(BASE + '/', { waitUntil: 'networkidle' });
  log(yt.length === 0, 'Sin solicitudes a YouTube al cargar la página');
  await pg.locator('[data-youtube] .video-poster').click();
  const src = await pg.locator('[data-youtube] iframe').getAttribute('src');
  log(src.startsWith('https://www.youtube-nocookie.com/embed/Gtj2sfF3A3Y'), 'Al pulsar se inserta el reproductor (youtube-nocookie)');
  await pg.close();
}
// 8. Movimiento reducido
{
  const ctx = await b.newContext({ reducedMotion: 'reduce' }); const pg = await ctx.newPage(); await pg.goto(BASE + '/');
  log(await pg.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior) === 'auto', 'prefers-reduced-motion: desplazamiento sin animación');
  await ctx.close();
}
await b.close();
console.log(out.join('\n'));
console.log('\nTOTAL', out.filter(l => l.startsWith('PASS')).length, 'PASS /', out.filter(l => l.startsWith('FAIL')).length, 'FAIL');
