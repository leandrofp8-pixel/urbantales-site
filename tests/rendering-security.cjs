const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const payload = `O'Neil ");globalThis.pwned=true;// <img src=x onerror=alert(1)> &quot;`;
function source(file) { return fs.readFileSync(path.join(__dirname, '..', file), 'utf8'); }
function extract(text, name) {
  const start = text.indexOf(`function ${name}(`);
  assert(start >= 0, name);
  return text.slice(text.slice(Math.max(0,start-6),start)==='async ' ? start-6:start, text.indexOf('\n}',start)+2);
}
function setup(file, functions) {
  const elements = new Map();
  const context = vm.createContext({
    document: {getElementById(id) { if(!elements.has(id)) elements.set(id,{innerHTML:'',textContent:'',value:''}); return elements.get(id); }},
    fmtDate:()=>'', fmt: String, _usd:String, usd:String, timeAgo:()=>'', countryFlag:()=>'',
    _stageBadge:{}, _selectedProfiles:new Set(), _activeProfileEmail:null,
    DATE_LOCALE:{en:'en'}, LANG:'en', REDEEM_BASE:'https://urbantales.net/redeem?code=',
    qrDataUrl:()=> 'data:image/png;base64,AA==', pl:()=> 'days',
    s:{daySingular:'day',dayPlural:'days'},
  });
  const text=source(file);
  for(const name of ['escapeHtml','jsArg',...functions]) vm.runInContext(extract(text,name),context);
  return {context,elements};
}
function safe(html) { assert(!html.includes('<img src=x'), html); assert(!html.includes('<script'),html); }
function decode(value) { return value.replace(/&(quot|#39|lt|gt|amp);/g,(_,key)=>({'quot':'"','#39':"'",lt:'<',gt:'>',amp:'&'}[key])); }
(async()=>{
  let {context:c,elements:e}=setup('dashboard.html',['renderInfluencerAccounts','renderUserList','loadAgencies','renderPromoCodes']);
  c.renderInfluencerAccounts({accounts:[{_id:'abc',name:payload,email:payload,instagram:payload,audience_description:payload}]});
  let html=e.get('pendingInfluencersBody').innerHTML;safe(html);
  let args;
  c.approveInfluencer=(...values)=>{args=values};
  vm.runInContext(decode(html.match(/onclick="([^"]*)"/)[1]),c);
  assert.equal(args[1],payload);assert.equal(c.pwned,undefined);
  c.renderPromoCodes({promo_codes:[{code:payload,influencer_email:payload}]});
  html=e.get('promoCodesBody').innerHTML;safe(html);
  c.editPromoCode=value=>{args=value};
  vm.runInContext(decode(html.match(/onclick="([^"]*)"/)[1]),c);assert.equal(args.code,payload);
  c.renderUserList([{email:payload,display_name:payload}]);safe(e.get('userList').innerHTML);
  c.api=async()=>({accounts:[{email:payload,name:payload,company:payload,phone:payload}]});
  await c.loadAgencies();html=e.get('agencyBody').innerHTML;safe(html);
  c.approveAgency=value=>{args=value};
  vm.runInContext(decode(html.match(/onclick="([^"]*)"/)[1]),c);assert.equal(args,payload);
  ({context:c}=setup('agency.html',['voucherHtml']));
  safe(c.voucherHtml({code:'PASS123',traveler_name:payload,start_date:'2026-09-25',days:3}));
  // Referral text is placed in a code node after the trusted locale markup.
  const invite=source('invite.html');
  const lines=invite.split('\n').filter(line=>line.includes("document.getElementById('txt-step3-p').innerHTML")||line.includes("document.querySelector('#txt-step3-p code').textContent"));
  let container={},code={};
  vm.runInNewContext(lines.join('\n'),{promoCode:payload,s:{step3p:'Enter <code>{code}</code> now.'},
    fmt:(s,v)=>s.replace('{code}',v.code),document:{getElementById:()=>container,querySelector:()=>code}});
  assert.equal(container.innerHTML,'Enter <code></code> now.');assert.equal(code.textContent,payload);
  // Playback tab: every string from the app (landmark names, versions, reasons) must be escaped.
  ({context:c,elements:e}=setup('dashboard.html',['kpiCard','_playbackSeconds','_playbackPct','_playbackMeters','_playbackEngine','renderPlaybackHealth']));
  const dash=source('dashboard.html');
  vm.runInContext(dash.slice(dash.indexOf('const PLAYBACK_SIGNAL_LABELS'),dash.indexOf('function _playbackSeconds')),c);
  Object.assign(c,{lineChart:()=>{},doughnutChart:()=>{},shortDate:String,C:{primary:'',yellow:'',green:'',blue:''}});
  c.renderPlaybackHealth({
    summary:{plays:1,auto_plays:1,users:1,sessions:1,signals:{overlapping_audio:1},direction_zones:{ahead:1,side:0,behind:0},
      end_reasons:{[payload]:1},queue_dropped:{[payload]:1},recovered:{[payload]:2},gen_cancelled:{},
      interruptions:{began:1,resumed:0,moved_on:{[payload]:1},audio_route_lost:0},trigger_to_audio_p50_ms:null,started_out_of_range_pct:null,started_behind_pct:null,
      external_pauses_per_100_plays:null,queued_age_p50_s:null,queued_age_p90_s:null},
    app_versions:[payload],
    breakdown:[{platform:payload,engine:payload,plays:1}],
    daily:[],
    recent_problems:[{timestamp:'2026-09-28T10:00:00Z',kind:payload,type:payload,detail:payload,landmark_name:payload,
      platform:payload,engine:payload,app_state:payload,app_version:payload}],
  });
  for(const id of ['playbackVersion','playbackEndReasons','playbackBreakdownBody','playbackProblemsBody','playbackSignals','playbackKpis','playbackKpis2','playbackNotice','playbackInterruptions','playbackSelfHealing']) safe(e.get(id).innerHTML);
  assert(e.get('playbackProblemsBody').innerHTML.includes('&lt;img src=x'));
  console.log('Rendering security checks passed: names, attributes, button arguments, vouchers, referral code, playback tab.');
})().catch(error=>{console.error(error);process.exitCode=1;});
