#!/usr/bin/env python3
"""Optional network review. Never deletes or changes a catalogue entry."""
import argparse
import concurrent.futures
import datetime
import urllib.request
from common import ROOT,read_json,write_json,outside_toolkit

def check(url):
    result={'url':url,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'FamilyHistoryStarter/0.1 (public link review)'})
        with urllib.request.urlopen(req,timeout=15) as response:
            body=response.read(20000).lower()
            result.update(http_status=response.status,final_url=response.url)
            result['review_required']=any(v in body for v in (b'captcha',b'cf-chl-',b'access denied',b'just a moment'))
            result['note']='Reachable page only; collection or scan access was not tested.'
    except Exception as error:
        result.update(review_required=True,error=str(error),note='Connection failure is not evidence that the institution or records are absent.')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    p.add_argument('--limit',type=int,default=0)
    a=p.parse_args()
    out=outside_toolkit(a.out)
    archives=read_json(ROOT/'regional-archives/data/archives.json')['archives']
    urls=sorted({a['website_url'] or a['directory_url'] for a in archives}|{s['url'] for s in read_json(ROOT/'resources/sources.json')['sources']})
    if a.limit:urls=urls[:a.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(check,urls))
    write_json(out,{'checks':rows,'catalogue_changed':False})
    print(str(len(rows))+' link observations saved to '+str(out))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
