"""Expand Grok Bot's compact draft specs (specs/batch-*.py, written by the model) into repo-format drafts.
Pointer shorthands: q:QUOTE -> wp:REV#quote=QUOTE ; a:TEXT -> wd:QID#alias=TEXT ; c:P=Q -> wd:QID#P=Q ;
C:QANC#P=Q -> wd:QANC#P=Q ; l:TEXT -> wn:SYN#lemma=TEXT ; r:REL=SYN -> wn:SYN#REL=SYN. Full pointers pass through.
Writes drafts.jsonl (TSV order, all specced seeds) and progress.json; prints per-seed verifier errors."""
import json, sys, glob, csv, runpy, hashlib, datetime
from pathlib import Path
RUN=Path(__file__).resolve().parents[1]; REPO=Path('/workspace/clinical-treatments-and-procedures-lexicon')
sys.path.insert(0,str(REPO/'replication/scripts'))
from check import check
seeds=[r['concept_id'] for r in csv.DictReader(open(REPO/'data/seeds.tsv',encoding='utf8'),delimiter='\t')]
B={}
for l in open(RUN/'bundles.jsonl',encoding='utf8'):
    if l.strip(): r=json.loads(l); B[r['concept_id']]=r
SYS_SHA=hashlib.sha256((REPO/'replication/prompts/system.txt').read_bytes()).hexdigest()
attempts=json.loads((RUN/'attempts.json').read_text()) if (RUN/'attempts.json').exists() else {}
def expand(p,b,wpc,wdc,wnc):
    k,_,v=p.partition(':')
    if k=='q': return f'wp:{wpc}#quote={v}'
    if k=='a': return f'wd:{wdc}#alias={v}'
    if k=='c': return f'wd:{wdc}#{v}'
    if k=='C': return f'wd:{v}'
    if k=='l': return f'wn:{wnc}#lemma={v}'
    if k=='r': return f'wn:{wnc}#{v}'
    return p
def spec_hash(s): return hashlib.sha256(repr(sorted(s.items())).encode()).hexdigest()
def build(s,batch):
    cid=s['id']; b=B[cid]
    nb={n['name'].casefold():n['id'] for n in b['neighbors']}
    wpcand=b['wikipedia'][0]['revision_id'] if b['wikipedia'] else None
    wdcand=next((d['qid'] for d in b['wikidata'] if not d.get('ancestor_of')),None)
    meta={'model':'Grok Bot','model_string':'unknown (the harness does not expose an exact model string or version)',
          'run_mode':'grounded, independently sourced bundles (Wikipedia pinned revision + Wikidata + WordNet 3.0)',
          'attempt_count':1,'batch':batch,'system_prompt_sha256':SYS_SHA,
          'drafted_utc':s.get('_t') or datetime.datetime.now(datetime.timezone.utc).date().isoformat()}
    if s.get('dup'):
        return {'concept_id':cid,'work_sense':'Duplicate: '+s['dup'],
            'links':{k:{'choice':None,'reason':f'Abstained: the seed page is a duplicate or redirect ({s["dup"]}), so no separate source is linked.'} for k in ('wikipedia','wikidata','wordnet')},
            'definition':{'text':'Out of scope','basis':'model_knowledge','pointers':[]},'variants':[],'relations':[],
            'flags':['duplicate: '+s['dup']]+s.get('f',[]),'_meta':meta}
    if s.get('oos'):
        return {'concept_id':cid,'work_sense':'Out of scope',
            'links':{k:{'choice':None,'reason':s.get(k+'r') or f'Abstained: the seed page has no clinical treatment or procedure sense ({s["oos"]}).'} for k in ('wikipedia','wikidata','wordnet')},
            'definition':{'text':'Out of scope','basis':'model_knowledge','pointers':[]},'variants':[],'relations':[],
            'flags':['out-of-scope: '+s['oos']]+s.get('f',[]),'_meta':meta}
    wpc=wpcand if s.get('wp',True) and wpcand else None
    wdc=wdcand if s.get('wd',True) and wdcand else None
    wnc=s.get('wn')
    links={'wikipedia':{'choice':wpc,'reason':s.get('wpr') or ('The pinned seed article is about this concept.' if wpc else 'No usable Wikipedia candidate in the bundle.')},
           'wikidata':{'choice':wdc,'reason':s.get('wdr') or ('The Wikidata item attached to the seed article matches this sense.' if wdc else ('No Wikidata item in the bundle.' if not wdcand else 'Abstained.'))},
           'wordnet':{'choice':wnc,'reason':s.get('wnr') or ('This synset matches the sense.' if wnc else ('No WordNet synset in the bundle.' if not b['wordnet'] else 'Abstained: no bundle synset matches the clinical sense.'))}}
    E=lambda ps:[expand(p,b,wpc,wdc,wnc) for p in ps]
    dp=E(s.get('dp',[]))
    var=[{'text':t,'condition':c,'basis':'source' if ps else 'model_knowledge','pointers':E(ps)} for t,c,ps in s.get('v',[])]
    rel=[]
    for t,lbl,ps,note in s.get('r',[]):
        tid=nb.get(lbl.casefold())
        rel.append({'type':t,'target_label':lbl,'target_id':tid,'proposed_new':tid is None,'basis':'source' if ps else 'model_knowledge','pointers':E(ps),'note':note})
    return {'concept_id':cid,'work_sense':s['ws'],'links':links,
            'definition':{'text':s['d'],'basis':'source' if dp else 'model_knowledge','pointers':dp},
            'variants':var,'relations':rel,'flags':s.get('f',[]),'_meta':meta}
D={}; bad=0
for f in sorted(glob.glob(str(RUN/'specs'/'batch-*.py'))):
    batch=Path(f).stem
    for s in runpy.run_path(f)['E']:
        if s['id'] in D: print('DUP SPEC',s['id']); bad+=1
        e=build(s,batch); D[s['id']]=e
        errs,warns=check(e,B[s['id']])
        prev=attempts.get(s['id'])
        if errs:
            bad+=1; print('FAIL',s['id'],errs)
            if any('copies' in x for x in errs):
                from verify_drafts import ngrams
                src=set().union(*[ngrams(w['text'],9) for w in B[s['id']]['wikipedia']])
                print('   COPIED:',[' '.join(g) for g in ngrams(e['definition']['text'],9)&src][:3])
        if errs and prev is None: attempts[s['id']]={'n':1,'failing':True}
        elif isinstance(prev,dict) and prev.get('failing') and spec_hash(s)!=prev.get('h'): attempts[s['id']]={'n':prev['n']+1,'failing':bool(errs)}
        if isinstance(attempts.get(s['id']),dict): attempts[s['id']]['h']=spec_hash(s); e['_meta']['attempt_count']=attempts[s['id']]['n']
(RUN/'attempts.json').write_text(json.dumps(attempts,indent=1))
with open(RUN/'drafts.jsonl','w',encoding='utf8') as out:
    for cid in seeds:
        if cid in D: out.write(json.dumps(D[cid],ensure_ascii=False)+'\n')
done=[c for c in seeds if c in D]
(RUN/'progress.json').write_text(json.dumps({'seeds_total':len(seeds),'drafted':len(done),'failing':bad,
   'next_index':next((i for i,c in enumerate(seeds) if c not in D),None),'spec_files':sorted(Path(f).name for f in glob.glob(str(RUN/'specs'/'batch-*.py'))),
   'updated':datetime.datetime.now().isoformat(timespec='seconds')},indent=1))
print(f'drafted {len(done)}/{len(seeds)}; failing {bad}')
