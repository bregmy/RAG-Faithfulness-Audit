# Judges compared: full

Faithful = judge score >= 0.5; human positive = 'supported'. Annotators A and B labeled the same sampled answers (non-refusals only here).

## Each judge against the human annotators

| judge   |   n_A |   accuracy_vs_A |   kappa_vs_A |   spearman_vs_A |   n_B |   accuracy_vs_B |   kappa_vs_B |   spearman_vs_B |
|:--------|------:|----------------:|-------------:|----------------:|------:|----------------:|-------------:|----------------:|
| local   |    71 |           0.676 |        0.356 |           0.492 |    71 |           0.662 |        0.329 |           0.467 |
| gemini  |    71 |           0.732 |        0.370 |           0.579 |    71 |           0.746 |        0.397 |           0.576 |
| haiku   |    71 |           0.761 |        0.469 |           0.516 |    71 |           0.775 |        0.497 |           0.567 |

## Judge-vs-judge agreement (answers both judged)

| judges          |   n |   agreement |   kappa |
|:----------------|----:|------------:|--------:|
| local vs gemini | 282 |       0.894 |   0.611 |
| local vs haiku  | 282 |       0.879 |   0.617 |
| gemini vs haiku | 282 |       0.823 |   0.415 |

## C4 answers that repeated the injected falsehood (80 non-refused)

A high score means the judge calls these answers grounded even though they are false.

| judge   |   n_judged |   mean_faithfulness |   share_rated_faithful |
|:--------|-----------:|--------------------:|-----------------------:|
| local   |         80 |               0.831 |                  0.863 |
| gemini  |         80 |               0.856 |                  0.887 |
| haiku   |         80 |               0.623 |                  0.688 |
