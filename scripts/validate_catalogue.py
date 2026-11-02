#!/usr/bin/env python3
"""Validate catalogue integrity, coverage assertions, general URLs, and upstream pin."""
import argparse
import hashlib
import re
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl
from common import ROOT,UPSTREAM,read_json

FORMER_USSR={'russia','ukraine','belarus','moldova','estonia','latvia','lithuania','georgia','armenia','azerbaijan','kazakhstan','kyrgyzstan','tajikistan','turkmenistan','uzbekistan'}

def check_url(url):
    try:
        p=urlsplit(url)
        if p.scheme not in ('http','https') or not p.hostname or p.username or p.password:return False
        if any(k.casefold() in {'token','session','sessionid','password','auth','q','query','surname','lastname'} for k,v in parse_qsl(p.query)):return False
        if re.search(r'/(?:person|persons|record|records|scan|scans)/\d',p.path,re.I):return False
        return not re.search(r'\s|[<>"\\]',url)
    except (ValueError,TypeError):return False

def validate(root=ROOT):
    errors=[]
    db=read_json(root/'regional-archives/data/archives.json')
    js=read_json(root/'regional-archives/data/jurisdictions.json')
    cov=read_json(root/'regional-archives/data/coverage.json')
    ss=read_json(root/'resources/sources.json')
    countries={c['id'] for c in db['countries']}
    if not FORMER_USSR <= countries:errors.append('Missing former-USSR country indexes.')
    def unique(rows,key,label):
        seen=set()
        for row in rows:
            value=row.get(key)
            if not value or value in seen:errors.append(label+': missing/duplicate '+str(value))
            seen.add(value)
        return seen
    unique(db['countries'],'id','countries')
    aids=unique(db['archives'],'id','archives');rids=unique(js['regions'],'id','regions')
    unique(ss['sources'],'id','resources')
    unique(cov['regions'],'region_id','coverage')
    amap={a['id']:a for a in db['archives']}
    rmap={r['id']:r for r in js['regions']}
    hosts={}
    for a in db['archives']:
        if a['country'] not in countries:errors.append(a['id']+': unknown country')
        if a['kind'] not in {'repository','branch','authority','service-office','portal'}:errors.append(a['id']+': invalid kind')
        if set(a['region_ids'])-rids:errors.append(a['id']+': dangling region')
        if any(rmap[r]['country']!=a['country'] for r in a['region_ids'] if r in rmap):errors.append(a['id']+': wrong-country region')
        if set(a['related_archive_ids'])-aids:errors.append(a['id']+': dangling related archive')
        if not a.get('description') or not a.get('gaps') or not a['verification'].get('source_urls'):errors.append(a['id']+': missing description, limits or evidence')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',a['verification'].get('checked_at','')):errors.append(a['id']+': missing check date')
        if a['website_url']:
            identity=(a['country'],a['website_url'].rstrip('/'),a['official_name'].casefold())
            if identity in hosts:errors.append(a['id']+': duplicate institution alias of '+hosts[identity])
            hosts[identity]=a['id']
    if {x['region_id'] for x in cov['regions']}!=rids:errors.append('Coverage does not match region checklist.')
    for c in cov['regions']:
        rid=c['region_id']
        expected={a['id'] for a in db['archives'] if rid in a['region_ids']}
        if set(c['institution_ids'])!=expected:errors.append(rid+': stale coverage institution list')
        if c['state']=='complete' and not(c['network_reconciled'] and c['municipal_branches_reconciled'] and c.get('review_explanation')):
            errors.append(rid+': unsupported completeness assertion')
        if c['state']!='complete' and not c['gaps']:errors.append(rid+': partial region lacks gaps')
    if cov['complete_regions']!=sum(r['state']=='complete' for r in cov['regions']):errors.append('Wrong complete-region count.')
    def urls(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k.endswith('_url') and v:yield v
                elif k.endswith('_urls') or k=='discovery_sources':
                    yield from (x for x in v if isinstance(x,str))
                else:yield from urls(v)
        elif isinstance(value,list):
            for v in value:yield from urls(v)
    for data in (db,js,cov,ss):
        for url in urls(data):
            if not check_url(url):errors.append('Unsafe/non-general URL: '+str(url))
    for s in ss['sources']:
        if not check_url(s['url']):errors.append('Unsafe source URL: '+s['id'])
        if set(s['archive_ids'])-aids:errors.append(s['id']+': missing archive reference')
    lock=read_json(root/'upstream-lock.json')
    actual={str(p.relative_to(root/'vendor/ex-ussr-kinship-research')) for p in (root/'vendor/ex-ussr-kinship-research').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if actual!=set(lock['files']):errors.append('Vendored file inventory differs from upstream lock.')
    for name,digest in lock['files'].items():
        p=(root/'vendor/ex-ussr-kinship-research'/name).resolve()
        base=(root/'vendor/ex-ussr-kinship-research').resolve()
        if base not in p.parents:errors.append('Unsafe upstream path.');continue
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append('Upstream checksum mismatch: '+name)
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-denylist',type=Path,help='Local-only JSON list of private strings; never copied or printed.')
    a=p.parse_args()
    errors=validate()
    if a.private_denylist:
        terms=read_json(a.private_denylist)
        for path in ROOT.rglob('*'):
            if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:continue
            content=path.read_bytes().decode('utf-8',errors='ignore').casefold()
            if any(t.casefold() in content for t in terms if t):errors.append('Private screening match in '+str(path.relative_to(ROOT)))
    if errors:print('\n'.join(errors));return 1
    print('Catalogue, coverage and upstream pin checks passed.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
