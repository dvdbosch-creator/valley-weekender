// Render-check a page at phone width (390px). Usage:
//   NODE_PATH=/workspace/valley-weekend/node_modules node tools/render_check.js URL OUT.png
// Prints font, image and link counts; exits 1 if any image is broken or fonts did not load.
const puppeteer = require('puppeteer-core');
const [url, out = '/tmp/vw-check-390.png'] = process.argv.slice(2);
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  const r = await p.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  await p.evaluate(() => document.fonts.ready);
  const s = await p.evaluate(() => ({
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family),
    broken: [...document.images].filter(i => !i.naturalWidth).map(i => i.src),
    links: document.querySelectorAll('a[href]').length,
    overflowX: document.documentElement.scrollWidth > 390,
  }));
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
  console.log(JSON.stringify({ status: r.status(), ...s, screenshot: out }, null, 1));
  const ok = r.status() === 200 && !s.broken.length && s.fonts.some(f => /Fraunces/.test(f)) && !s.overflowX;
  process.exit(ok ? 0 : 1);
})();
