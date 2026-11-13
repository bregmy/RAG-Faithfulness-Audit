# Judges compared: full_deepseek-r1-32b

Faithful = judge score >= 0.5; human positive = 'supported'. Annotators A and B labeled the same sampled answers (non-refusals only here).

## Each judge against the human annotators

| judge   |   n_A |   accuracy_vs_A |   kappa_vs_A |   spearman_vs_A |   n_B |   accuracy_vs_B |   kappa_vs_B |   spearman_vs_B |
|:--------|------:|----------------:|-------------:|----------------:|------:|----------------:|-------------:|----------------:|
| local   |    61 |           0.738 |        0.331 |           0.323 |    61 |           0.754 |        0.362 |           0.377 |
| gemini  |     8 |           1.000 |      nan     |         nan     |     8 |           1.000 |      nan     |         nan     |
| haiku   |     8 |           0.875 |        0.000 |         nan     |     8 |           0.875 |        0.000 |         nan     |

## Judge-vs-judge agreement (answers both judged)

| judges          |   n |   agreement |   kappa |
|:----------------|----:|------------:|--------:|
| local vs gemini | 201 |       0.955 |   0.686 |
| local vs haiku  | 201 |       0.910 |   0.507 |
| gemini vs haiku | 201 |       0.905 |   0.527 |

## C4 answers that repeated the injected falsehood (62 non-refused)

A high score means the judge calls these answers grounded even though they are false.

| judge   |   n_judged |   mean_faithfulness |   share_rated_faithful |
|:--------|-----------:|--------------------:|-----------------------:|
| local   |         62 |               0.935 |                  0.935 |
| gemini  |         62 |               0.879 |                  0.887 |
| haiku   |         62 |               0.823 |                  0.855 |
