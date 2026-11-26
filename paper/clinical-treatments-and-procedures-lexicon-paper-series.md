# Clinical Treatments and Procedures Lexicon

*Rough draft, not reviewed.* A paper series modelled on *Five Papers on WordNet*. Nik Bear Brown and Humanitarians AI [TODO: confirm authorship]. Drafted 2026-11-26 with Grok Bot.

**Where it stands:** the seed list (354 Wikipedia pages) and replication kit are public; one independent Grok Bot edition is drafted and checked (354/354 pass: 312 entries, 26 out of scope, 16 duplicates, 104 ambiguous). No second edition, no cross-model judging and no human review have been run. This vocabulary is descriptive only and is not treatment advice.

## Part I. Introduction to the Clinical Treatments and Procedures Lexicon

### I.1 What the lexicon is for

Health information names interventions in many ways. A public-health page speaks of *hyperbaric oxygen therapy*, a textbook of *hyperbaric medicine*, an abbreviation list of *HBOT*. A reader, a search system or a coding tool needs to know when these name one thing, when one is a kind of another, and when two names that look alike are not the same at all. This lexicon records those decisions for treatments, therapies and medical procedures, at the level of what each one *is*. It does not say how, when or for whom to perform any of them. It is a terminology resource, not a clinical one.

### I.2 Why a WordNet-style relational lexicon

An alphabetical glossary would put *Tracheal intubation* and *Advanced airway management* far apart and say nothing about how they relate. A relational lexicon, in the manner of WordNet, can say that tracheal intubation is a kind of intubation and a kind of medical procedure, and that it is often confused with the broader advanced airway management. The WordNet papers argued that such relations, not spelling, are how people organise what they know about words (Miller et al. 1990/1993). The argument transfers to a technical vocabulary with one change of emphasis: here the relations serve retrieval and disambiguation more than psychology.

### I.3 The lexical matrix, adapted

The rows of the matrix are concepts, one per seed page (`enwiki:<page id>`), each fixed in a draft by a one-sentence work sense. The columns are names: the page title and its variants, each variant with a condition when it names the concept only sometimes. *Rx* is a variant of *Medical prescription*, "abbreviation, chiefly North America"; *intubation* is a "common short form" of *Tracheal intubation*. Polysemy shows up as pages that name two things at once. *Hyperbaric medicine* names both a specialty and the treatment it delivers, and the draft flags it rather than choosing silently.

### I.4 The relations

