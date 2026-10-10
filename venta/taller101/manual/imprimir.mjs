import pkg from '/opt/node-tools/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const p = await b.newPage();
await p.goto('file://' + process.cwd() + '/manual-imagen-taller101.html',
             { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: 'manual-imagen-taller101.pdf', format: 'A4',
              printBackground: true,
              margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await b.close();
console.log('pdf listo');
