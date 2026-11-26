"""Build one bundle per seed (repo bundle format, 7 fields) from cached raw evidence. Writes bundles.jsonl + raw/sources.tsv."""
import csv, json, re, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
from nltk.corpus import wordnet as wn
RUN=Path(__file__).resolve().parents[1]; REPO=Path('/workspace/clinical-treatments-and-procedures-lexicon')
seeds=list(csv.DictReader(open(REPO/'data/seeds.tsv',encoding='utf8'),delimiter='\t'))
title2id={s['preferred_name']:s['concept_id'] for s in seeds}
def wd(q):
    f=RUN/'raw'/'wd'/f'{q}.json'
    return json.loads(f.read_text()) if f.exists() else None
def item_claims(e):
    out={}
    for pid,cs in e.get('claims',{}).items():
        vals=[c['mainsnak']['datavalue']['value']['id'] for c in cs
              if c['mainsnak'].get('snaktype')=='value' and isinstance(c['mainsnak'].get('datavalue',{}).get('value'),dict) and 'id' in c['mainsnak']['datavalue']['value'] and str(c['mainsnak']['datavalue']['value']['id']).startswith('Q')]
        if vals: out[pid]=vals
    return out
def lab(e): return e.get('labels',{}).get('en',{}).get('value','')
def als(e): return [a['value'] for a in e.get('aliases',{}).get('en',[])]
def excerpt(t,limit=2500):
    t=re.sub(r'\n+','\n',(t or '')).strip()
    if len(t)<=limit: return t
    cut=t[:limit]; k=max(cut.rfind('. '),cut.rfind('.\n'))
    return cut[:k+1] if k>500 else cut
def wordnet_for(title):
    forms=[title, re.sub(r'\s*\(.*?\)\s*','',title)]
    seen=[]; out=[]
    for f in forms:
        for s in wn.synsets(f.lower().replace(' ','_'),pos=wn.NOUN):
            if s.name() in seen: continue
            seen.append(s.name())
            rel={}
            for k,fn in [('hypernym',s.hypernyms),('hyponym',s.hyponyms),('part_meronym',s.part_meronyms),('part_holonym',s.part_holonyms),('member_meronym',s.member_meronyms),('member_holonym',s.member_holonyms)]:
                v=[x.name() for x in fn()][:15]
                if v: rel[k]=v
            out.append({'synset':s.name(),'lemmas':[l.name().replace('_',' ') for l in s.lemmas()],'gloss':s.definition(),'relations':rel})
    return out
B=open(RUN/'bundles.jsonl','w',encoding='utf8'); src=open(RUN/'raw'/'sources.tsv','w',encoding='utf8')
src.write('concept_id\ttitle_at_fetch\twp_revision_id\twp_rev_timestamp\twp_fetched_utc\twikidata_qid\twd_revision_id\twordnet_synsets\tredirect_or_missing\n')
import sys
LIMIT=int(sys.argv[1]) if len(sys.argv)>1 else len(seeds)
for s in seeds[:LIMIT]:
    p=json.loads((RUN/'raw'/'wp'/f"{s['page_id']}.json").read_text())
    rev=p.get('revisions',[{}])[0]
    wpl=[]
    if rev.get('revid'):
        wpl=[{'title':p['title'],'revision_id':str(rev['revid']),'text':excerpt(p.get('extract',''))}]
    q=p.get('pageprops',{}).get('wikibase_item'); wdl=[]
    e=wd(q) if q else None
    if e:
        wdl.append({'qid':q,'label':lab(e),'aliases':als(e),'claims':item_claims(e),'revision_id':str(e.get('lastrevid',''))})
        added=set()
        for pid in ('P31','P279','P361'):
            for a in wdl[0]['claims'].get(pid,[]):
                ae=wd(a)
                if ae and a not in added:
                    added.add(a)
                    wdl.append({'qid':a,'label':lab(ae),'aliases':als(ae)[:8],'claims':{k:v for k,v in item_claims(ae).items() if k in ('P31','P279','P361')},'revision_id':str(ae.get('lastrevid','')),'ancestor_of':[q]})
    nb=[]; 
    for t in p.get('_links',[]):
        if t in title2id and title2id[t]!=s['concept_id']: nb.append({'id':title2id[t],'name':t})
    wnl=wordnet_for(s['preferred_name'])
    b={'concept_id':s['concept_id'],
       'concept':{'id':s['concept_id'],'preferred_name':s['preferred_name'],'kind':'unclassified','broad_class':'unclassified','variants':[],'relations':[]},
       'neighbors':nb[:40],'examples':[],'wikipedia':wpl,'wikidata':wdl,'wordnet':wnl}
    B.write(json.dumps(b,ensure_ascii=False)+'\n')
    src.write('\t'.join([s['concept_id'],p.get('title',''),str(rev.get('revid','')),rev.get('timestamp',''),p.get('_fetched_utc',''),q or '',wdl[0]['revision_id'] if wdl else '',' '.join(x['synset'] for x in wnl),'redirect' if p.get('redirect') else ('missing' if p.get('missing') else '')])+'\n')
print('bundles',LIMIT)
