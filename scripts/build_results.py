#!/usr/bin/env python3
"""Build self-contained HTML views from an audited external case."""
import argparse
import html
import json
from pathlib import Path
from common import outside_toolkit, fail
from result_view import build_view

def document(view):
    # Escape for a script element, not only JSON: register text is untrusted input.
    payload = json.dumps(view, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return TEMPLATE.replace('__PAYLOAD__', payload)

TEMPLATE = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<title>Family history · evidence and open questions</title><style>
body{font:16px/1.6 system-ui,sans-serif;background:#f5f2eb;color:#252c2a;margin:0}header,main{max-width:1150px;margin:auto;padding:28px}h1{font-family:Georgia,serif;font-size:2.5rem;margin:0}.muted{color:#626c68}button,input{font:inherit;padding:8px 14px;border:1px solid #b8c3bc;border-radius:8px;background:white}button{cursor:pointer}nav{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.canvas{overflow:auto;max-height:65vh;background:#e6ece5;border-radius:12px;padding:20px;min-height:220px}.world{display:flex;align-items:flex-start;gap:45px;transform-origin:top left;position:relative;min-width:max-content}.column{display:grid;gap:18px;z-index:1}.person{display:block;width:220px;text-align:left;background:white;border:1px solid #9cae9f;padding:14px;box-shadow:0 2px 5px #0001}.person strong{display:block}.selected{outline:3px solid #4c7865}.uncertain{border-style:dashed;color:#886b31}svg{position:absolute;inset:0;overflow:visible;pointer-events:none}.details{background:white;border-radius:12px;padding:20px;margin-top:22px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #d4ddd5;padding:10px;text-align:left;vertical-align:top}a{color:#235f4b}code{font-size:.85em}summary{cursor:pointer} @media(max-width:600px){header,main{padding:18px}h1{font-size:2rem}table{font-size:.85rem}} @media print{nav{display:none}.canvas{max-height:none;overflow:visible}.world{transform:none!important}body{background:white}}
</style><header><p class="muted">FAMILY HISTORY · LOCAL RESEARCH VIEW</p><h1>People, relationships, evidence</h1><p id="mode" class="muted"></p><p id="warnings"></p><nav><input id="search" aria-label="Find a person" placeholder="Find a name or ID"><button id="minus" aria-label="Zoom out">−</button><button id="plus" aria-label="Zoom in">+</button><button id="reset">Reset zoom</button></nav></header><main><section class="canvas" aria-label="Family tree"><div id="world" class="world"></div></section><p class="muted">Solid lines: single-source or stronger. Dashed lines: unresolved, hypothetical, or conflicting. Generations are a display aid; distinct candidates stay separate.</p><section id="details" class="details" aria-live="polite"></section><section class="details"><h2>Relationships and their sources</h2><div id="relations"></div></section><section class="details"><h2>Sources</h2><div id="sources"></div></section><section class="details"><h2>Open questions and research coverage</h2><p>This view contains recorded relationships only. Consult the private case's research-state.md, search-log.csv, plan/BOARD.md, and audit warnings for unresolved readings, competing identities, actual search coverage, and next actions. Missing relatives and empty searches are not evidence of absence.</p></section></main><script id="case-data" type="application/json">__PAYLOAD__</script><script>
const data=JSON.parse(document.getElementById('case-data').textContent), byId=new Map(data.people.map(p=>[p.id,p])), world=document.getElementById('world');
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n};
const accepted=r=>['single-source','corroborated','strongly-corroborated'].includes(r.status)&&!r.has_contradictions;
document.getElementById('mode').textContent=data.private?'PRIVATE OUTPUT · includes living or unknown-status people. Review before sharing.':'Sharing view · explicitly deceased people only. Review citations before sharing.';
document.getElementById('warnings').textContent=data.audit_warning_count?`${data.audit_warning_count} evidence audit warning(s) remain. Read the case audit before interpreting this view.`:'Referential audit completed. This does not establish identity or kinship.';
let selected=data.root, scale=1;const cards=new Map(), depth=new Map(data.people.map(p=>[p.id,0]));
const parents=data.relationships.filter(r=>['parent-of','father-of','mother-of','child-of'].includes(r.type));
const endpoints=r=>r.type==='child-of'?[r.b,r.a]:[r.a,r.b];
// Bounded relaxation handles malformed cycles without hanging; audit/review must resolve them.
for(let step=0;step<Math.min(data.people.length,25);step++){let changed=false;for(const r of parents){const [p,c]=endpoints(r), d=Math.min(24,(depth.get(c)||0)+1);if(d>(depth.get(p)||0)){depth.set(p,d);changed=true}}if(!changed)break}
const columns=new Map();for(const p of data.people){const d=depth.get(p.id);if(!columns.has(d)){const col=el('div');col.className='column';columns.set(d,col)}}
for(const [d,col] of [...columns].sort((a,b)=>a[0]-b[0]))world.append(col);
const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('aria-hidden','true');world.prepend(svg);
function show(id){selected=id;for(const [pid,n] of cards)n.classList.toggle('selected',pid===id);const p=byId.get(id), box=document.getElementById('details');box.replaceChildren();if(!p){box.append(el('p','No people in this output view. Record evidence and deceased status, or request a private output.'));return}box.append(el('h2',p.name),el('p',`${p.id} · ${p.birth||'?'} — ${p.death||'?'}`));for(const r of data.relationships.filter(r=>r.a===id||r.b===id)){const other=byId.get(r.a===id?r.b:r.a);box.append(el('p',`${r.type} · ${other.name} · ${r.status}${r.has_contradictions?' · conflicting evidence':''}`))}}
for(const p of data.people){const card=el('button');card.className='person';card.append(el('strong',p.name),el('span',`${p.birth||'?'} — ${p.death||'?'}`),el('small',' · '+p.id));card.onclick=()=>show(p.id);columns.get(depth.get(p.id)).append(card);cards.set(p.id,card)}
function lines(){svg.replaceChildren();for(const r of data.relationships){if(!parents.includes(r)&&!['spouse-of','married-to'].includes(r.type))continue;const a=cards.get(r.a),b=cards.get(r.b);if(!a||!b)continue;const path=document.createElementNS(svg.namespaceURI,'path');const x1=a.offsetLeft+a.offsetWidth/2,y1=a.offsetTop+a.offsetHeight/2,x2=b.offsetLeft+b.offsetWidth/2,y2=b.offsetTop+b.offsetHeight/2;path.setAttribute('d',`M${x1},${y1} C${(x1+x2)/2},${y1} ${(x1+x2)/2},${y2} ${x2},${y2}`);path.setAttribute('fill','none');path.setAttribute('stroke',accepted(r)?'#587567':'#a08247');path.setAttribute('stroke-width','2');if(!accepted(r))path.setAttribute('stroke-dasharray','5 5');svg.append(path)}}
const table=el('table');const head=el('tr');for(const t of ['People','Relationship','Evidence status','Sources'])head.append(el('th',t));table.append(head);for(const r of data.relationships){const row=el('tr');row.append(el('td',`${byId.get(r.a).name} → ${byId.get(r.b).name}`),el('td',`${r.type} (${r.nature||'unspecified'})`),el('td',r.status+(r.has_contradictions?' · conflicting evidence':'')));const refs=el('td');for(const id of r.sources){const a=el('a',id+' ');a.href='#source-'+id;refs.append(a)}row.append(refs);table.append(row)}document.getElementById('relations').append(table);
for(const s of data.sources){const box=el('p');box.id='source-'+s.id;box.append(el('strong',s.id+' · '+s.title),el('span',' · '+s.custodian+(s.reference?' · '+s.reference:'')));if(s.url){const a=el('a',' Open source');a.href=s.url;a.rel='noreferrer noopener';box.append(a)}document.getElementById('sources').append(box)}
function zoom(value){scale=Math.max(.35,Math.min(2,value));world.style.transform=`scale(${scale})`};document.getElementById('minus').onclick=()=>zoom(scale-.15);document.getElementById('plus').onclick=()=>zoom(scale+.15);document.getElementById('reset').onclick=()=>zoom(1);document.getElementById('search').oninput=e=>{const q=e.target.value.toLocaleLowerCase();for(const p of data.people){const n=cards.get(p.id);n.style.opacity=(!q||(p.name+' '+p.id).toLocaleLowerCase().includes(q))?'1':'.25'}};
show(selected);requestAnimationFrame(lines);window.addEventListener('resize',lines);
</script></html>'''

def build(case, output_dir=None, private=False, root_person=None, overwrite=False):
    case = outside_toolkit(case)
    out = outside_toolkit(output_dir or case / 'output')
    if out == case or out in case.parents or any((case / name).resolve() == out or (case / name).resolve() in out.parents for name in ('originals', 'sources', 'photos', 'work', 'plan')):
        raise ValueError('Choose a dedicated output directory, not the case root or an ancestor.')
    view = build_view(case, private, root_person)
    destinations = [out / 'report.html']
    if any(path.exists() for path in destinations) and not overwrite:
        raise ValueError('Output exists. Use --overwrite to replace generated files.')
    out.mkdir(parents=True, exist_ok=True)
    rendered = document(view)
    for path in destinations:
        path.write_text(rendered, encoding='utf-8')
    return destinations

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case-dir', required=True)
    parser.add_argument('--output-dir')
    parser.add_argument('--root-person')
    parser.add_argument('--private-output', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        for path in build(args.case_dir, args.output_dir, args.private_output, args.root_person, args.overwrite):
            print(path)
        return 0
    except (ValueError, OSError, KeyError) as error:
        return fail(error)

if __name__ == '__main__':
    raise SystemExit(main())
