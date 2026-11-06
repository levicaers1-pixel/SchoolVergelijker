// Rooktest: npm i playwright && python3 app/maak_preview.py && node tests/smoke.js
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const width of [1100, 400]) {
    const p = await b.newPage({viewport: {width, height: 900}});
    const fouten = [];
    p.on('pageerror', (e) => fouten.push(e.message));
    await p.goto('file://' + path.resolve(__dirname, '../app/preview.html'));
    const q = (f) => p.evaluate(f);
    if (await q(() => document.querySelectorAll('.bs-pin').length) < 200) fouten.push('te weinig punten op de kaart');
    await p.fill('#zoek', 'Diksmuidelaan');
    await p.keyboard.press('Enter');
    const res = await q(() => document.querySelector('[data-draw=resultaat]').textContent);
    if (!/binnen 2 km/.test(res)) fouten.push('straal werkt niet: ' + res);
    await p.click('.bs-tabel tbody a');
    if (await q(() => !document.querySelector('#detailvak h3').textContent)) fouten.push('geen detail');
    if (await q(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)) fouten.push('horizontale scroll');
    console.log(width, fouten.length ? fouten : 'ok');
    if (fouten.length) process.exitCode = 1;
    await p.close();
  }
  await b.close();
})();
