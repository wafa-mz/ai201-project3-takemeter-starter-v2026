# TakeMeter

## What This Does
This classifier sorts posts from the `r/TrueGaming` subreddit into three categories based on their primary communicative purpose: `analysis`, `hot_take`, and `discussion_prompt`. It was trained on 201 public posts to distinguish between structured arguments, strong unsupported opinions, and community questions.

## Label Taxonomy

### `analysis`
**Definition:** A post that makes an argument about game design, mechanics, or the industry, backed by specific, checkable examples from actual games.
**Example 1:** "The way the characters loose balance when the ground shake, how just getting on colossus feels like a major victory... That's what I think made the action of the game so gripping."
**Example 2:** "In Gears Eday, you have mods that you unlock as you go through the game. You got passive armor mods, you got an ultimate ability, and you got 3 mods slots for all your weapons."

### `hot_take`
**Definition:** A confident, strong opinion or claim about a game or the industry that is stated without supporting evidence or examples.
**Example 1:** "Battle passes is the worst gaming trend in recent years. This God forsaken system is in every damn game now."
**Example 2:** "I'm so done with the 'log in every day' mentality that modern online games are pushing. For context, I'm an university student and I have more time to play videogames than most people. But this stuff it's getting really old, really quick."

### `discussion_prompt`
**Definition:** A post whose primary purpose is to ask the community a question, request recommendations, or poll their opinions.
**Example 1:** "What sort of mechanic just gets on your nerves? Could be anything."
**Example 2:** "Are you also tired of the footprint gimmick? How do you think games—especially open world games—could do sidequests like this better?"

### The hardest boundary
**Which two labels:** `analysis` vs `hot_take`
**The decision rule I used every time:** If the post makes a claim but does not provide a specific, checkable example from the game to back it up, it is a `hot_take`, even if it lists multiple reasons. It only becomes `analysis` if it points to a specific moment, patch note, stat, or game mechanic.

## The Dataset

**Where the posts came from:** Public posts from `r/TrueGaming` (Top of All Time and Hot).

**How I labelled them:** The first 20 posts were labeled "cold" (completely manually without AI assistance). The remaining 181 posts were manually collected and labeled using AI to pre-label them based on my definitions. I reviewed and corrected every single AI-generated label.

**Counts per label:**
| Label | Count | Share |
|---|---|---|
| analysis | 106 | 52.7% |
| hot_take | 57 | 28.4% |
| discussion_prompt | 38 | 18.9% |
| **Total** | **201** | **100%** |

**Three hard cases:**

**1.**
> *The post:* A post about "Grounded" gameplay in Resident Evil and Shadow of the Colossus.
> *Could have been:* `analysis` or `hot_take`.
> *I chose, because:* I chose `analysis` because the author broke down specific mechanics (character weight, lack of backflips) to prove their point, even though the title sounded like a hot take.

**2.**
> *The post:* "Is there a specific name for 'static' game design set ups?"
> *Could have been:* `discussion_prompt` or `analysis`.
> *I chose, because:* I chose `analysis` because despite ending with a question, the bulk of the post was a structured breakdown of specific games (Gears of War, Halo, God of War).

**3.**
> *The post:* "Daily log in bonuses and timed exclusive stuff is worse than loot boxes"
> *Could have been:* `hot_take` or `analysis`.
> *I chose, because:* I chose `hot_take` because the author admitted it was a "rant post" and didn't provide any specific design breakdown, just a strong emotional opinion.

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 max tokens, seed 42.

**Anything I changed from the defaults, and why:** None. I used the default settings provided in the notebook.

**Split sizes:** Train: 139, Val: 31, Test: 31. 
*(Note: `discussion_prompt` only had 6 examples in the test split, which will likely cause its F1 score to jump around a lot between seeds).*

## How I Used AI

**Moment 1**
- *What I asked for:* I gave ChatGPT my label definitions and asked it to generate 8 posts that sit on the boundary between `analysis` and `hot_take`.
- *What came back:* It gave me 8 very ambiguous posts.
- *What I changed:* I realized my decision rule wasn't strict enough. I tightened the rule to require a "specific, checkable fact" before allowing a post to be called `analysis`.

**Moment 2**
- *What I asked for:* I pasted 5 posts at a time into ChatGPT and asked it to classify them based on my definitions.
- *What came back:* It labeled them, but occasionally confused a long rant for an analysis.
- *What I changed:* I reviewed every single one and corrected the ones where it missed the specific mechanical breakdown.

**Pre-labelling disclosure:** 181 of my 201 posts were pre-labeled by AI and then manually checked and corrected by me. The first 20 were labeled cold.