| Relation | Test the drafter must pass with the real names filled in | WordNet analogue |
|---|---|---|
| synonym | the target can replace the concept in a source excerpt without changing the concept | membership in one synset |
| hypernym | "[concept] is a kind of [target]" is true | hypernymy (@) |
| hyponym | "[target] is a kind of [concept]" is true | hyponymy (~) |
| meronym | the concept includes the target as a component by definition | part meronymy (%p) |
| holonym | the concept is a component of the target by definition | part holonymy (#p) |
| uses | the concept is characteristically associated with the target tool, material or substance | none (new) |
| requires | an explicit conceptual prerequisite supported by a source | none; compare verb entailment |
| certifies | the concept is a credential and attests to the target | none (new) |
| contrast | the target is often confused with the concept but differs from it, including look-alike names | none; replaces antonymy |

Antonyms and pertainyms are not recorded. Every relation also carries a `basis` (`source`, with pointers, or `model_knowledge`, with none) and a target that is either a seed ID or marked `proposed_new`.

In this lexicon **certifies** is not used, and the prompt adds two guards: `uses` may record the characteristic tool or material of an intervention but "never give operating instructions", and `requires` may record only a conceptual prerequisite a source states, never "operational steps". In the Grok Bot edition the relations carrying the structure are hypernym (346 edges) and contrast (119), followed by hyponym (71), uses (32), meronym (21), holonym (8) and synonym (1) [counted from `drafts.jsonl` on 2026-11-26]. The taxonomy is shallow and mostly points outward, to general classes (therapy, medical procedure) that are not themselves seeds.

### I.5 Built with AI: what changes and what does not

What stays from WordNet: concepts organised by relations, relations with explicit tests, and a separation between the source files and the program that checks them. What changes: a language model writes the first draft of every entry from a pinned evidence bundle; a script rejects drafts that cite what they did not read; several models are meant to draft the same seeds blind so their agreement can be measured; and people decide what enters the lexicon. The shared pipeline is described once in the shared methods paper.

## Part II. The vocabulary by category

The seed list comes from three Wikipedia categories: *Medical treatments* (248 direct article members), *Therapy* (67) and *Medical procedures* (51). Category membership supplies candidates, not authority, and the drafts treat the categories as a starting point. The three content papers below follow those categories, then a fourth deals with what the categories pulled in that is not a treatment or procedure, much as the WordNet verb paper kept a residual file of stative verbs.

### II.1 Treatments

The largest category groups named interventions: drug-based and device-based therapies, physical treatments and historical or contested practices. The organising relation is the hypernym. *Hyperbaric medicine* is drafted as a kind of therapy and a kind of diving medicine, with *Hyperbaric treatment schedules* as a meronym, a component by definition. The `uses` relation links an intervention to the material it is characteristically associated with, without saying how it is used.

Hard cases sit at the edges. *VZV immune globulin* is a medication rather than a procedure; *Zinc and the common cold* is an article about a supplement's use, not a named intervention. Both were kept as entries and flagged ambiguous, leaving the scope call to people.

### II.2 Therapies

The *Therapy* category mixes psychological, physical and alternative therapies. Contrast does much of the work: these are the names most often confused with each other or with broader practices. *Virtual reality therapy* illustrates the source problems: its Wikidata item is the narrower virtual reality exposure therapy, and its source also lists computerised CBT as a synonym, which is broader. The draft records both concerns as flags rather than as relations.

### II.3 Procedures

Procedures are things done to or for a patient: *Tracheal intubation*, *Advanced airway management*, *Aerosol-generating procedure*. Here meronymy and holonymy matter more than in treatments, because procedures have parts. The descriptive rule bites hardest in this category. The *Tracheal intubation* entry says what the procedure is (insertion of a tube into the windpipe to keep the airway open or to give certain drugs) and in what settings it is common, and stops there.

### II.4 What the categories pulled in

The categories also contain pages that name no treatment or procedure. The Grok Bot edition abstained on 26 as out of scope: biographies (*Douglas Sadownick*), organisations (*Turning Point*, *VAGA*), places (*Ville Sbertoli*), lists and timelines (*List of therapies*, *Timeline of cancer treatment development*), conditions (*Androgen deficiency*), outcomes (*Remission*, *Therapeutic effect*), and a folk adage (*Feed a cold, starve a fever*). Sixteen more are redirect pages whose target is another seed, recorded as duplicates. A larger group, 104 entries, was kept but flagged ambiguous: phenomena (*Abscopal effect*), documents (*Medical prescription*), examinations (*Well-woman examination*). Whether those belong is a human decision (Part IV).

## Part III. Design and implementation

The common pipeline is in the shared methods paper. This part records what is specific to this lexicon.

### III.1 Seed list and manifest

354 unique English Wikipedia article pages, deduplicated by page ID, all direct members of a seed category, with no subcategory-only pages and no title filter. `data/seeds.tsv` has the columns `concept_id`, `page_id`, `preferred_name`, `source_url` and `direct_categories`. Its SHA-256 is `5ee2167938f2a521e5f35e7a49deceb2e05ea3798384971bd2eb1492b4c223db`, recorded in `data/source-manifest.json`, which also records that `Category:Treatments` was missing. Seed commit: `588a9866` ("Initialize direct-member lexicon and blind replication kit"). The list was retrieved on 2026-11-24 at about 3:52–3:53 PM EST.

### III.2 Evidence bundles

Wikipedia pages were fetched by page ID with the exact revision pinned (pinned revisions date from 2013 to 2026); the lead extract was capped at 2,500 characters; neighbours were the article's out-links to other seeds, at most 40. Wikidata items came from the page's linked item (345 of 354 seeds have one), with ancestors along P31, P279 and P361. WordNet 3.0 noun synsets were read through NLTK; only 38 seeds have any synset, which shows how far a general lexicon is from this vocabulary. No examples from external glossaries were used, and no patient records.

### III.3 Drafting prompt and kit

Prompt gen-v2, adapted from the Irreducibly Human Work Lexicon kit; `system.txt` SHA-256 `f782dda6…`. The domain rule: "Describe what the named intervention or procedure is at a high level. Do not give clinical instructions, doses, contraindication assessments, or patient-specific advice." The field `work_sense` keeps its original name for compatibility.

### III.4 Flags

`out-of-scope:`, `ambiguous:` and `duplicate:`. The Grok Bot edition used `duplicate:` for redirect pages (16) and for two entries Wikidata marks as duplicate items, and also recorded free-text flags for source conflicts and Wikidata problems (198 flags in all, listed in `raw/flags.tsv`).

### III.5 Checking

`check.py` passed 354 of 354 with no errors. 330 drafts passed on the first attempt and 24 needed a second, mostly after the copy guard or the quote check failed. 54 records carry the warning "most claims rest on model knowledge": the 42 abstentions, which have no pointers by design, and 12 entries.

### III.6 Provenance

The run folder `clinical-lexicon-grok-run-20261124` holds the four handoff files plus the raw source cache, specs and tools. Every draft's `_meta` records the model as Grok Bot and the version as unknown.

### III.7 The Grok Bot edition: what was done and how it deviated

A 10-seed pilot passed the check, then the remaining seeds were drafted in 24 batches of about 14 to 16 within one working session, from compact views of each bundle; a script expanded the batch specs into gen-v2 JSON and ran the verifier on each record. This departs from the protocol's fresh context per seed and is stated in RUN.md. Two further departures: WordNet 3.0 rather than 3.1, and capped bundle sizes. No other model drafted or judged, and no other edition was read.

### III.8 Parallel editions and agreement

A paste-in prompt (`02-clinical-treatments-and-procedures.md`) lets another model draft its own blind edition from the same seed commit and hash. The judging kit was ported from the work lexicon to the `grok-agreement-method` branch (commit `51774fbd`), adapted to this schema and scope; it holds no drafts. A smoke test with a synthetic second edition exercised every command.

### III.9 Human in the loop

Professor Bear decides scope, redirects, duplicates and what enters the reviewed edition. The kit's rule: agreement is not evidence, and a reviewer checks the cited source for each retained claim.

## Part IV. Evaluation (to do): what humans do after the AI comparison

### IV.1 Status

Not run. Only one edition exists, so the AI comparison itself has not started.

### IV.2 Prerequisites on the AI side

A second blind edition with its commit SHA; a `drafters.tsv` row for each drafter; `agreement.py run`; model judges joined and finished; the leak check; and the family-weighted panel code. See [HUMAN-EVALUATION-TODO.md](HUMAN-EVALUATION-TODO.md), Part 1.

### IV.3 Human steps in order

The steps below are the same for every lexicon and are written out once, with owners and checkboxes, in [HUMAN-EVALUATION-TODO.md](HUMAN-EVALUATION-TODO.md). They run **after** the AI side has produced its blinded, pairwise comparison of the independent editions. Every step is a human step. None has started.

| # | Human step | What it produces | Gate before the next step | Owner | Status |
|---|---|---|---|---|---|
| H1 | Settle the open decisions (IV.6): judge invitations, `drafters.tsv` rows, trap list, worked examples, weights, acceptance threshold | a committed decision record | Bear signs off | Bear | not started |
| H2 | Recruit and register human judges (`agreement.py register`) | registry rows, seeded samples | at least 2 judges for the pilot; about 10 for full scale | Bear | not started |
| H3 | Pilot: Bear and at least one other judge label the whole pilot pool; tune the rubric on the development half only; freeze the prompts (`agree-v1`) and tag the analysis plan | adjudicated pilot labels, frozen rubric | rubric frozen and tagged | Bear + 1 judge | not started |
| H4 | Human–human overlap pool: about 30% of each judge's items come from a shared pool of about 50, each item judged by at least 2 people | the **human ceiling** (Krippendorff's α, pairwise κ, before adjudication) | ceiling reported per field | human judges | not started |
| H5 | Calibrate the AI judges against people: judge–human κ per field, for the panel, for the outside-family judge alone and for each judge | acceptance per field | κ ≥ 0.6 **and** no more than 0.1 below human–human; otherwise revise the rubric on the development split only and redraw the validation sample | Bear | not started |
| H6 | Targeted review queues (IV.4): disagreements, `FAMILY_SPLIT`, low agreement, flagged records, redirects, Wikidata errors, consensus gaps | a human label for each queued item | every queued item labelled or marked `UNSURE` with a note | human judges | not started |
| H7 | Random audit of agreed items: a seeded sample of items every model agreed on | the false-agreement rate | reported with an interval | human judges | not started |
| H8 | Adjudicate: majority of human judges, ties to Bear, judges' own words kept in `notes` | one adjudicated label per reviewed item | no open ties | Bear | not started |
| H9 | Verify claims (correctness, not agreement): for every claim kept, a reviewer opens the cited source and marks `supports`, `contradicts` or `unsure`; claims with only `model_knowledge` basis are sourced or withheld | per-claim decisions | no kept claim without a named check | reviewers | not started |
| H10 | Domain-safety review against the lexicon's rule (IV.4) | a pass or a list of removals | zero open safety items | Bear or a named domain reviewer | not started |
| H11 | Scope, duplicate and redirect decisions, with a crosswalk to the original seed IDs | decision list and crosswalk | every flagged seed decided | Bear | not started |
| H12 | Accept or reject merged entries into the reviewed edition (`lexicon/entries.jsonl`), with per-claim decisions, contributing run IDs and a named reviewer | the first reviewed entries | each accepted entry has a named reviewer and no unresolved contradiction | Bear | not started |
| H13 | Held-out task and coverage evaluations (IV.5) | task scores with intervals | analysis plan fixed before annotation | Bear + raters | not started |
| H14 | Write up: human ceiling, judge–human agreement, false-agreement rate, safety outcome, accepted-entry counts | the evaluation section of this paper | Bear approves | Bear | not started |

