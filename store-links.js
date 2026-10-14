/* Tags every App Store / Google Play link with where the visitor came from, so the store reports
   can split installs by source (blog vs Instagram vs Facebook vs Google...).
   Campaign = "<page>-<source>", e.g. "blog-instagram", "home-google", "tour-direct".
   - source: ?src=... on the URL (use https://urbantales.net/?src=instagram in the Instagram bio), else the
     referrer's domain, else "direct". It's remembered for the visit, so it survives clicks to other pages.
   - Apple: needs the provider token (App Store Connect > Analytics > Campaigns > "pt=..."); until it's set,
     Apple links are left as they are. Google Play: utm referrer, shown in Play Console > Acquisition. */
(function () {
  var APPLE_PROVIDER_TOKEN = '128624357';
  function source() {
    try {
      var q = new URLSearchParams(location.search).get('src');
      if (q) { sessionStorage.setItem('ut_src', q); return q; }
      var saved = sessionStorage.getItem('ut_src');
      if (saved) return saved;
    } catch (e) {}
    var r = (document.referrer || '').toLowerCase(), s = 'direct';
    if (r && r.indexOf(location.hostname) === -1) {
      s = /instagram/.test(r) ? 'instagram' : /facebook|fb\.|l\.facebook/.test(r) ? 'facebook' : /tiktok/.test(r) ? 'tiktok'
        : /google\./.test(r) ? 'google' : /bing\.|duckduckgo|yahoo/.test(r) ? 'search' : /chatgpt|openai|perplexity|claude|gemini|copilot/.test(r) ? 'ai'
        : 'other';
    }
    try { sessionStorage.setItem('ut_src', s); } catch (e) {}
    return s;
  }
  function page() {
    var p = location.pathname.split('/').pop() || 'index.html';
    if (/^blog-/.test(p)) return 'blog';
    if (p === 'blog.html') return 'bloglist';
    if (p === 'index.html' || p === '') return 'home';
    if (/^tour/.test(p)) return 'tour';
    return p.replace(/\.html$/, '').slice(0, 15);
  }
  var lang = /^\/es\//.test(location.pathname) ? 'es' : '';
  var campaign = ((lang ? lang + '' : '') + page() + '-' + source()).replace(/[^a-z0-9-]/gi, '').slice(0, 40);
  function tag() {
    var links = document.querySelectorAll('a[href*="apps.apple.com"], a[href*="play.google.com/store/apps"]');
    for (var i = 0; i < links.length; i++) {
      try {
        var u = new URL(links[i].href);
        if (u.hostname === 'apps.apple.com') {
          if (!APPLE_PROVIDER_TOKEN) continue;
          u.searchParams.set('pt', APPLE_PROVIDER_TOKEN); u.searchParams.set('ct', campaign); u.searchParams.set('mt', '8');
        } else {
          u.searchParams.set('referrer', 'utm_source=' + source() + '&utm_medium=website&utm_campaign=' + campaign);
        }
        links[i].href = u.toString();
      } catch (e) {}
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', tag); else tag();
  new MutationObserver(tag).observe(document.documentElement, { childList: true, subtree: true });
})();
