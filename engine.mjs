const hex=b=>Array.from(b,x=>x.toString(16).padStart(2,'0')).join('');
const sha=async s=>{if(typeof s!=='string')throw Error('Artifact content must be text');return hex(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s))));};
const canonical=v=>Array.isArray(v)?'['+v.map(canonical).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}':JSON.stringify(v);
export async function analyze(d){
if(!d||typeof d!=='object'||Array.isArray(d))throw Error('Input must be a JSON object');
const raw=JSON.stringify(d);if(raw.length>100000)throw Error('Scenario exceeds 100 KB limit');
function inspect(v,depth=0){if(depth>15)throw Error('Input nesting exceeds 15 levels');if(Array.isArray(v)&&v.length>1000)throw Error('Maximum 1000 items per array');if(v&&typeof v==='object'){for(const [k,x] of Object.entries(v)){if(['__proto__','constructor','prototype'].includes(k))throw Error('Reserved input key');inspect(x,depth+1);}}if(typeof v==='number'&&!Number.isFinite(v))throw Error('Numbers must be finite');}inspect(d);
const r=d.request;if(!r||typeof d.now!=='number')throw Error('request and numeric now are required');const matches=(d.grants||[]).filter(g=>g.subject===r.subject&&g.action===r.action&&g.resource===r.resource&&g.expires>d.now);if(matches.some(g=>g.effect==='deny'))return {allowed:false,reason:'explicit-deny'};const a=matches.filter(g=>g.effect==='allow');if(!a.length)return {allowed:false,reason:'no-active-grant'};if(a.every(g=>g.approval_required)&&!r.approved)return {allowed:false,reason:'approval-required'};return {allowed:true,reason:'active-grant'};
}
