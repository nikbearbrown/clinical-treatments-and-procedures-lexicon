# Grok Bot independent edition: Clinical Treatments and Procedures Lexicon

Run folder: `/workspace/clinical-lexicon-grok-run-20261124/` (private; outside the checkout; not pushed or published).

## Model
- Model: **Grok Bot**
- Exact model string / version: **unknown**. The harness does not show an exact model string or version, so none is recorded or guessed. The same value is in every draft's `_meta.model_string`.
- Mode: grounded, using independently sourced bundles (pinned Wikipedia revision, Wikidata and WordNet 3.0).

## Seeds
- Repository: `nikbearbrown/clinical-treatments-and-procedures-lexicon`, branch `main`, commit **588a9866dc42744cecf7ab3789551ab5869687e4** ("Initialize direct-member lexicon and blind replication kit").
- `data/seeds.tsv` sha256 **5ee2167938f2a521e5f35e7a49deceb2e05ea3798384971bd2eb1492b4c223db**. This matches `data/source-manifest.json`, which records 354 seeds and no duplicate IDs. The seed list was retrieved 2026-11-24 at 3:52–3:53 PM EST (20:52–20:53 UTC).
- Every one of the 354 seeds has exactly one record, under its original `concept_id`, in TSV order. No subcategory pages were added and no seed was dropped.
- System prompt used as the drafting rules: `replication/prompts/system.txt`, sha256 f782dda691a0f4d516a02b29de742260dccc56f67cbfa917700b8633896bffd6.

## Sources (fetched 2026-11-24, 4:18–4:38 PM EST / 21:18–21:38 UTC)
- **Wikipedia** (en.wikipedia.org/w/api.php):
  - Fetched by pageid, with the exact `revision_id` pinned per seed in `bundles.jsonl` and `raw/sources.tsv`. Pinned revisions are dated from 2013-06-06 to 2026-11-24 (UTC revision timestamps).
  - Lead extract with `exintro` and plain text, capped at 2,500 characters. Out-link titles were used to compute `neighbors`, keeping only links to other seeds, at most 40.
  - Raw API JSON is cached in `raw/wp/<pageid>.json`.
  - 16 seeds are redirect pages, kept as their own redirect revisions. One seed, Outpatient parenteral antibiotic therapy (enwiki:56425833), has an empty lead, so the full-page extract of the same pinned revision 1372811343 was used instead (`_extract_note`).
- **Wikidata**:
  - Items come from the page's `wikibase_item`; 345 of 354 seeds have one.
  - Ancestors were collected along P31, P279 and P361 (`ancestor_of`).
  - 559 entity JSONs, each with its `lastrevid`, are cached in `raw/wd/`. The item revision for each seed is listed in `raw/sources.tsv`.
- **WordNet 3.0**: noun synsets for the seed title via nltk's WordNet corpus (38 seeds have any synset). The corpus was downloaded from the nltk_data GitHub repository into `/home/box/nltk_data`.
- No patient records and no other model's drafts, branches or `data/lexicon-parallel` were read.

## Method
1. `tools/fetch.py` and `tools/fetch_wd.py` fetch and cache sources, with a polite User-Agent, 2 s spacing and backoff on HTTP 429. `tools/build_bundles.py` writes the 7-field bundles in the repo format.
2. **Pilot**: seeds 1–10 were drafted first and checked with `check.py`; all 10 passed (`raw/pilot-report.jsonl`).
3. **Drafting**: Grok Bot drafted every record itself, following `system.txt` and `instructions.md`.
   - It worked in 24 batches of about 14–16 seeds, from compact views of each bundle (`tools/view.py`), writing compact specs in `specs/batch-NNN.py`.
   - `tools/assemble.py` expands the specs into the exact gen-v2 JSON format. It sets `basis` (source if pointers, else model_knowledge), resolves `target_id` and `proposed_new` against the bundle's neighbors, and adds `_meta`.
   - It runs the repo's verifier on each draft, writes `progress.json` (resumable) and counts attempts (`attempts.json`).