Agreement between models is not evidence that an entry is right. Steps H9 to H12 exist because two models can agree on the same mistake.

### IV.4 What humans review in this lexicon

Editions available today: **one**, the Grok Bot edition (354 records, 312 entries). The cross-model comparison cannot run until a second blind edition exists (paste-in prompt `02-clinical-treatments-and-procedures.md`). Until then, the queues below come from the Grok edition's own flags; after the comparison they are joined by the disagreement queues of step H6.

| Queue | Source | Size in the Grok edition | What the human decides |
|---|---|---:|---|
| Ambiguous entries | `ambiguous:` flags | 104 entries | in scope or not; which sense; keep, narrow or withdraw |
| Out of scope | `out-of-scope:` flags | 26 | confirm the abstention (biographies, organisations, places, conditions, lists) |
| Duplicate redirects | `duplicate:` flags on redirect pages | 16 | map to the seed it redirects to, or keep as its own concept |
| Wikidata duplicate items | `duplicate:` flags on entries | 2 (Bacteriotherapy, Electrotherapeutics) | whether the concepts are one |
| Redirects to pages that are not seeds | RUN.md | 7 targets: Balneotherapy, EHealth, Exocrine pancreatic insufficiency, Magnesium deficiency, Neuromodulation (medicine), Brief intervention, Wake therapy | add a new concept, map, or leave as an abstention |
| Wikidata problems | flags mentioning Wikidata | 47 records [counted from `drafts.jsonl` flags on 2026-11-26] | confirm the problem was not used as evidence |
| Thin evidence | check warning "most claims rest on model knowledge" | 54 (42 abstentions + 12 entries) | the 12 entries go first in claim verification (H9) |
| Retried drafts | `_meta` attempt 2 | 24 | spot-check that the reworded definition still says the same thing |

