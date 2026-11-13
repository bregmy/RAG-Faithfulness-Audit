# Human validation: full

Labels: `validation_sheet.csv` · items: 80

| check                                                    |   n |   accuracy |   cohen_kappa | kappa_95ci   |   judge_positive |   human_positive |
|:---------------------------------------------------------|----:|-----------:|--------------:|:-------------|-----------------:|-----------------:|
| faithful: judge >= 0.5 vs human 'supported'              |  71 |      0.676 |         0.356 | [0.16, 0.54] |            0.493 |            0.732 |
| faithful: judge >= 0.5 vs human 'supported' or 'partial' |  71 |      0.606 |         0.219 | [0.05, 0.39] |            0.493 |            0.831 |
| correct: lenient rule vs human                           |  77 |      0.961 |         0.918 | [0.81, 1.00] |            0.623 |            0.610 |
| refusal: regex vs human                                  |  80 |      0.988 |         0.934 | [0.75, 1.00] |            0.100 |            0.113 |

Spearman correlation between judge faithfulness and human support (supported=1, partial=0.5, unsupported=0): rho = 0.492, p = 0.0000, n = 71.

Prevalence-weighted agreement (the balanced sample re-weighted to the run's mix of judge verdicts, C0-C5): accuracy = 0.921, Cohen's kappa = 0.688, judge faithful = 0.846, human supported = 0.855.

## Human labels by judge verdict (counts)

| judge                    |   partial |   supported |   unsupported |   All |
|:-------------------------|----------:|------------:|--------------:|------:|
| judge faithful (>= 0.5)  |         1 |          32 |             2 |    35 |
| judge unfaithful (< 0.5) |         6 |          20 |            10 |    36 |
| All                      |         7 |          52 |            12 |    71 |

## Faithfulness agreement by condition (balanced sample)

| condition   |      n |   agreement |   judge_faithful |   human_supported |
|:------------|-------:|------------:|-----------------:|------------------:|
| C0          | 12.000 |       0.500 |            0.500 |             1.000 |
| C1          | 12.000 |       0.750 |            0.500 |             0.750 |
| C2          | 12.000 |       0.750 |            0.500 |             0.750 |
| C3          | 12.000 |       0.750 |            0.500 |             0.750 |
| C4          | 12.000 |       0.583 |            0.500 |             0.917 |
| C5          | 11.000 |       0.727 |            0.455 |             0.182 |

## Estimated share of answers humans would rate supported (whole run)

The sample has equal numbers of judge-faithful and judge-unfaithful answers per condition. Here the human rate within each verdict is re-weighted by how common that verdict is among all non-refused answers in the run.

| condition   |   judge_mean_faithfulness |   judge_share_faithful |   human_supported_given_judge_faithful |   human_supported_given_judge_unfaithful |   est_human_supported |   est_human_supported_or_partial |
|:------------|--------------------------:|-----------------------:|---------------------------------------:|-----------------------------------------:|----------------------:|---------------------------------:|
| C0          |                     0.924 |                  0.941 |                                  1.000 |                                    1.000 |                 1.000 |                            1.000 |
| C1          |                     0.901 |                  0.914 |                                  1.000 |                                    0.500 |                 0.957 |                            1.000 |
| C2          |                     0.908 |                  0.920 |                                  1.000 |                                    0.500 |                 0.960 |                            0.973 |
| C3          |                     0.898 |                  0.907 |                                  1.000 |                                    0.500 |                 0.953 |                            0.953 |
| C4          |                     0.899 |                  0.914 |                                  1.000 |                                    0.833 |                 0.986 |                            1.000 |
| C5          |                     0.339 |                  0.406 |                                  0.400 |                                    0.000 |                 0.163 |                            0.343 |
