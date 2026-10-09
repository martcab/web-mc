// Comprobaciones automáticas del sitio con Playwright.
// Requiere un servidor local: python3 -m http.server 8000 (desde la raíz del proyecto).
// Uso: node herramientas/qa/mailto.mjs  (o PLAYWRIGHT_MODULE=/ruta/a/playwright/index.mjs node ...)
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const b = await chromium.launch(); const pg = await b.newPage();
const cdp = await pg.context().newCDPSession(pg); await cdp.send('Page.enable');
let url = null; cdp.on('Page.frameRequestedNavigation', e => url = e.url);
await pg.goto((process.env.BASE_URL || 'http://localhost:8000') + '/');
await pg.locator('#organizacion').fill('Gremio & Asociados «Ñandú»');
await pg.selectOption('#tema', 'Arbitraje y controversias');
const txt = 'Necesito evaluar: ¿plazos? 100% & más #1 +\nSegunda línea.';
await pg.locator('#contexto').fill(txt);
await pg.locator('#consulta button[type=submit]').click(); await pg.waitForTimeout(800);
console.log(url);
const u = new URL(url); const body = u.searchParams.get('body');
console.log('para:', u.pathname, '| asunto:', u.searchParams.get('subject'));
console.log('cuerpo íntegro:', body.includes(txt.replace(/\n/g, '\r\n')) && body.includes('Gremio & Asociados «Ñandú»'), '| largo URL:', url.length);
await pg.locator('#contexto').fill('x'.repeat(2000)); console.log('maxlength aplicado:', (await pg.locator('#contexto').inputValue()).length);
await b.close();
