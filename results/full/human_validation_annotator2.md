# Human validation: full

Labels: `validation_sheet_annotator2.csv` · items: 80

| check                                                    |   n |   accuracy |   cohen_kappa | kappa_95ci   |   judge_positive |   human_positive |
|:---------------------------------------------------------|----:|-----------:|--------------:|:-------------|-----------------:|-----------------:|
| faithful: judge >= 0.5 vs human 'supported'              |  71 |      0.662 |         0.329 | [0.14, 0.51] |            0.493 |            0.746 |
| faithful: judge >= 0.5 vs human 'supported' or 'partial' |  71 |      0.592 |         0.191 | [0.02, 0.36] |            0.493 |            0.845 |
| correct: lenient rule vs human                           |  77 |      0.987 |         0.973 | [0.91, 1.00] |            0.623 |            0.610 |
| refusal: regex vs human                                  |  80 |      0.988 |         0.934 | [0.75, 1.00] |            0.100 |            0.113 |

Spearman correlation between judge faithfulness and human support (supported=1, partial=0.5, unsupported=0): rho = 0.467, p = 0.0000, n = 71.

Prevalence-weighted agreement (the balanced sample re-weighted to the run's mix of judge verdicts, C0-C5): accuracy = 0.906, Cohen's kappa = 0.617, judge faithful = 0.846, human supported = 0.869.

## Human labels by judge verdict (counts)

| judge                    |   partial |   supported |   unsupported |   All |
|:-------------------------|----------:|------------:|--------------:|------:|
| judge faithful (>= 0.5)  |         1 |          32 |             2 |    35 |
| judge unfaithful (< 0.5) |         6 |          21 |             9 |    36 |
| All                      |         7 |          53 |            11 |    71 |

## Faithfulness agreement by condition (balanced sample)

| condition   |      n |   agreement |   judge_faithful |   human_supported |
|:------------|-------:|------------:|-----------------:|------------------:|
| C0          | 12.000 |       0.500 |            0.500 |             1.000 |
| C1          | 12.000 |       0.750 |            0.500 |             0.750 |
| C2          | 12.000 |       0.750 |            0.500 |             0.750 |
| C3          | 12.000 |       0.750 |            0.500 |             0.750 |
| C4          | 12.000 |       0.583 |            0.500 |             0.917 |
| C5          | 11.000 |       0.636 |            0.455 |             0.273 |

## Estimated share of answers humans would rate supported (whole run)

The sample has equal numbers of judge-faithful and judge-unfaithful answers per condition. Here the human rate within each verdict is re-weighted by how common that verdict is among all non-refused answers in the run.

| condition   |   judge_mean_faithfulness |   judge_share_faithful |   human_supported_given_judge_faithful |   human_supported_given_judge_unfaithful |   est_human_supported |   est_human_supported_or_partial |
|:------------|--------------------------:|-----------------------:|---------------------------------------:|-----------------------------------------:|----------------------:|---------------------------------:|
| C0          |                     0.924 |                  0.941 |                                  1.000 |                                    1.000 |                 1.000 |                            1.000 |
| C1          |                     0.901 |                  0.914 |                                  1.000 |                                    0.500 |                 0.957 |                            1.000 |
| C2          |                     0.908 |                  0.920 |                                  1.000 |                                    0.500 |                 0.960 |                            0.973 |
| C3          |                     0.898 |                  0.907 |                                  1.000 |                                    0.500 |                 0.953 |                            0.953 |
| C4          |                     0.899 |                  0.914 |                                  1.000 |                                    0.833 |                 0.986 |                            1.000 |
| C5          |                     0.339 |                  0.406 |                                  0.400 |                                    0.167 |                 0.261 |                            0.442 |
