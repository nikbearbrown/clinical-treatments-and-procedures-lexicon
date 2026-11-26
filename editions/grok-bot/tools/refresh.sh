#!/bin/bash
# rebuild bundles for the contiguous prefix of seeds whose Wikipedia evidence is cached
cd "$(dirname "$0")/.."
N=$(python3 -c "
import csv,os
s=list(csv.DictReader(open('/workspace/clinical-treatments-and-procedures-lexicon/data/seeds.tsv'),delimiter='\t'))
n=0
for r in s:
    if os.path.exists('raw/wp/'+r['page_id']+'.json'): n+=1
    else: break
print(n)")
/workspace/venv-clinlex/bin/python tools/fetch_wd.py >/dev/null && /workspace/venv-clinlex/bin/python tools/build_bundles.py $N
