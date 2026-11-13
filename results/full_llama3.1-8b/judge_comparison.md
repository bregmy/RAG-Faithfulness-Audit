# Judges compared: full_llama3.1-8b

Faithful = judge score >= 0.5; human positive = 'supported'. Annotators A and B labeled the same sampled answers (non-refusals only here).

## Each judge against the human annotators

| judge   |   n_A |   accuracy_vs_A |   kappa_vs_A |   spearman_vs_A |   n_B |   accuracy_vs_B |   kappa_vs_B |   spearman_vs_B |
|:--------|------:|----------------:|-------------:|----------------:|------:|----------------:|-------------:|----------------:|
| local   |    39 |           0.769 |        0.276 |           0.230 |    39 |           0.769 |        0.276 |           0.230 |
| gemini  |     7 |           1.000 |      nan     |         nan     |     7 |           1.000 |      nan     |         nan     |
| haiku   |     7 |           0.857 |        0.000 |         nan     |     7 |           0.857 |        0.000 |         nan     |

## Judge-vs-judge agreement (answers both judged)

| judges          |   n |   agreement |   kappa |
|:----------------|----:|------------:|--------:|
| local vs gemini | 157 |       0.930 |   0.606 |
| local vs haiku  | 157 |       0.866 |   0.484 |
| gemini vs haiku | 157 |       0.847 |   0.401 |

## C4 answers that repeated the injected falsehood (78 non-refused)

A high score means the judge calls these answers grounded even though they are false.

| judge   |   n_judged |   mean_faithfulness |   share_rated_faithful |
|:--------|-----------:|--------------------:|-----------------------:|
| local   |         78 |               0.825 |                  0.897 |
| gemini  |         78 |               0.871 |                  0.897 |
| haiku   |         78 |               0.656 |                  0.769 |