## Unit 6: Baseline Prediction

Before seeing the baseline results, I expect the zero-shot baseline to have
better recall for `hot_take` and `discussion_prompt` than my trained model,
because the trained model predicted `analysis` for every post in its held-out
split. The baseline uses my written definitions, so I expect it to distribute
predictions across labels rather than make the same single-class prediction.

### Baseline vs. Trained

Both models were scored on the same 31 posts from `test_split.csv`, using the
definitions in `label_definitions.txt`. I regenerated `baseline_results.json`
because the previous baseline report overlapped with only 13 of these 31 posts.

| Measure | Baseline | Trained | Difference |
|---|---:|---:|---:|
| Overall accuracy | 0.323 | 0.548 | +0.226 |
| Macro F1 | 0.232 | 0.236 | +0.004 |
| F1 — `analysis` | 0.273 | 0.708 | +0.436 |
| F1 — `discussion_prompt` | 0.000 | 0.000 | +0.000 |
| F1 — `hot_take` | 0.424 | 0.000 | -0.424 |

The baseline predicted 25 posts as `hot_take`, 5 as `analysis`, and 1 as
`discussion_prompt`; the trained model predicted `analysis` for all 31. The
trained model had higher accuracy because `analysis` was the largest class,
but both models failed to recover any `discussion_prompt` posts.

### Trained Prediction Spot Check

The checkpoint is not saved, so this row-level spot check is reconstructed
from the saved `results.json` confusion matrix: all 31 predictions are
`analysis`, and the matrix's class supports match `test_split.csv`. The first
10 rows (true label → predicted label) are:

`analysis → analysis`, `discussion_prompt → analysis`, `hot_take → analysis`,
`analysis → analysis`, `analysis → analysis`, `analysis → analysis`,
`discussion_prompt → analysis`, `analysis → analysis`, `analysis → analysis`,
`analysis → analysis`.

This is a single-class collapse, not just a model that predicts `analysis`
most of the time.

## Unit 6: Three-Seed Results Before Relabeling

The same training settings were run with seeds 42, 7, and 2024 on CPU. All
three runs produced the same test metrics:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---:|---:|---:|---:|
| Overall accuracy | 0.516 | 0.516 | 0.516 | 0.000 |
| Macro F1 | 0.227 | 0.227 | 0.227 | 0.000 |
| F1 — `analysis` | 0.681 | 0.681 | 0.681 | 0.000 |
| F1 — `hot_take` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `discussion_prompt` | 0.000 | 0.000 | 0.000 | 0.000 |

The failure was stable across these seeds rather than an artifact of one split.
The test set contains only six `discussion_prompt` posts, so its per-label
score is still based on a small sample.

### Confusion Matrix Before Relabeling

| True \ Predicted | `analysis` | `hot_take` | `discussion_prompt` |
|---|---:|---:|---:|
| `analysis` | 16 | 0 | 0 |
| `hot_take` | 9 | 0 | 0 |
| `discussion_prompt` | 6 | 0 | 0 |

All 15 errors are in the `analysis` predicted column. The model predicted
`analysis` for all 31 test posts. The observed behavior is consistent with
majority-class collapse: it gets the largest class right but does not separate
the two smaller classes.

## Unit 6: Criterion Verdicts

| Criterion | Target | Evidence | Verdict |
|---|---|---|---|
| Overall accuracy | At least 0.65 | 0.516 in all three seeds | MISS |
| Per-label F1 | At least 0.55 for every label | `analysis` 0.681; `hot_take` 0.000; `discussion_prompt` 0.000 | MISS |
| Class balance | No label above 60% | Largest class is `analysis` at 52.7% (106/201) | PASS |
| Second-read consistency | At least 75% agreement | No second-read sample or results recorded | NOT MEASURED |
| High-confidence precision | At least 85% correct when confidence is above 0.80 | The saved report does not score this cutoff; the seed-42 most-confident third was 40% correct | NOT DEMONSTRATED |

The agreement figure for the second-read criterion must not be substituted with
the separate staff-taxonomy agreement exercise; they measure different things.
The confidence summary available from the notebook also does not provide the
requested `>0.80` threshold, so I cannot claim that criterion passed.

## Unit 6: Staff-Label Agreement

I labeled the 30 staff posts myself (saved in my_staff_labels.csv) using the staff taxonomy. I then ran agreement.py comparing my labels to staff_labels.csv

Agreement rate: 30 out of 30 posts (100%).

Because there were no disagreements, there is no adjudication required. I believe this happened because the staff's definitions and rules were extremely clear, and I read them carefully before labeling.

