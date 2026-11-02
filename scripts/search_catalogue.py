#!/usr/bin/env python3
"""Search local catalogue text; historical custody still requires source review."""
import argparse
import json
import unicodedata
from common import ROOT, read_json

def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD',value.casefold().replace('ё','е')) if not unicodedata.combining(c))

def search(place='', country=None, record_type='', year=None):
    db=read_json(ROOT/'regional-archives/data/archives.json')
    jurisdictions=read_json(ROOT/'regional-archives/data/jurisdictions.json')
    regions={r['id']:r for r in jurisdictions['regions']}
    records=[]
    terms=[normalize(v) for v in (place,record_type) if v]
    for a in db['archives']:
        if country and a['country']!=country:continue
        labels=' '.join(regions[r]['name']+' '+' '.join(regions[r]['aliases']) for r in a['region_ids'])
        hay=normalize(json.dumps(a,ensure_ascii=False)+' '+labels)
        score=sum(term in hay for term in terms)
        if terms and not score:continue
        records.append({'id':a['id'],'name':a['official_name'],'country':a['country'],'kind':a['kind'],
                        'score':score,'path':'regional-archives/countries/'+a['country']+'/README.md#'+a['id'],
                        'url':a['website_url'] or a['directory_url'],'date_coverage':a['documented_date_range'],
                        'warning':'Keyword match only; verify historical jurisdiction, collection dates and actual custody.'})
    for s in read_json(ROOT/'resources/sources.json')['sources']:
        if country:continue
        hay=normalize(json.dumps(s,ensure_ascii=False));score=sum(term in hay for term in terms)
        if terms and not score:continue
        records.append({'id':s['id'],'name':s['title'],'kind':'general-resource','score':score,'url':s['url'],
                        'warning':'General discovery route; not an archival custody determination.'})
    return {'event_year':year,'year_used_as_filter':False,
            'note':'The year is research context, not an automatic date or custody filter. Follow the dated place workflow.',
            'results':sorted(records,key=lambda r:(-r['score'],r['name'])),
            'historical_routes':jurisdictions['historical_routes']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--place',default='')
    p.add_argument('--country')
    p.add_argument('--year',type=int)
    p.add_argument('--record-type',default='')
    p.add_argument('--json',action='store_true')
    p.add_argument('--limit',type=int,default=20)
    a=p.parse_args()
    result=search(a.place,a.country,a.record_type,a.year)
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(result['note'])
        for row in result['results'][:a.limit]:
            print(row['name']+' ['+row['kind']+']\n  '+row['url'])
        print(str(len(result['results']))+' keyword matches; no result is not proof of absent records.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
