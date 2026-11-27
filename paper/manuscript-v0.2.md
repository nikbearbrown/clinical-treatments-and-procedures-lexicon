# Separating Symptoms from Interventions: A Clinical Treatments and Procedures Lexicon

Humanitarians AI | Revised rough methods manuscript v0.2 | November 2026

## Abstract

A treatment or procedure can be mentioned as a performed action, an option, or a public announcement. We propose a reviewer-maintained clinical vocabulary that preserves these differences and can work alongside a separately versioned symptom lexicon. We describe independent edition construction, two agentic applications, and a synthetic review-queue comparison. No clinical validation or measured staff savings are reported.

## Construction and review

The [frozen seed manifest](../data/README.md) contains 354 distinct English Wikipedia article pages from listed treatment and procedure categories. These are candidates, not 354 validated concepts. Use the [replication kit](../replication/README.md) to draft independent editions without peer exposure. Freeze editions before comparison, validate structure, and verify claim support independently of model agreement. Retain class and source provenance. For evaluation, distinguish the concept, its role and context: for example, performed, considered, declined, or promoted. A treatment mention alone does not establish whether a patient has the associated condition. Add [MeSH](https://www.nlm.nih.gov/mesh/meshhome.html) mappings only after review; do not modify the independent-edition schema for this experiment.

## Evaluation

| Question | Comparison and outcome |
|---|---|
| Do context rules separate interventions from conditions? | Compare literal matches and context-aware typing on held-out fictional announcements. Report counts by sense: condition, intervention, awareness/event, other, and unclear. Use a sense breakdown chart plus a reviewer decision table. |
| Does the lexicon improve literature discovery? | Compare a fixed title/abstract plus applicable MeSH baseline to intervention alias expansion on the same snapshot. Blind-label pooled paper–topic pairs; report precision at a fixed shortlist size and reasons for new matches. |
| Does a typed intervention layer help a note review queue? | Compare fixed keyword search, reviewed symptom terms, and symptom terms plus typed interventions. Count unique notes, not term hits: relevant notes found and missed, irrelevant notes surfaced, and total notes queued per 100 eligible. If thresholds are tunable, compare burden at a prespecified recall target. |

Define relevance before running the matcher. Split by fictional template family, including symptom-only, intervention-only, combined, and ambiguous contexts. Lock context rules and thresholds using development data only. Label independently and adjudicate against a frozen rubric. Do not import an exclusion learned from an announcement directly into the review-queue test.

## Reproducibility and release decisions

Implementation of the independent edition follows the [pinned manifest](../data/source-manifest.json) and keeps one object per seed, including abstentions. Record structural failures separately from concept and source-review disagreements. Before releasing an alias, record which sense it matches, whether the decision applies to public or fictional clinical context, and the release in which it becomes eligible.

Evaluate whether each queue finds a note under a prespecified relevance definition, regardless of the number of lexical matches. Where a queue assigns a score, select thresholds using development data only and report actual held-out recall at the chosen thresholds, even if it differs from the target. Show false additions and false removals separately. Include fictional negative controls: a procedure merely considered, an appointment described as public outreach, and a relevant note using no canonical term. Document how disagreements and ambiguous cases are counted.

**Figure 2 design:** For each arm, show relevant notes surfaced and missed, with irrelevant notes queued shown in a separate panel beside total workload. For each arm, label raw counts and denominator per 100 eligible notes; keep actual observed recall beside the prespecified target when applicable. No clinical or measured workload result is implied.

[NEEDS: frozen note relevance rubric, pinned symptom-only vocabulary, sample size rationale, and threshold decision rule.]

## Agentic workflows

[Figure 1](agentic-workflows.md) shows Social Media Agent for checking how organizations use phrases and Research Ledger for finding papers relevant to a reader’s question, such as evidence on reviewer workload. The workflows share reviewed terminology but not records, labels or preferences.

## Status and limitations

The seed list and replication kit exist; this draft does not claim a reviewed release or study results. Synthetic notes test designed scenarios, not clinical accuracy. Real-note evaluation would require separate approval and governance. Neither agent diagnoses, recommends treatment, or autonomously triages records.