4. Pointers use the repo formats `wp:REV#quote=` (verbatim, at most 20 words), `wd:QID#P=Q`, `wd:QID#alias=` and `wn:SYNSET#lemma=` / `#hypernym=`.
5. **Scope**:
   - Pages that are not treatments or procedures (biographies, organisations, places, businesses, lists, timelines, research overviews, conditions or states, outcomes, sayings, substances or materials, theories, education) are recorded in the repo's out-of-scope format.
   - Redirect seeds are recorded as **duplicate** abstentions that name the redirect target.
   - Devices, drug products or classes, diagnostic procedures, umbrella "Treatment/Management of…" articles and similar borderline pages are entries with an `ambiguous:` flag.
6. **Descriptive only**: definitions say what a treatment or procedure is. They give no performing steps, doses or recommendations, and include composition details only where these are the definition itself; for example, the Semper solution's concentrations were deliberately left out.
7. **Agreement-method compatibility**: the drafts are plain gen-v2 objects, which `replication/scripts/agreement.py` (`canon_genv2`) in the agreement kit reads directly. Definition, variants (aliases/synonyms with conditions) and relations (typed, with target ids where resolvable) can each be judged per concept_id.

### Deviations from replication/README.md
- **Shared drafting context**: messages were not rendered with `render.py` and sent one per seed to a fresh model context. Grok Bot, the agent running this job, drafted in batches within one working session, so the seeds in a batch were seen together. No other model was used to draft or judge.
- **Copy guard**: when the verifier's copy guard (9 or more consecutive words from Wikipedia) or a quote check failed, the definition was reworded and re-verified. 330 drafts passed on attempt 1 and 24 needed attempt 2.
- **Bundle sizes**: neighbors come from article out-links restricted to seeds, at most 40. Lead text is capped at 2,500 characters.
- **WordNet**: WordNet is the nltk copy of 3.0, not 3.1.

## Results
- Records: **354/354**.
  - **312 entries**. Of these, 104 carry an `ambiguous:` flag and 2 carry a `duplicate:` flag because Wikidata marks them as duplicate items (Bacteriotherapy, Electrotherapeutics).
  - **26 out-of-scope** flags.
  - **16 duplicate** abstentions (redirect pages).
- `python3 replication/scripts/check.py bundles.jsonl drafts.jsonl report.jsonl` gives **354/354 seeds passed**, with 0 errors (`raw/check-final.txt`).
  - 54 records carry the warning "most claims rest on model knowledge": the 42 abstentions, which by format have no pointers, plus 12 entries.
- sha256:
  - bundles.jsonl c6b0fdbbd66ae72922f827a20f272c56eafda7c1296ae8d245c6f00b9b0faa50
  - drafts.jsonl 9aa0e6d092592306ba2cc39ecc4f6144eeb2128e125b268366e14393de6e1703
  - report.jsonl 26ca5010300dbd7b14b58a00b1cec9c736537bc5534c8c07889385ce092d97d0

## Unresolved issues
All flags are listed machine-readably in `raw/flags.tsv` (198 flags).

