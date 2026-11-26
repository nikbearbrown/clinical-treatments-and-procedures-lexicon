"""Fetch raw public evidence per seed (Wikipedia API pinned revision, Wikidata entity). Caches in raw/."""
import csv, json, sys, time, datetime
from pathlib import Path
import requests
RUN=Path(__file__).resolve().parents[1]
REPO=Path('/workspace/clinical-treatments-and-procedures-lexicon')
S=requests.Session(); S.headers['User-Agent']='HumanitariansAI-ClinicalLexicon-GrokBotRun/1.0 (research; contact via github nikbearbrown)'
WP='https://en.wikipedia.org/w/api.php'; WD='https://www.wikidata.org/w/api.php'
def get(url,params):
    for i in range(10):
        time.sleep(2.0)
        try:
            r=S.get(url,params=params,timeout=60)
            if r.status_code==200: return r.json()
            print("status",r.status_code,r.text[:200],file=sys.stderr)
        except Exception as e: print('retry',e,file=sys.stderr)
        time.sleep(int(r.headers.get('retry-after',0) or 0) if 'r' in dir() else 0); time.sleep(min(120,5*2**i))
    raise RuntimeError(f'fetch failed {params}')
seeds=list(csv.DictReader(open(REPO/'data/seeds.tsv',encoding='utf8'),delimiter='\t'))
out=RUN/'raw'/'wp'; out.mkdir(parents=True,exist_ok=True)
todo=[s for s in seeds if not (out/f"{s['page_id']}.json").exists()]
for i in range(0,len(todo),20):
    chunk=todo[i:i+20]; ids='|'.join(s['page_id'] for s in chunk)
    d=get(WP,dict(action='query',format='json',formatversion=2,pageids=ids,prop='revisions|pageprops|extracts|info',
        rvprop='ids|timestamp',exintro=1,explaintext=1,exlimit=20,inprop='url'))
    links={}; cont={}
    while True:
        ld=get(WP,dict(action='query',format='json',formatversion=2,pageids=ids,prop='links',plnamespace=0,pllimit='max',**cont))
        for lp in ld['query']['pages']:
            links.setdefault(str(lp['pageid']),[]).extend(l['title'] for l in lp.get('links',[]))
        if 'continue' in ld: cont=ld['continue']
        else: break
    for p in d['query']['pages']:
        pid=str(p['pageid'])
        p['_links']=links.get(pid,[])
        p['_fetched_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (out/f'{pid}.json').write_text(json.dumps(p,ensure_ascii=False))
    print('wp',i+len(chunk),flush=True)
# Wikidata
wdo=RUN/'raw'/'wd'; wdo.mkdir(exist_ok=True)
qids=set()
for s in seeds:
    p=json.loads((out/f"{s['page_id']}.json").read_text())
    q=p.get('pageprops',{}).get('wikibase_item')
    if q: qids.add(q)
def fetch_entities(qs,props='labels|aliases|claims|info'):
    qs=[q for q in qs if not (wdo/f'{q}.json').exists()]
    for i in range(0,len(qs),50):
        d=get(WD,dict(action='wbgetentities',format='json',ids='|'.join(qs[i:i+50]),props=props,languages='en'))
        for q,e in d.get('entities',{}).items():
            e['_fetched_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            (wdo/f'{q}.json').write_text(json.dumps(e,ensure_ascii=False))
fetch_entities(sorted(qids)); print('wd items',len(qids))
anc=set()
for q in qids:
    e=json.loads((wdo/f'{q}.json').read_text())
    for pid in ('P31','P279','P361'):
        for c in e.get('claims',{}).get(pid,[]):
            v=c['mainsnak'].get('datavalue',{}).get('value')
            if isinstance(v,dict) and 'id' in v: anc.add(v['id'])
fetch_entities(sorted(anc-qids)); print('wd ancestors',len(anc))
