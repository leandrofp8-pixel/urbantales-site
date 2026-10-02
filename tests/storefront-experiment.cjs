const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(require('node:path').join(__dirname,'../dashboard.html'),'utf8');
const el={};const c=vm.createContext({document:{getElementById:()=>el},fmt:String});
for(const name of ['escapeHtml','renderStorefrontExperiment']){const start=html.indexOf(`function ${name}(`);vm.runInContext(html.slice(start,html.indexOf('\n}',start)+2),c);}
c.renderStorefrontExperiment(null);assert(el.textContent.includes('unavailable'));
c.renderStorefrontExperiment({enabled:false,test_pct:50,window_days:7,rows:[]});assert(el.innerHTML.includes('No measured Store exposures'));
c.renderStorefrontExperiment({enabled:true,test_pct:50,window_days:7,rows:[{segment:'<img src=x>',variant:'coins_first',exposed:10,mature:0,buyers:0,conversion_pct:null,coin_buyers:0,subscription_buyers:0,gross_usd:0,revenue_per_exposed_usd:null,unpriced_purchases:0}]});
assert(!el.innerHTML.includes('<img src=x>'));assert(el.innerHTML.includes('—'));assert(el.innerHTML.includes('Coins first'));
console.log('Store report rendering passed: missing backend, empty experiment, immature cohorts and escaped labels.');
