const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(require('node:path').join(__dirname, '..', 'dashboard.html'), 'utf8');
const elements = new Map(), charts = new Map();
const context = vm.createContext({
  document: { getElementById(id) { if (!elements.has(id)) elements.set(id, {}); return elements.get(id); } },
  fmt: String, fmtCost: String, fmtPct: n => n + '%', shortDate: String,
  C: {}, _purchasesLoaded: true,
  lineChart: (id, labels, data) => charts.set(id, {labels, data}), doughnutChart: () => {},
});
for (const name of ['escapeHtml', 'kpiCard', 'renderCosts', 'renderCostTrends']) {
  const start = source.indexOf(`function ${name}(`);
  assert(start >= 0);
  vm.runInContext(source.slice(start, source.indexOf('\n}', start) + 2), context);
}
// Old backend / historical periods must show missing measurements, not zero reuse.
context.renderCosts({summary: {actual_api_calls: 7}}, {});
assert(elements.get('requestCacheKpis').innerHTML.includes('No measured requests'));
assert.equal(charts.get('chartCacheTrend').labels.length, 0);
context.renderCosts({summary: {actual_api_calls: 1}, legacy_events: 8,
  cache_metrics: {nearby: {requests: 2, hits: 1, distinct_keys: 1, hit_rate: 50}},
  cache_daily: [{_id: {date: '2026-10-02', family: 'nearby'}, requests: 2, hits: 1}],
}, {});
assert(elements.get('requestCacheKpis').innerHTML.includes('50.0%'));
assert(elements.get('costEstimateNote').textContent.includes('8 older events'));
assert.equal(charts.get('chartCacheTrend').data[0].data[0], 50);
assert.equal(charts.get('chartCacheTrend').data[2].data[0], null);
context.renderCostTrends({weekly: [{week_start: '2026-09-28', cache_hit_rate: null,
  maps_cache_hit_rate: null, total_cost: 1, revenue: 0}], by_city: []});
assert(elements.get('costTrendKpis').innerHTML.includes('—'));
assert.equal(charts.get('chartCacheHitTrend').data[0].data[0], null);
console.log('Pricing/cache rendering passed: old responses, missing history, measured reuse, weekly gaps.');
