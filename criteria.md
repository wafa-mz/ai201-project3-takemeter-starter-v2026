# Acceptance criteria - TakeMeter

**1. Overall Accuracy target: ≥ 0.65**
Reason: Since there are three labels, a random guess gets roughly 33%. A 65% accuracy means the model is learning the actual distinctions and is useful for sorting posts. It is a realistic target for a small dataset of 200 examples.

**2. Per-label F1 score target: ≥ 0.55 for every label**
Reason: A high average accuracy can hide the fact that the model completely fails on one specific label. Even if one label has fewer examples, I want to ensure the model can identify it at least half the time (0.55 F1).

**3. Class Balance target: No single label > 60% of the dataset**
Reason: The syllabus caps it at 70%, but I want a stricter margin. If one label dominates, the model learns to just guess that label. Keeping every label under 60% forces the dataset to be diverse.

**4. Consistency target: ≥ 75% agreement on a second read**
Reason: If I re-label 20 randomly selected posts a week later, I should agree with my past self at least 75% of the time. If I can't label consistently, the model can't learn a consistent pattern.

**5. Confidence target: High-confidence predictions (>0.80) should be correct ≥ 85% of the time**
Reason: A confident wrong prediction is worse than an unsure right one. If the model says it is 90% sure a post is a `hot_take`, it needs to actually be a `hot_take` almost every time.