Examples of what the ambiguous queue holds: *Abscopal effect* (a treatment-response phenomenon, not an intervention), *Medical prescription* (an authorising document), *VZV immune globulin* (a medication), *Well-woman examination* (an examination rather than a treatment), *Hyperbaric medicine* (both a specialty and the treatment it delivers).

**Domain-safety review (H10).** The rule: describe what the intervention or procedure is at a high level; no clinical instructions, doses, contraindication assessments or patient-specific advice; no patient records. The reviewer reads every definition, every variant condition and every `uses` and `requires` relation, since those are the fields where procedure steps could creep in. Pass criterion: zero items that tell a reader how, when or for whom to perform a procedure.

### IV.5 Held-out task and coverage evaluations

- **Coverage against reference vocabularies.** Map a seeded sample of entries to MeSH (the "Analytical, Diagnostic and Therapeutic Techniques, and Equipment" tree), to ICD-10-PCS or WHO's ICHI, and to the SNOMED CT procedure hierarchy if a licence is available [TODO: licence for SNOMED CT]. Measures how much of the lexicon has an established counterpart, and which of its entries do not. Two raters, adjudicated. Status: not designed.
- **Mention linking on public descriptive text.** A held-out set of public, non-clinical-record texts (encyclopaedic or public-health pages, course material), with raters marking treatment and procedure mentions and the concept they name, or *unresolved* or *not in the lexicon*. Measures whether the lexicon's variants and conditions resolve real mentions. No patient records. Status: not designed [TODO: choose the corpus].
- **Scope agreement.** Human labels of entry, out of scope or duplicate on a sample, against each edition's scope decision (AC1). Status: possible as soon as H4 runs.