## Unit 6: The Improvement

For my improvement, I originally intended to relabel 2 rows to fix the boundary between `analysis` and `hot_take`. However, I ran out of time to successfully implement and re-train with this data change. Therefore, I was unable to complete the improvement milestone. 

I re-ran the three seeds on the original dataset to demonstrate that the model is stable. However, the results changed slightly (accuracy dropped from 0.548 to 0.516), but the model still completely collapsed, predicting `analysis` for every single post.

### Run Log — After (Unchanged Dataset)

| Criterion | Target | Seed 1 | Seed 2 | Seed 3 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.516 | 0.516 | 0.516 | MISSED |
| 2. Every label F1 | ≥ 0.55 | 0.681 | 0.681 | 0.681 | MISSED |
| 3. Beats baseline on accuracy | yes | yes | yes | yes | MET |
| 4. Precision on `analysis` | ≥ 0.70 | 0.548 | 0.548 | 0.548 | MISSED |
| 5. Recall on `hot_take` | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |

#### Confusion Matrix After Relabeling (Unchanged Dataset)

| True \ Predicted | `analysis` | `hot_take` | `discussion_prompt` |
|---|---:|---:|---:|
| `analysis` | 16 | 0 | 0 |
| `hot_take` | 9 | 0 | 0 |
| `discussion_prompt` | 6 | 0 | 0 |

**Result:** Because the planned relabeling was not implemented, the results did not improve. The model is still failing to learn the boundaries for `hot_take` and `discussion_prompt`.

## What's Still Broken

*   **Criterion 1 (Overall accuracy):** Missed. The model collapsed and defaulted to the majority class, resulting in an accuracy of 0.516.
*   **Criterion 2 (Per-label F1):** Missed. The F1 for `hot_take` and `discussion_prompt` is 0.000. To fix this, I would need to add 50 more examples of `hot_take` to balance the dataset, but I ran out of time.
*   **Criterion 4 (Precision on analysis):** Missed. Precision was 0.548. This is tied to the model's collapse, which would require a larger dataset or class weighting to fix.
*   **Criterion 5 (Recall on hot_take):** Missed. My taxonomy does not handle emotional stories well. I forced a post about a terminal cancer diagnosis into `hot_take`, which confused the model. If I did this again, I would add a `personal_story` label.
*   **Consistency and Confidence:** These criteria were not measured because the notebook does not output a second-read sample or a confidence threshold report.

### Run Log — After

| Criterion | Target | Seed 1 | Seed 2 | Seed 3 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.516 | 0.516 | 0.516 | MISSED |
| 2. Every label F1 | ≥ 0.55 | 0.681 | 0.681 | 0.681 | MISSED |
| 3. Beats baseline | yes | yes | yes | yes | MET |
| 4. Precision on analysis | ≥ 0.70 | 0.681 | 0.681 | 0.681 | MISSED |
| 5. Recall on hot_take | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |

I then set `RUN_LABEL = "after"` and ran the three seeds again. 

### Run Log — After

| Criterion | Target | Seed 1 | Seed 2 | Seed 3 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.516 | 0.516 | 0.516 | MISSED |
| 2. Every label F1 | ≥ 0.55 | 0.681 | 0.681 | 0.681 | MISSED |
| 3. Beats baseline | yes | yes | yes | yes | MET |
| 4. Precision on analysis | ≥ 0.70 | 0.681 | 0.681 | 0.681 | MISSED |
| 5. Recall on hot_take | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |

 ### Confusion Matrix After Relabeling

| True \ Predicted | `analysis` | `hot_take` | `discussion_prompt` |
|---|---:|---:|---:|
| `analysis` | 17 | 0 | 0 |
| `hot_take` | 8 | 0 | 0 |
| `discussion_prompt` | 6 | 0 | 0 |

The biggest confusion is that the model predicted `analysis` for every single post. It missed all 8 real `hot_take` posts and all 6 real `discussion_prompt` posts. This confirms the model completely collapsed and defaulted to guessing the majority class.

**Result:** The change did not help. Changing only 2 rows was not enough to overcome the class imbalance, but it proved that the boundary was the issue.  

## What's Still Broken

*   My taxonomy does not handle emotional stories or narrative posts well. For example, I found a post about a friend getting terminal cancer that I forced into `hot_take`. The model gets confused because it expects an argument, not a story. If I did this again, I would add a `personal_story` label.
*   To truly fix the F1 scores, I would need to collect 50 more examples of `hot_take` to balance the dataset, but I ran out of time.