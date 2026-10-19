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