### IV.6 Open decisions

- The seven "Decisions for Bear" in `AGREEMENT-METHOD.md` §12 on the `grok-agreement-method` branch (51774fbd): judge invitations and `drafters.tsv`; human judges and sample settings; weights, hard gate and acceptance threshold; whether scope agreement is a primary outcome; the draft trap list (`TRAP_IDS`); whether a reviewed `entries.jsonl` counts as an edition in α; scheduling and batch size.
- The seven redirect targets that are not seeds (IV.4).
- Scope policy for medications, examinations, outcomes and phenomena that the category membership pulled in.
- WordNet version: the Grok edition used WordNet 3.0 through NLTK, while the IHWL kit aligns links on Open English WordNet 2025 [TODO: decide one version for link alignment].
- Who drafts the second edition.

### IV.7 Resources, owners and status

About 10 human judges at about 100 items each (3 to 5 hours per judge), a pilot labelled by Bear and one other judge, a named domain reviewer for H10, and reviewers for claim verification. Tools: `agreement.py register`, `validate`, `stats`, and the judging instructions on the `grok-agreement-method` branch. Owner of every step: Bear unless delegated. Status of every step: not started.

## Part V. Limitations

The seed frame is whatever three Wikipedia categories contained on one day. The Grok Bot edition was batched. WordNet barely covers the domain. Wikidata errors were recorded, not fixed. And until a second edition exists, nothing can be said about agreement.

## Appendix A. File formats

**Seeds** (`data/seeds.tsv`): `concept_id`, `page_id`, `preferred_name`, `source_url`, `direct_categories`.

**Evidence bundle** (`bundles.jsonl`, one JSON object per seed, exactly seven top-level fields):

| Field | Content |
|---|---|
| `concept_id` | the seed ID, unchanged |
| `concept` | `id`, `preferred_name`, `kind` and `broad_class` (`unclassified` until supported), `variants` and `relations` (start empty) |
| `neighbors` | candidate relation targets, taken only from the seed list, each `{id, name}` |
| `examples` | optional public terminology excerpts `{id, source URL, text}` |
| `wikipedia` | up to three `{title, revision_id, text}`; the revision is pinned |
| `wikidata` | candidate items `{qid, label, aliases, claims, revision_id}` and ancestors marked `ancestor_of` |
| `wordnet` | matching senses `{synset, lemmas, gloss, relations}` |

**Draft** (`drafts.jsonl`, one JSON object per seed, prompt gen-v2):

