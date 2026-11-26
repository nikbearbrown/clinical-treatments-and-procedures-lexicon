# Parallel editions

Independent, machine-drafted editions of this lexicon, kept here as parallel evaluations so they can be compared side by side. Each subfolder is one model's edition.

- **Unreviewed.** Every record is a machine draft. None has been checked by a person, and none is part of the reviewed lexicon in [`lexicon/`](../lexicon/README.md).
- **Not for drafters.** If you are drafting an independent edition with the [replication kit](../replication/README.md), do not open this folder until your edition is frozen. The kit's blindness rule covers every edition here.
- **Unedited copies.** The files inside an edition folder are copied unchanged from that model's private run folder. Nothing was hand-edited after the edition's final `check.py` run. Paths inside `RUN.md` and the tools refer to the drafter's own machine.
- Wikipedia text in the bundles is CC BY-SA 4.0, with the exact revision id pinned per record; Wikidata is CC0; WordNet 3.0 is under the WordNet licence.

## Editions

| Folder | Model as recorded | Run mode | Date | Seed commit | `data/seeds.tsv` sha256 | Records | `check.py` |
|---|---|---|---|---|---|---|---|
| [`grok-bot/`](grok-bot/) | Grok Bot (exact version: unknown, not exposed to the drafter) | Batched: 24 batches of about 14–16 seeds in one session (a 10-seed pilot first), not a fresh context per seed. Disclosed in `RUN.md`. `_meta.run_mode` records the evidence mode (grounded). | 2026-11-24 (EST) | `588a9866dc42744cecf7ab3789551ab5869687e4` | `5ee2167938f2a521e5f35e7a49deceb2e05ea3798384971bd2eb1492b4c223db` | 354 / 354 seeds | 354/354 pass, 0 fail (330 on the first attempt, 24 after one retry) |

## `grok-bot/`: files

| File | What it is |
|---|---|
| `RUN.md` | Model, seed commit and hash, sources, method, deviations, check result |
| `drafts.jsonl` | One draft per seed, each with `_meta` |
| `report.jsonl` | `check.py` output per seed |
| `bundles.jsonl` | Evidence bundle per seed: pinned Wikipedia revision lead (capped at 2,500 characters), Wikidata, WordNet 3.0, neighbors |
| `attempts.json`, `progress.json` | Attempt counts and resume state |
| `raw/check-final.txt`, `raw/pilot-report.jsonl` | Final and pilot check results |
| `raw/sources.tsv`, `raw/flags.tsv`, `raw/fetch.log` | Pinned revision per seed, reviewer flags, fetch log |
| `specs/batch-NNN.py` | The drafter's per-batch drafting sources |
| `tools/` | Fetch, bundle, view and assemble scripts |

## Left out of `grok-bot/`, and why

- `raw/wp/` and `raw/wd/` (raw Wikipedia and Wikidata API responses, about 900 files). The pinned extracts and revision ids they produced are in `bundles.jsonl` and `raw/sources.tsv`.
- No rendered entries file exists for this edition (`replication/scripts/render.py` renders prompt packets, not entries).
- No keys, secrets or judging anonymisation files are included.

More editions from other models can be added as sibling folders, for example `editions/<model>/`, with a row in the table above.
