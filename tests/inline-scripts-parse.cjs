// Fails if any inline <script> in a published page doesn't parse. One stray
// apostrophe in a single-quoted string ("don't") once broke the whole admin
// dashboard, including Sign In, with no visible error.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const os = require('os');

const root = path.join(__dirname, '..');
const skipDirs = new Set(['.git', 'node_modules', 'carousel', 'store', 'i18n', 'tests']);
const pages = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!skipDirs.has(e.name)) walk(path.join(dir, e.name)); }
    else if (e.name.endsWith('.html')) pages.push(path.join(dir, e.name));
  }
})(root);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'inline-js-'));
let failures = 0, checked = 0;
for (const page of pages) {
  const html = fs.readFileSync(page, 'utf8');
  const re = /<script(\s[^>]*)?>([\s\S]*?)<\/script>/gi;
  let m, i = 0;
  while ((m = re.exec(html))) {
    const attrs = m[1] || '';
    if (/\bsrc\s*=/.test(attrs)) continue;
    const type = (attrs.match(/\btype\s*=\s*["']?([^"'\s>]+)/i) || [])[1] || 'text/javascript';
    if (!/^(text\/javascript|application\/javascript|module)$/i.test(type)) continue;  // JSON-LD etc.
    const file = path.join(tmp, `s${checked}${type === 'module' ? '.mjs' : '.cjs'}`);
    fs.writeFileSync(file, m[2]);
    checked++; i++;
    try { execFileSync(process.execPath, ['--check', file], { stdio: 'pipe' }); }
    catch (e) {
      failures++;
      const line = html.slice(0, m.index).split('\n').length;
      console.error(`✗ ${path.relative(root, page)} — inline script #${i} (starts at line ${line}):\n${String(e.stderr).trim()}\n`);
    }
  }
}
console.log(`${checked} inline scripts in ${pages.length} pages checked, ${failures} failed`);
process.exit(failures ? 1 : 0);
