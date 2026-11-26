"""Fetch Wikidata items (+P31/P279/P361 targets) for whatever Wikipedia pages are cached so far."""
import json, sys, time, datetime
from pathlib import Path
import requests
RUN=Path(__file__).resolve().parents[1]
S=requests.Session(); S.headers['User-Agent']='HumanitariansAI-ClinicalLexicon-GrokBotRun/1.0 (research; contact via github nikbearbrown)'
WD='https://www.wikidata.org/w/api.php'; wdo=RUN/'raw'/'wd'; wdo.mkdir(exist_ok=True)
def get(params):
    for i in range(10):
        time.sleep(1)
        r=S.get(WD,params=params,timeout=60)
        if r.status_code==200: return r.json()
        print('status',r.status_code,file=sys.stderr); time.sleep(min(120,5*2**i))
    raise RuntimeError('wd fail')
def fetch(qs):
    qs=sorted(q for q in qs if not (wdo/f'{q}.json').exists())
    for i in range(0,len(qs),50):
        d=get(dict(action='wbgetentities',format='json',ids='|'.join(qs[i:i+50]),props='labels|aliases|claims|info',languages='en'))
        for q,e in d.get('entities',{}).items():
            e['_fetched_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            (wdo/f'{q}.json').write_text(json.dumps(e,ensure_ascii=False))
qids={json.loads(f.read_text()).get('pageprops',{}).get('wikibase_item') for f in (RUN/'raw'/'wp').glob('*.json')}-{None}
fetch(qids)
anc=set()
for q in qids:
    e=json.loads((wdo/f'{q}.json').read_text())
    for pid in ('P31','P279','P361'):
        for c in e.get('claims',{}).get(pid,[]):
            v=c['mainsnak'].get('datavalue',{}).get('value')
            if isinstance(v,dict) and 'id' in v: anc.add(v['id'])
fetch(anc); print('items',len(qids),'ancestors',len(anc))
