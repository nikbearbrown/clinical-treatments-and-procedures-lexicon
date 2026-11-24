# Instructions for human judges

Thank you for helping. This page is for people. You don't need to write code, upload files, or know anything about the models.

## What the study is

The Clinical Treatments and Procedures Lexicon is a descriptive dictionary of medical treatments, therapies and procedures, built from 354 Wikipedia pages in the categories Medical treatments, Therapy and Medical procedures. It says what each treatment or procedure **is**, never how to do it or who should have it. Several AI models each wrote their **own** version of the dictionary, without seeing the others. We want to know how far they agree, and agreement has to mean **in meaning**, not in wording.

AI judges do most of the comparing. **Your job is to tell us whether the AI judges can be trusted.** You'll see pairs of entries side by side, written by models you won't be told the names of, and say how their meanings relate. We then compare your answers with the AI judges' answers, and with other people's.

There are no right answers we're hoping for. An honest "I'm not sure" is far more useful than a guess.

## How much time it takes

- About **100 items**, or **50** if you prefer. Most take one to two minutes, so plan on about **3 to 5 hours in total**, split into as many sittings as you like.
- About a third of your items are also shown to other judges, so we can see how far people agree with each other. The rest are yours alone. Your sample is drawn at random for you.

## How to start

1. Open **Claude Code** or **Codex** in a copy of this repository (Bear will send the link and the run folder name).
2. Type: **"I'm a human judge."**
3. The assistant asks your name and an id (for example `human-jsmith`), and whether you want 100 items or 50. It then draws your sample.
4. It shows you **one item at a time**. Answer in your own words, as you would to a colleague: "B is just a narrower version of A", say, or "these are about completely different things". The assistant turns that into one of the labels below, **reads it back to you**, and saves it only when you confirm. Your own words are saved alongside, exactly as you said them.
5. When you finish, or whenever you stop, it checks your answers and saves them under your name.

The assistant will not suggest an answer before you have given yours. If it seems to, tell it to stop.

## Pausing and resuming

- Say **"pause"** at any time. Everything you have confirmed is saved.
- To resume, open Claude Code or Codex in the repository again and say **"I'm a human judge, resuming as human-jsmith"** (with your id). It picks up at your next unanswered item.
- You can change an earlier answer: say "go back to item 12".

## The labels, with worked examples

Most items show **two definitions** of the same concept, labelled A and B. Pick the relation between their **meanings**:

| Label | Meaning | Worked example |
|---|---|---|
| **Equivalent** | Same thing, same essentials. Either could replace the other. | *Tracheal intubation.* A: "Placing a flexible tube into the windpipe to keep the airway open." B: "Insertion of a breathing tube into the trachea so the airway stays open and the lungs can be ventilated." |
| **A narrower** or **B narrower** | Same thing, but one covers strictly less. | *Stem-cell therapy.* A: "Treatment or prevention of disease using stem cells." B: "Transplanting blood-forming stem cells from bone marrow or cord blood." **B narrower.** |
| **Overlapping** | Same thing, different emphasis. Neither contains the other, and nothing contradicts. | *Pulmonary rehabilitation.* A: "A multidisciplinary programme for people with chronic lung disease." B: "Exercise training and education to improve breathing and daily function." |
| **Conflicting** | Same thing, but they contradict each other on a fact. | *Transdermal.* A: "A route of drug administration through the skin into the bloodstream." B: "An injection given into the outer layer of the skin." Absorption through intact skin is not an injection. |
| **Different sense** | They're about different things. | *Tamponade.* A: "Packing or pressing on a wound to stop bleeding." B: "Compression of the heart by fluid in the pericardial sac." |
| **Not sure** | You can't tell, or you don't know the concept well enough. | Use it freely. It is counted as "no answer", not as a wrong answer. |

Some items ask something slightly different. The assistant explains each kind when it first comes up:

- **Same sense?** Several short statements of what a concept means. Which ones are about the same thing?
- **Same name?** A list of alternative names (for example "TTM", "therapeutic hypothermia") or related concepts. Which ones name the same thing? Something broader or narrower is **not** the same thing: kyphoplasty is not vertebroplasty.
- **Relation type.** Two models link the concept to the same other concept in different ways (for example "kyphoplasty is a kind of vertebral augmentation" against "kyphoplasty uses bone cement"). Are those the same kind of link, compatible ones, reversed (one says "kind of", the other "has kinds"), or in conflict?

## Two rules that always apply

- **Describe, don't advise.** You are judging whether two dictionary definitions mean the same thing. Please don't judge whether a treatment works or is a good idea, and don't add instructions or doses. If the assistant is asked for medical advice, it won't give it during the session.
- **No patient information.** Never mention a real patient, including yourself or anyone you know, in your answers or comments. If an item seems to contain someone's medical details, say "Not sure", tell the assistant "possible patient information", and don't repeat it.

## A few tips

- Judge **meaning**, not writing quality. A longer or more polished definition is not more correct.
- Don't look things up to decide which one is *right*. We only ask whether they *agree*. (Looking up a term you don't know at all is fine, and so is "Not sure".)
- Don't talk with other judges about specific items until everyone has finished.

## Your answers and your name

Your answers are saved in the repository under your id, together with your name as the author, so your contribution is credited. Your comments are stored word for word. If you would rather be credited by initials only, tell the assistant at the start.
