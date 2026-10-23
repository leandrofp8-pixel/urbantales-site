/* Fixed store destinations only. No ad SDK, cookies, or external dependencies. */
(function () {
  'use strict';
  var query = new URLSearchParams(window.location.search);
  function label(value, fallback, limit) {
    return (value || '').replace(/[^a-z0-9_-]/gi, '-').slice(0, limit) || fallback;
  }
  var source = label(query.get('utm_source') || query.get('src'), 'direct', 40);
  var medium = label(query.get('utm_medium'), 'website', 40);
  var campaign = label(query.get('utm_campaign'), 'download-' + source, 40);
  var apple = new URL('https://apps.apple.com/app/id6760130598');
  apple.searchParams.set('pt', '128624357');
  apple.searchParams.set('ct', campaign);
  apple.searchParams.set('mt', '8');
  var google = new URL('https://play.google.com/store/apps/details?id=com.urbantales.app');
  var referrer = new URLSearchParams({ utm_source: source, utm_medium: medium, utm_campaign: campaign });
  ['utm_content', 'utm_term'].forEach(function (key) {
    if (query.get(key)) referrer.set(key, label(query.get(key), '', 100));
  });
  google.searchParams.set('referrer', referrer.toString());
  document.getElementById('apple').href = apple.toString();
  document.getElementById('google').href = google.toString();

  var ua = navigator.userAgent || '';
  var ios = /iPhone|iPad|iPod/i.test(ua) ||
    (/Macintosh/i.test(ua) && navigator.maxTouchPoints > 1);
  var destination = /Android/i.test(ua) ? google : ios ? apple : null;
  // Unknown devices stay on the store chooser. Never guess from screen size.
  if (destination) {
    document.getElementById('status').textContent = 'Opening ' + (ios ? 'the App Store' : 'Google Play') + '…';
    try { window.location.replace(destination.toString()); } catch (error) {
      document.getElementById('status').textContent = 'Choose your store below to download Urban Tales.';
    }
  }
})();
