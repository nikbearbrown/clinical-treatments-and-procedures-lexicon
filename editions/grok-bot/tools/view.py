"""Print compact drafting view of bundles START..END (0-based, TSV order)."""
import json, sys
from pathlib import Path
RUN=Path(__file__).resolve().parents[1]
a,b=int(sys.argv[1]),int(sys.argv[2]); maxc=int(sys.argv[3]) if len(sys.argv)>3 else 1400
lab={}
for f in (RUN/'raw'/'wd').glob('*.json'):
    e=json.loads(f.read_text()); lab[f.stem]=e.get('labels',{}).get('en',{}).get('value','')
rows=[json.loads(l) for l in open(RUN/'bundles.jsonl')]
for i,r in enumerate(rows[a:b],a):
    print(f"#### [{i}] {r['concept_id']} | {r['concept']['preferred_name']}")
    raw=json.loads((RUN/'raw'/'wp'/(r['concept_id'].split(':')[1]+'.json')).read_text())
    if raw.get('redirect'): print('REDIRECT ->',raw.get('_links'))
    for w in r['wikipedia']: print(f"WP rev {w['revision_id']} ({w['title']}): {w['text'][:maxc]}")
    for d in r['wikidata']:
        if d.get('ancestor_of'): continue
        cl={k:[f"{q}({lab.get(q,'')})" if k in('P31','P279','P361') else q for q in v] for k,v in d['claims'].items() if k in ('P31','P279','P361','P1889','P460','P2175','P366','P2283','P1269','P527')}
        print(f"WD {d['qid']} '{d['label']}' aliases={d['aliases']} {cl}")
    for s in r['wordnet']: print(f"WN {s['synset']} {s['lemmas']}: {s['gloss']} {s['relations'].get('hypernym','')}")
    if r['neighbors']: print("NB:", '; '.join(n['name'] for n in r['neighbors']))
    print()