### Abstentions (out-of-scope and duplicate redirects)
| concept_id | title | flag |
|---|---|---|
| enwiki:27943180 | Alternative uses for placenta | out-of-scope: survey article on non-obstetric uses of the placenta (ritual consumption, product extracts, training search dogs), not a single treatment or procedure concept |
| enwiki:36105574 | Androgen deficiency | out-of-scope: names a medical condition (insufficient androgen activity), not a treatment or procedure; the treatment sense is covered by the separate seed Androgen replacement therapy |
| enwiki:35353665 | Barometric pressure therapy | duplicate: redirect page to the seed Hyperbaric medicine (pinned redirect revision 558567870) |
| enwiki:8999379 | Bioartificial liver device | duplicate: redirect page to the seed Liver support system (pinned redirect revision 996087594); Wikidata still has a separate item Q3742039 for bioartificial liver devices |
| enwiki:71725016 | Collusion (psychology) | out-of-scope: psychological concept of collusive relationship patterns and therapist non-neutrality, not a treatment or procedure |
| enwiki:75124737 | Crenotherapy | duplicate: redirect page to Balneotherapy (pinned redirect revision 1309396289); Wikidata keeps a separate crenotherapy item Q1727131; Balneotherapy is not checked here as a seed |
| enwiki:28936 | Cyanoacrylate | out-of-scope: family of chemical adhesives with industrial, household and medical uses; a material, not a treatment or procedure (its medical use as tissue adhesive is only one application) |
| enwiki:4219967 | Day spa | out-of-scope: a type of business offering personal-care services, not a treatment or procedure |
| enwiki:44217965 | Doctor's orders | duplicate: redirect page to the seed Medical prescription (pinned redirect revision 678165194) |
| enwiki:6420325 | Douglas Sadownick | out-of-scope: biography of a person (writer, activist and psychotherapist), not a treatment or procedure |
| enwiki:72931373 | Feed a cold, starve a fever | out-of-scope: folk adage about eating during illness, not a treatment or procedure |
| enwiki:73208456 | Ghost surgery | out-of-scope: names a fraudulent practice in which an unauthorized person substitutes for the credited surgeon, not a treatment or procedure type |
| enwiki:73208456 | Ghost surgery | ambiguous: medical-ethics term; could be kept in a broader clinical vocabulary |
| enwiki:239217 | Healing | out-of-scope: names the biological repair process of tissues and organs, not an intervention or procedure |
| enwiki:239217 | Healing | ambiguous: Wikidata subclasses healing under health care |
| enwiki:52857868 | Hyperbaric oxygen treatment | duplicate: redirect page to the seed Hyperbaric medicine (pinned redirect revision 1347464868) |
| enwiki:74237154 | Hyperbaric oxygen treatment table | duplicate: redirect page to the seed Hyperbaric treatment schedules (pinned redirect revision 1347464873) |
| enwiki:72499506 | Hyperbaric treatment | duplicate: redirect page to the seed Hyperbaric medicine (pinned redirect revision 1347464880) |
| enwiki:67708367 | Hyperbaric treatment schedule | duplicate: redirect page to the seed Hyperbaric treatment schedules (pinned redirect revision 1347464887) |
| enwiki:51189925 | Hyperbaric treatment tables | duplicate: redirect page to the seed Hyperbaric treatment schedules (pinned redirect revision 1347464901) |
| enwiki:31661142 | Hyperimmune globulin | duplicate: redirect page to the seed Immunoglobulin therapy (pinned redirect revision 1384889098) |
| enwiki:72257559 | Internet intervention | duplicate: redirect page to EHealth (pinned redirect revision 1387101101); EHealth is not checked here as a seed |
| enwiki:72257559 | Internet intervention | Wikidata keeps a separate item Q115917352 for internet intervention |
| enwiki:4544090 | Interprofessional education | out-of-scope: names a form of health-professional education, not a treatment or procedure |
| enwiki:29790 | List of therapies | out-of-scope: Wikipedia list article of therapies, not a single concept |
| enwiki:50990100 | Lundh's test | duplicate: redirect page to Exocrine pancreatic insufficiency (pinned redirect revision 1383003238); the target is not checked here as a seed |
| enwiki:50990100 | Lundh's test | Wikidata keeps a separate item Q25350140 for Lundh's test (a diagnostic test) |
| enwiki:41344951 | Magnesium and depression | duplicate: redirect page to Magnesium deficiency (pinned redirect revision 1383423414); the target is a condition and is not checked here as a seed |
| enwiki:676718 | Medical tourism | out-of-scope: practice of travelling abroad to obtain treatment; a health-services and travel phenomenon, not a treatment or procedure |
| enwiki:78825235 | Neurotherapy | duplicate: redirect page to Neuromodulation (medicine) (pinned redirect revision 1364768743); the target is not checked here as a seed |
| enwiki:78825235 | Neurotherapy | Wikidata keeps a separate item Q131726203 for neurotherapy; other seeds (Electroanalgesia, Electromagnetic therapy) describe themselves as types of neurotherapy |
| enwiki:3474537 | Optometric Extension Program | out-of-scope: a professional organization (the Optometric Extension Program Foundation), not a treatment or procedure |
| enwiki:55882601 | Proceduralist | out-of-scope: names a type of physician who performs procedures, not a treatment or procedure |
| enwiki:25087021 | Pumpable ice technology | out-of-scope: the pinned article describes an industrial ice-slurry cooling technology; no clinical treatment or procedure sense is stated |
| enwiki:25087021 | Pumpable ice technology | ambiguous: may have been categorised for medical cooling uses not described in the pinned lead |
| enwiki:5827094 | Remission (medicine) | out-of-scope: names a disease state (reduction or disappearance of signs and symptoms), not a treatment or procedure |
| enwiki:44942023 | Research in management of Ebola | out-of-scope: overview of research into Ebola treatments, not a single treatment or procedure |
| enwiki:13033422 | Research in multiple sclerosis | out-of-scope: overview of multiple sclerosis research (Wikidata: list article), not a single treatment or procedure |
| enwiki:61091006 | Screening, brief intervention and referral to treatment | duplicate: redirect page to Brief intervention (pinned redirect revision 1384645501); the target is not checked here as a seed |
| enwiki:61091006 | Screening, brief intervention and referral to treatment | Wikidata keeps a separate item Q65049697 (SBIRT) classed as a public health intervention |
| enwiki:14296441 | Skunk oil | out-of-scope: names an animal-derived substance (oil from skunk glands); the pinned lead describes no treatment or procedure |
| enwiki:65290378 | Sleep Deprivation Therapy | duplicate: redirect page to Wake therapy (pinned redirect revision 1177900387); the target is not a separate seed but the redirect title is preserved here as an abstention |
| enwiki:65290378 | Sleep Deprivation Therapy | no Wikidata item on the redirect page |
| enwiki:13406038 | Social interaction approach | out-of-scope: a theory of language development, not a treatment or procedure |
| enwiki:1636042 | Spa | out-of-scope: names a place or business (spa) where treatments are given, not a treatment; the treatment sense is balneotherapy |
| enwiki:1636042 | Spa | ambiguous: WordNet senses are resort/hotel/health club |
| enwiki:3727311 | Therapeutic effect | out-of-scope: names an outcome of treatment (a favourable response), not a treatment or procedure |
| enwiki:52077650 | Timeline of cancer treatment development | out-of-scope: a timeline article (Wikidata: timeline) about the history of cancer treatment, not a treatment or procedure |
| enwiki:12763409 | Turning Point (charity) | out-of-scope: an organisation (charitable health and social care provider), not a treatment or procedure |
| enwiki:43182278 | VAGA | out-of-scope: an organisation (artists collective focused on art therapy), not a treatment or procedure |
| enwiki:65632796 | Ville Sbertoli | out-of-scope: a former psychiatric hospital (place), not a treatment or procedure |