| Field | Content |
|---|---|
| `concept_id` | the seed ID |
| `work_sense` | one sentence fixing the sense every later decision is about (the name is kept from the first lexicon for schema compatibility) |
| `links.{wikipedia,wikidata,wordnet}` | `{choice, reason}`; `choice` is a revision ID, QID or synset ID, or `null` to abstain |
| `definition` | `{text, basis, pointers}`; one to three sentences, never more than eight consecutive words from a source |
| `variants[]` | `{text, condition, basis, pointers}`; `condition` says when the form names the concept |
| `relations[]` | `{type, target_label, target_id, proposed_new, basis, pointers, note}` |
| `flags[]` | strings, each a prefix and a reason (Appendix B) |
| `_meta` | added after drafting: model and version (or `unknown`), run mode, attempt count, and for retries the errors that triggered them |

**Pointer forms:** `wd:QID#PID=VALUE_QID`, `wd:QID#alias=TEXT`, `wn:SYNSET#lemma=TEXT`, `wn:SYNSET#RELATION=TARGET`, `wp:REVISION_ID#quote=TEXT` (at most 20 words, copied exactly), `ex:EXAMPLE_ID`.

**Check report** (`report.jsonl`): one line per seed, `{concept_id, status: pass|fail, errors[], warnings[]}`.

**RUN.md:** dates, seed commit and hash, model and settings, tools, evidence sources, deviations, coverage totals, retries and unresolved failures.

## Appendix B. Flags

| Prefix | Meaning |
|---|---|
| `out-of-scope: <reason>` | no usable treatment or procedure sense; every link null, definition "Out of scope", basis `model_knowledge` |
| `ambiguous: <reason>` | unresolved evidence or scope; abstain where needed |
| `duplicate: <id and title>` | used by the Grok Bot edition for redirects to another seed; not defined in `instructions.md` [open decision] |

## Appendix C. Scripts

| Script | Who runs it | What it does |
|---|---|---|
| `render.py` | drafter | renders one system and one user message per bundle |
| `check.py` | drafter, then maintainer | completeness, shape and pointer checks; writes `report.jsonl` |
| `verify_drafts.py` | called by `check.py` | evidence checks from the work lexicon kit |
| `agreement.py` | maintainer and judges | normalise, align, write blinded requests, join, register, validate, stats (on `grok-agreement-method`) |

## References

- Miller, G. A., Beckwith, R., Fellbaum, C., Gross, D., and Miller, K. J. 1990. Introduction to WordNet: An on-line lexical database. *International Journal of Lexicography* 3(4): 235–244. Revised in *Five Papers on WordNet*, CSL Report 43, Princeton University, 1990, revised 1993.
- Miller, G. A. 1990. Nouns in WordNet: A lexical inheritance system. *International Journal of Lexicography* 3(4): 245–264.
- Gross, D., and Miller, K. J. 1990. Adjectives in WordNet. *International Journal of Lexicography* 3(4): 265–277. Revised as Fellbaum, Gross and Miller in *Five Papers on WordNet*, 1993.
- Fellbaum, C. 1990. English verbs as a semantic net. *International Journal of Lexicography* 3(4): 278–301.
- Beckwith, R., Miller, G. A., and Tengi, R. 1993. Design and implementation of the WordNet lexical database and searching software. In *Five Papers on WordNet*.
- Miller, G. A. 1995. WordNet: A lexical database for English. *Communications of the ACM* 38(11): 39–41.
- Fellbaum, C., ed. 1998. *WordNet: An Electronic Lexical Database*. MIT Press.
- Vrandečić, D., and Krötzsch, M. 2014. Wikidata: A free collaborative knowledgebase. *Communications of the ACM* 57(10): 78–85.
- Krippendorff, K. 2018. *Content Analysis: An Introduction to Its Methodology*, 4th ed. SAGE.
- Fleiss, J. L. 1971. Measuring nominal scale agreement among many raters. *Psychological Bulletin* 76(5): 378–382.
- Shared methods paper: *Building WordNet-style lexica with AI: process and provenance* (`building-wordnet-style-lexica-with-ai.md` in this folder).
- MeSH, ICD-10-PCS, WHO ICHI and SNOMED CT are named in IV.5 as candidate reference vocabularies [TODO: add citations when the coverage study is designed].
