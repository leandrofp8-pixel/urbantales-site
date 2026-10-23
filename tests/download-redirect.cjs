const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const script = readFileSync(join(__dirname, '../download/redirect.js'), 'utf8');
function run(userAgent, search = '', maxTouchPoints = 0, blocked = false) {
  const elements = { apple: {}, google: {}, status: {} };
  let destination;
  vm.runInNewContext(script, {
    URL, URLSearchParams, navigator: { userAgent, maxTouchPoints },
    document: { getElementById: id => elements[id] },
    window: { location: { search, replace: url => { if (blocked) throw Error('Blocked'); destination = new URL(url); } } }
  });
  return { elements, destination };
}
for (const ua of ['Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X)', 'iPod', 'iPad', 'iPhone BytedanceWebview TikTok']) {
  assert.equal(run(ua).destination.hostname, 'apps.apple.com');
}
assert.equal(run('Mozilla/5.0 (Macintosh; Intel Mac OS X)', '', 5).destination.hostname, 'apps.apple.com');
for (const ua of ['Windows NT 10.0', 'Macintosh', 'Linux x86_64', '', 'Googlebot']) assert.equal(run(ua).destination, undefined);
const query = '?utm_source=tiktok&utm_medium=paid_social&utm_campaign=tiktok-launch&utm_content=rome-video';
const android = run('Mozilla/5.0 (Linux; Android 15) TikTok', query);
assert.equal(android.destination.hostname, 'play.google.com');
assert.equal(android.destination.searchParams.get('id'), 'com.urbantales.app');
const referrer = new URLSearchParams(android.destination.searchParams.get('referrer'));
assert.equal(referrer.get('utm_source'), 'tiktok');
assert.equal(referrer.get('utm_medium'), 'paid_social');
assert.equal(referrer.get('utm_campaign'), 'tiktok-launch');
assert.equal(referrer.get('utm_content'), 'rome-video');
const apple = run('iPhone', query).destination;
assert.equal(apple.searchParams.get('pt'), '128624357');
assert.equal(apple.searchParams.get('ct'), 'tiktok-launch');
assert.equal(run('iPhone', '?src=tiktok').destination.searchParams.get('ct'), 'download-tiktok');
assert.equal(run('Android', '?url=https://evil.example').destination.hostname, 'play.google.com');
assert.equal(run('iPhone', '?utm_campaign=' + 'x'.repeat(100)).destination.searchParams.get('ct').length, 40);
const blocked = run('iPhone', query, 0, true);
assert.equal(blocked.destination, undefined);
assert.ok(blocked.elements.apple.href.startsWith('https://apps.apple.com/'));
assert.ok(blocked.elements.status.textContent.includes('Choose your store'));
const html = readFileSync(join(__dirname, '../download/index.html'), 'utf8');
assert.ok(html.includes('href="https://apps.apple.com/'));
assert.ok(html.includes('href="https://play.google.com/'));
console.log('Download routing passed: iOS, Android, TikTok user agents, iPadOS, desktop, attribution, blocked redirect and static fallback.');