### Flags on entries (ambiguous scope, Wikidata/source conflicts, link caveats)
| concept_id | title | flag |
|---|---|---|
| enwiki:35026040 | Abscopal effect | ambiguous: names a treatment-response phenomenon rather than an intervention or procedure itself |
| enwiki:63579244 | Aerosol-generating procedure | ambiguous: the designation is agency-specific and the source notes it is increasingly at odds with current understanding of airborne transmission |
| enwiki:63687773 | Age management medicine | ambiguous: seed title is age management medicine but the pinned article leads with longevity medicine; the two may not be the same concept |
| enwiki:22717670 | Aguamiel | ambiguous: primarily a plant sap and beverage; treatment sense rests on traditional use, not an established clinical intervention |
| enwiki:73401926 | Antrectomy | Wikidata item Q121734532 is typed as an instance of disease (Q12136), which looks like an error for a surgical procedure |
| enwiki:56363317 | Aquablation therapy | conflicting sources: Wikidata classes it as a minimally-invasive procedure (P279 Q1755504) while the article says it is not categorized as minimally invasive |
| enwiki:79741102 | B52 (medical treatment) | ambiguous: slang name whose digits encode doses; the string B52 has many unrelated senses |
| enwiki:41403522 | Bacteriotherapy | duplicate: Wikidata marks this article item as a Wikimedia duplicated page; may overlap another article |
| enwiki:75212947 | Balloon Eustachian tuboplasty | Wikidata types the item as an instance of angioplasty (Q539795), which normally refers to blood vessels |
| enwiki:2971357 | Banding (medical) | ambiguous: article also covers veterinary elastration of livestock |
| enwiki:14475526 | Bathroom privileges | ambiguous: the page also covers school and workplace senses; only the clinical-order sense is drafted, and it is an order rather than a treatment |
| enwiki:15017463 | Bidirectional Glenn procedure | Wikidata lists hemi-Fontan as an alias; surgically it is a related but distinct operation |
| enwiki:6216692 | Bone cement | ambiguous: a material used in procedures rather than a treatment or procedure itself |
| enwiki:25081142 | Cancer treatment | ambiguous: Wikidata alias "cancer care" is broader than treatment |
| enwiki:46246338 | CAREN | ambiguous: names a proprietary device system rather than a generic procedure; the expanded name is not stated in the excerpt |
| enwiki:5371837 | Catholicon (electuary) | ambiguous: historical remedy, not a current treatment |
| enwiki:6877491 | Celacade | ambiguous: proprietary, discontinued product name |
| enwiki:1419730 | Chest wall oscillation | Wikidata alias "Chest compression" conflicts with the CPR sense of that term |
| enwiki:47401821 | Chondroprotection | ambiguous: the seed names an effect (chondroprotection) while the article and Wikidata describe a class of compounds |
| enwiki:31270321 | Clinical uses of mesenchymal stem cells | ambiguous: topic article grouping several uses rather than one named procedure |
| enwiki:493716 | Cranial electrotherapy stimulation | Wikidata alias "Transcranial alternating current stimulation" may conflate two techniques |
| enwiki:14245489 | Craterization | ambiguous: the page also uses the term for crater formation after explosions and in volcanoes |
| enwiki:26411203 | Credé's maneuver | ambiguous: same eponym names a bladder-emptying technique and an obstetric placenta-expulsion technique (and, elsewhere, Credé prophylaxis for newborn eyes) |
| enwiki:39935833 | Cryolipolysis | Wikidata aliases "Cryolipologist" and "Cryolipolysis Technician" name practitioners, not the procedure |
| enwiki:22791521 | Culdoscopy | Wikidata types the procedure as an instance of medical device type, which looks like an error |
| enwiki:16767087 | Cure | ambiguous: the page covers both the outcome (being cured) and the agent (a cure); Wikidata item is labelled remedy |
| enwiki:69137517 | De Simone Formulation | ambiguous: a specific proprietary product formula rather than a generic treatment |
| enwiki:878519 | Directly observed treatment, short-course | ambiguous: names a public-health control strategy rather than a single treatment |
| enwiki:1999674 | Diversional therapy | ambiguous: country-specific (Australian) professional term |
| enwiki:44517156 | Dopamine therapy | likely source error: the article describes dopamine antagonists as compounds that activate dopamine receptors (that describes agonists) |
| enwiki:5262451 | Drug of last resort | Wikidata also subclasses it under antibiotic (Q12187), which is too narrow |
| enwiki:25970819 | Drug therapy problems | ambiguous: names a classification of medication-related problems, not a treatment or procedure |
| enwiki:10173852 | Dry-powder inhaler | ambiguous: a drug-delivery device rather than a treatment or procedure itself |
| enwiki:22551311 | Electroanalgesia | Wikidata subclasses it under TENS (Q142091); TENS is better seen as one form of electroanalgesia |
| enwiki:67487128 | Electrochemical skin conductance | ambiguous: a diagnostic measurement rather than a treatment |
| enwiki:72262401 | Electrohydraulic lithotripsy | ambiguous: EHL is also widely used intracorporeally via endoscopes, while the article frames it as extracorporeal |
| enwiki:22816756 | Electromagnetic therapy | ambiguous: the page partly works as a disambiguation listing evidence-based and alternative-medicine senses |
| enwiki:4001248 | Electrotherapeutics | duplicate: same concept as the seed Electrotherapy; Wikidata marks this item a permanent duplicate |
| enwiki:4001248 | Electrotherapeutics | the pinned article contains outdated technical working instructions, which were not used |
| enwiki:58582221 | Endomyocardial biopsy | ambiguous: diagnostic procedure rather than treatment |
| enwiki:50777212 | Enterostomy | ambiguous: names both the operation and the resulting stoma |
| enwiki:50777212 | Enterostomy | WordNet lists enterotomy as a lemma of the same synset; enterotomy usually means an incision into the intestine |
| enwiki:44897758 | Ex vivo reconstruction | ambiguous: the generic title ex vivo reconstruction could apply to other organs; the page covers only the renal sense |
| enwiki:11072059 | Expiratory apnea | ambiguous: names a physiological state and examination manoeuvre, not a treatment |
| enwiki:8726400 | Extracorporeal shockwave therapy | ambiguous: covers both lithotripsy and musculoskeletal shockwave therapy, which some sources treat as separate concepts |
| enwiki:74418190 | Faradic battery | ambiguous: a historical device rather than a treatment |
| enwiki:3762041 | Fecal microbiota transplant | Wikidata alias "inpoosion" is a slang coinage |
| enwiki:14673089 | Feminizing hormone therapy | Wikidata alias "MTF" names the transition direction rather than the therapy |
| enwiki:52159046 | Flea treatments | ambiguous: largely veterinary; the term also names products as well as procedures |
| enwiki:301110 | Fluid replacement | Wikidata subclasses fluid replacement under pharmacotherapy (Q701216), which is questionable |
| enwiki:338082 | Gastric intubation | ambiguous: the seed title is gastric intubation but the pinned article is about nasogastric intubation; Wikidata alias "nasogastric tube" names the device |
| enwiki:36228151 | Grinberg Method | ambiguous: described as a teaching method, not a clinical treatment |
| enwiki:1488293 | Heating pad | ambiguous: a device used in heat therapy rather than a treatment itself |
| enwiki:38010 | Heliox | ambiguous: names a gas mixture; its diving use is outside clinical scope |
| enwiki:82533358 | Hidaklon | ambiguous: a traditional system of medicine rather than a single treatment |
| enwiki:3015816 | Hot water bottle | ambiguous: a household object used for heat application rather than a treatment |
| enwiki:70932327 | Human bake oven | ambiguous: an obsolete apparatus/treatment of historical interest only |
| enwiki:53138539 | Hydrogel dressing | ambiguous: a wound-care product rather than a treatment or procedure |
| enwiki:37114476 | Hydrogogue | ambiguous: names a class of substances rather than a treatment or procedure |
| enwiki:326490 | Hyperbaric medicine | ambiguous: names both a medical specialty and the treatment it delivers; several redirect seeds point here |
| enwiki:47411772 | Hyperbaric treatment schedules | several redirect seeds (treatment table, schedule, tables) point to this concept |
| enwiki:14417 | Hypnosis | ambiguous: names a mental state rather than a treatment; the treatment sense is the seed Hypnotherapy |
| enwiki:2420839 | Ice pack | ambiguous: a device used for cold therapy rather than a treatment itself |
| enwiki:168944 | Immunosuppression | ambiguous: names both a state (reduced immunity, including side effects) and a deliberate treatment; WordNet places it under immunological disorder |
| enwiki:47908493 | In-depth-systemics | ambiguous: a niche professional approach; the article describes it as context independent rather than clinical |
| enwiki:32173049 | Inferior petrosal sinus sampling | ambiguous: diagnostic rather than therapeutic procedure |
| enwiki:49999342 | Intermittent hypoxia | ambiguous: the same term names a harmful physiological pattern (e.g. in sleep apnoea) as well as the intervention |
| enwiki:1958802 | Interventionism (medicine) | ambiguous: an evaluative term about a care philosophy, not a treatment |
| enwiki:25284347 | Intradermal injection | Wikidata subclasses intradermal injection under subcutaneous injection (Q2035485), which conflicts with anatomy |
| enwiki:178769 | Intravenous therapy | Wikidata labels the item "intravenous infusion and defusion" and lists "perfusion" as an alias, which is a different concept |
| enwiki:62474511 | Invasive test | the source lists excision and cryotherapy as examples of tests, which are usually treatments |
| enwiki:73590840 | Invasomes | ambiguous: a drug-delivery vehicle rather than a treatment or procedure |
| enwiki:29095970 | Kraamzorg | ambiguous: country-specific service; the Wikidata item is the broader concept "maternity care" |
| enwiki:68469 | Laparoscopy | WordNet hypernym laparotomy conflicts with usual usage |
| enwiki:1836020 | Laser ablation | ambiguous: the pinned article describes the general physical process; the medical sense is not described in the excerpt |
| enwiki:22191268 | LILFU | ambiguous: experimental research technique, mainly tested in animals |
| enwiki:45031863 | Liquid biopsy | ambiguous: diagnostic rather than therapeutic procedure |
| enwiki:863712 | Liquid breathing | ambiguous: largely experimental; Wikidata classes it as a hypothetical technology |
| enwiki:74836167 | Maibaron | ambiguous: a traditional system of healing rather than a single treatment |
| enwiki:18291303 | Malotilate | ambiguous: names an investigational drug substance rather than a treatment or procedure |
| enwiki:6180485 | Management of Crohn's disease | ambiguous: an umbrella topic article rather than one procedure |
| enwiki:7663818 | Management of multiple sclerosis | ambiguous: an umbrella topic article rather than one procedure |
| enwiki:51305509 | Management of scoliosis | ambiguous: an umbrella topic article rather than one procedure |
| enwiki:48107460 | Management of strabismus | ambiguous: an umbrella topic article rather than one procedure |
| enwiki:33212628 | Medical gas therapy | Wikidata alias "gasocrinology" names a research field, not the therapy |
| enwiki:304263 | Medical prescription | ambiguous: an authorisation document rather than a treatment or procedure |
| enwiki:59516003 | Micropore particle technology | ambiguous: a wound-care material technology rather than a treatment or procedure |
| enwiki:1862494 | Mirror therapy | Wikidata alias "mirror box" names the apparatus |
| enwiki:35001508 | Mydicar | conflicting sources: the article and Wikidata call Mydicar an enzyme replacement therapy, although it delivers a gene (gene therapy) |
| enwiki:2105523 | Myolysis | ambiguous: also names pathological muscle breakdown; Wikidata classes it as tissue damage |
| enwiki:1243042 | Nasal spray | ambiguous: a dosage form rather than a treatment or procedure |
| enwiki:56587867 | Nature therapy | source aliases "grounding" and "earthing" name a narrower, distinct practice |
| enwiki:50914828 | NDR Method | ambiguous: a proprietary trademarked protocol; the page reads promotionally |
| enwiki:57665889 | Non-contact normothermic wound therapy | the source gives "nonthermal" as an alternative to "normothermic", which looks inconsistent |
| enwiki:2768512 | Optoelectronic plethysmography | ambiguous: a measurement method rather than a treatment |
| enwiki:1558567 | Oral rehydration therapy | Wikidata alias "they give you bad bacteria" appears to be vandalism |
| enwiki:42758445 | PAIR (puncture-aspiration-injection-reaspiration) | source describes PAIR as noninvasive although it is a percutaneous (minimally invasive) procedure |
| enwiki:3496191 | Pastille | ambiguous: a dosage form/confection, and the term also names incense pellets; not a treatment or procedure |
| enwiki:59041435 | Pelvic massage | ambiguous: historical treatment |
| enwiki:12359827 | Pentastarch | ambiguous: names a substance used in treatment rather than a treatment or procedure |
| enwiki:11333093 | Pfannenstiel incision | Wikidata types the incision as an instance of caesarean section and a subclass of birth, which looks like an error |
| enwiki:3259830 | Pharmacological chaperone | ambiguous: a drug class rather than a treatment or procedure |
| enwiki:51934343 | Photopharmacology | ambiguous: a research field rather than a treatment |
| enwiki:11693664 | Photothermal therapy | source calls photothermal therapy a neurotherapy, which seems mistaken |
| enwiki:8340113 | Pink lady (medicine) | ambiguous: slang name with unrelated senses (cocktail) |
| enwiki:44476833 | Plasma needling | ambiguous: cosmetic procedure with claims the source frames as purported |
| enwiki:2728236 | Pneumotherapy | ambiguous: largely historical term |
| enwiki:2508123 | Poultice | WordNet lemma "plaster" is broader than poultice |
| enwiki:25045060 | Prevention of migraine attacks | ambiguous: topic article covering many preventive treatments |
| enwiki:40841128 | Prophylactic cranial irradiation | Wikidata subclasses it under radiation oncology (a specialty) rather than radiation therapy |
| enwiki:22656751 | Proteases (medical and related uses) | ambiguous: topic article on uses of an enzyme class, not one treatment |
| enwiki:12304171 | Protein replacement therapy | Wikidata item is labelled "Protein therapy", which is broader |
| enwiki:74221549 | Psychedelic retreat | ambiguous: a commercial or wellness programme rather than a clinical treatment |
| enwiki:30427095 | Quaternary prevention | Wikidata subclasses it under "patient" and "health risk", which look like errors |
| enwiki:80370311 | Recitation over water | ambiguous: a religious rite with folk-healing uses, not a clinical treatment |
| enwiki:12842385 | Respimat | ambiguous: a proprietary device rather than a treatment or procedure |
| enwiki:19202113 | Revalenta arabica | ambiguous: a historical quack product rather than a treatment |
| enwiki:19202113 | Revalenta arabica | possible source date error: the product is usually dated to the 19th century, the article says 18th |
| enwiki:36737883 | Rose position | ambiguous: a positioning term used within procedures rather than a procedure itself |
| enwiki:21488622 | Self-administration | ambiguous: also an animal-research paradigm |
| enwiki:37204951 | Semper rehydration solution | ambiguous: a specific preparation rather than a treatment; composition details omitted deliberately |
| enwiki:31218265 | Sensory room | ambiguous: a therapeutic environment rather than a treatment |
| enwiki:54654085 | Smit sleeve | ambiguous: a medical device rather than a treatment or procedure |
| enwiki:5778180 | Sociotherapy | ambiguous: described both as a discipline and as a therapy |
| enwiki:36264089 | Sonodynamic therapy | Wikidata item label "Sono photo dynamic therapy" names a combined modality; link may be imprecise |
| enwiki:2180102 | Tamagozake | ambiguous: a beverage used as a folk remedy rather than a clinical treatment |
| enwiki:2358970 | Tamponade | ambiguous: the word also names pathological compression (e.g. cardiac tamponade) |
| enwiki:69607361 | Therapeutic interfering particle | ambiguous: an agent or preparation rather than a treatment |
| enwiki:1539123 | Thickened fluids | ambiguous: a dietary modification/product rather than a procedure |
| enwiki:21093002 | Thyroid blocker | ambiguous: names a use of drugs rather than a procedure |
| enwiki:3930866 | Time delay toxin activation | pinned revision is old (2021) and thinly sourced; the concept may be non-mainstream |
| enwiki:82884049 | Tividenofusp alfa | ambiguous: a specific drug product rather than a treatment type |
| enwiki:146396 | Tracheal intubation | Wikidata English label is malformed ("tracheal intubation g") and aliases are Spanish; aliases not used |
| enwiki:3233638 | Traction splint | ambiguous: a device rather than a procedure |
| enwiki:5004685 | Transcranial direct-current stimulation | Wikidata alias "pulsed electromagnetic field therapy" names a different modality; not used |
| enwiki:3749250 | Transillumination | ambiguous: a diagnostic or imaging technique rather than a treatment |
| enwiki:56926042 | Treatment and management of addiction | ambiguous: umbrella topic article rather than a single treatment |
| enwiki:2348583 | Treatment of human lice | ambiguous: umbrella topic article rather than a single treatment |
| enwiki:4615904 | Treatment of influenza | ambiguous: umbrella topic article rather than a single treatment |
| enwiki:55742304 | Treatment of Rett syndrome | ambiguous: umbrella topic article rather than a single treatment |
| enwiki:76556199 | Urinary anti-infective agent | ambiguous: a drug class rather than a treatment or procedure |
| enwiki:32487739 | Video self-modeling | ambiguous: an educational/behavioural technique not exclusively clinical |
| enwiki:4949370 | Virtual reality therapy | Wikidata item is "virtual reality exposure therapy", a narrower sense; source also lists computerized CBT as a synonym, which is broader/different |
| enwiki:28975429 | VZV immune globulin | ambiguous: a medication rather than a procedure |
| enwiki:39327248 | Well-woman examination | ambiguous: an examination (diagnostic/screening) rather than a treatment |
| enwiki:39327248 | Well-woman examination | Wikidata item is "intimate examination", which is broader |
| enwiki:40757483 | Zinc and the common cold | ambiguous: topic article about a supplement's use rather than a named procedure |

### Other open points
- **Redirect targets that are not seeds**: Balneotherapy, EHealth, Exocrine pancreatic insufficiency, Magnesium deficiency, Neuromodulation (medicine), Brief intervention and Wake therapy are not in the seed list. A reviewer should decide whether the redirect seeds map to new concepts.
- **Wikidata data-quality problems** found in passing and not used as evidence, for example:
  - vandal or foreign-language labels and aliases (Tracheal intubation);
  - wrong aliases (tDCS alias "pulsed electromagnetic field therapy");
  - items of the wrong type (Antrectomy typed as a disease; Quaternary prevention subclassed under "patient").
- **Model version**: the exact model version is unknown (see above).

## Agreement kit (separate from this run)
The IHWL judging kit was ported to the clinical repo on the new branch `grok-agreement-method`, cut from main at 588a9866 and pushed as commit 51774fbd8385e6595e52fa28cf3f59bb20bd83e4 under the author nikbearbrown. No drafts or outputs from this run are on that branch. These drafts load into it unchanged with `--edition grok=gen-v2:<path>/drafts.jsonl`. A smoke test in /tmp with a synthetic second edition exercised run, join, self-exclusion, export-packet, import, validate, register and stats; the test files were deleted afterwards.
