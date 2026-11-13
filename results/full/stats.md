# Statistics: full

Bootstrap: 2000 resamples of questions, seed 42. Faithfulness and answer relevancy use non-refused answers only. Paired tests match the same question across two cells; p-values are Holm-adjusted within each family (`p_holm`).

## Correctness (lenient; C5 = refusal): mean [95% CI]

| condition   | -                    | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|:---------------------|
| C0          |                      | 0.947 [0.893, 0.987] | 0.933 [0.867, 0.987] | 0.947 [0.893, 0.987] |
| C1          |                      | 0.907 [0.827, 0.960] | 0.933 [0.867, 0.987] | 0.947 [0.893, 0.987] |
| C2          |                      | 0.920 [0.853, 0.973] | 0.907 [0.840, 0.973] | 0.920 [0.853, 0.973] |
| C3          |                      | 0.920 [0.853, 0.973] | 0.947 [0.893, 0.987] | 0.947 [0.893, 0.987] |
| C4          |                      | 0.707 [0.613, 0.813] | 0.667 [0.560, 0.773] | 0.587 [0.467, 0.693] |
| C5          |                      | 0.074 [0.021, 0.126] | 0.547 [0.453, 0.653] | 0.411 [0.316, 0.516] |
| closed_book | 0.320 [0.227, 0.427] |                      |                      |                      |

## Refusal rate: mean [95% CI]

| condition   | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|
| C0          | 0.000 [0.000, 0.000] | 0.027 [0.000, 0.067] | 0.013 [0.000, 0.040] |
| C1          | 0.000 [0.000, 0.000] | 0.027 [0.000, 0.067] | 0.013 [0.000, 0.040] |
| C2          | 0.000 [0.000, 0.000] | 0.013 [0.000, 0.040] | 0.000 [0.000, 0.000] |
| C3          | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| C4          | 0.000 [0.000, 0.000] | 0.040 [0.000, 0.080] | 0.000 [0.000, 0.000] |
| C5          | 0.074 [0.032, 0.127] | 0.547 [0.442, 0.642] | 0.411 [0.316, 0.516] |

## Faithfulness: mean [95% CI]

| condition   | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|
| C0          | 0.940 [0.887, 0.980] | 0.927 [0.868, 0.975] | 0.905 [0.838, 0.966] |
| C1          | 0.909 [0.844, 0.967] | 0.909 [0.842, 0.966] | 0.885 [0.811, 0.953] |
| C2          | 0.916 [0.856, 0.964] | 0.919 [0.851, 0.973] | 0.891 [0.818, 0.951] |
| C3          | 0.896 [0.827, 0.956] | 0.900 [0.827, 0.960] | 0.898 [0.824, 0.958] |
| C4          | 0.927 [0.873, 0.973] | 0.875 [0.799, 0.944] | 0.893 [0.820, 0.953] |
| C5          | 0.330 [0.245, 0.420] | 0.419 [0.291, 0.558] | 0.290 [0.187, 0.403] |

## Answer relevancy: mean [95% CI]

| condition   | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|
| C0          | 0.916 [0.892, 0.937] | 0.911 [0.887, 0.932] | 0.914 [0.892, 0.933] |
| C1          | 0.920 [0.899, 0.941] | 0.920 [0.898, 0.941] | 0.919 [0.897, 0.940] |
| C2          | 0.914 [0.894, 0.933] | 0.895 [0.851, 0.930] | 0.922 [0.900, 0.942] |
| C3          | 0.912 [0.889, 0.932] | 0.902 [0.867, 0.930] | 0.919 [0.897, 0.940] |
| C4          | 0.921 [0.900, 0.941] | 0.903 [0.870, 0.931] | 0.920 [0.900, 0.939] |
| C5          | 0.864 [0.827, 0.895] | 0.855 [0.822, 0.886] | 0.892 [0.866, 0.916] |

## Context precision: mean [95% CI]

| condition   | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|
| C0          | 0.987 [0.960, 1.000] | 0.987 [0.960, 1.000] | 0.987 [0.960, 1.000] |
| C1          | 0.247 [0.240, 0.250] | 0.247 [0.240, 0.250] | 0.247 [0.240, 0.250] |
| C2          | 0.327 [0.287, 0.373] | 0.327 [0.287, 0.370] | 0.327 [0.290, 0.373] |
| C3          | 0.187 [0.164, 0.211] | 0.187 [0.164, 0.213] | 0.187 [0.164, 0.215] |
| C4          | 0.557 [0.523, 0.597] | 0.557 [0.520, 0.593] | 0.557 [0.520, 0.597] |
| C5          | 0.124 [0.084, 0.168] | 0.124 [0.084, 0.166] | 0.124 [0.082, 0.168] |

## Followed fake (C4): mean [95% CI]

| condition   | M0                   | M1                   | M2                   |
|:------------|:---------------------|:---------------------|:---------------------|
| C4          | 0.333 [0.227, 0.440] | 0.333 [0.227, 0.440] | 0.413 [0.293, 0.520] |

## Paired tests

| family                  | metric        | a     | b     |   n_pairs |   mean_a |   mean_b |   effect | effect_name        | detail                          |     p |   p_holm |
|:------------------------|:--------------|:------|:------|----------:|---------:|---------:|---------:|:-------------------|:--------------------------------|------:|---------:|
| mitigation              | correct       | C0 M0 | C0 M1 |        75 |    0.947 |    0.933 |   -0.013 | difference (b - a) | discordant: only a=2, only b=1  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C0 M0 | C0 M1 |        73 |    0.938 |    0.927 |   -0.333 | rank-biserial r    | non-zero differences: 3         | 0.750 |    1.000 |
| mitigation              | correct       | C0 M0 | C0 M2 |        75 |    0.947 |    0.947 |    0.000 | difference (b - a) | discordant: only a=2, only b=2  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C0 M0 | C0 M2 |        74 |    0.939 |    0.905 |   -0.800 | rank-biserial r    | non-zero differences: 4         | 0.250 |    1.000 |
| mitigation              | correct       | C0 M1 | C0 M2 |        75 |    0.933 |    0.947 |    0.013 | difference (b - a) | discordant: only a=1, only b=2  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C0 M1 | C0 M2 |        72 |    0.926 |    0.917 |   -0.200 | rank-biserial r    | non-zero differences: 5         | 0.875 |    1.000 |
| mitigation              | correct       | C1 M0 | C1 M1 |        75 |    0.907 |    0.933 |    0.027 | difference (b - a) | discordant: only a=2, only b=4  | 0.688 |    1.000 |
| mitigation              | faithfulness  | C1 M0 | C1 M1 |        73 |    0.906 |    0.909 |    0.133 | rank-biserial r    | non-zero differences: 5         | 0.875 |    1.000 |
| mitigation              | correct       | C1 M0 | C1 M2 |        75 |    0.907 |    0.947 |    0.040 | difference (b - a) | discordant: only a=0, only b=3  | 0.250 |    1.000 |
| mitigation              | faithfulness  | C1 M0 | C1 M2 |        74 |    0.919 |    0.885 |   -0.524 | rank-biserial r    | non-zero differences: 6         | 0.375 |    1.000 |
| mitigation              | correct       | C1 M1 | C1 M2 |        75 |    0.933 |    0.947 |    0.013 | difference (b - a) | discordant: only a=1, only b=2  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C1 M1 | C1 M2 |        72 |    0.912 |    0.882 |   -0.800 | rank-biserial r    | non-zero differences: 4         | 0.250 |    1.000 |
| mitigation              | correct       | C2 M0 | C2 M1 |        75 |    0.920 |    0.907 |   -0.013 | difference (b - a) | discordant: only a=2, only b=1  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C2 M0 | C2 M1 |        74 |    0.919 |    0.919 |    0.000 | rank-biserial r    | non-zero differences: 5         | 1.000 |    1.000 |
| mitigation              | correct       | C2 M0 | C2 M2 |        75 |    0.920 |    0.920 |    0.000 | difference (b - a) | discordant: only a=3, only b=3  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C2 M0 | C2 M2 |        75 |    0.916 |    0.891 |   -0.393 | rank-biserial r    | non-zero differences: 7         | 0.406 |    1.000 |
| mitigation              | correct       | C2 M1 | C2 M2 |        75 |    0.907 |    0.920 |    0.013 | difference (b - a) | discordant: only a=2, only b=3  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C2 M1 | C2 M2 |        74 |    0.919 |    0.896 |   -0.381 | rank-biserial r    | non-zero differences: 6         | 0.531 |    1.000 |
| mitigation              | correct       | C3 M0 | C3 M1 |        75 |    0.920 |    0.947 |    0.027 | difference (b - a) | discordant: only a=0, only b=2  | 0.500 |    1.000 |
| mitigation              | faithfulness  | C3 M0 | C3 M1 |        75 |    0.896 |    0.900 |    0.143 | rank-biserial r    | non-zero differences: 7         | 0.812 |    1.000 |
| mitigation              | correct       | C3 M0 | C3 M2 |        75 |    0.920 |    0.947 |    0.027 | difference (b - a) | discordant: only a=1, only b=3  | 0.625 |    1.000 |
| mitigation              | faithfulness  | C3 M0 | C3 M2 |        75 |    0.896 |    0.898 |    0.000 | rank-biserial r    | non-zero differences: 6         | 1.000 |    1.000 |
| mitigation              | correct       | C3 M1 | C3 M2 |        75 |    0.947 |    0.947 |    0.000 | difference (b - a) | discordant: only a=1, only b=1  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C3 M1 | C3 M2 |        75 |    0.900 |    0.898 |   -0.100 | rank-biserial r    | non-zero differences: 4         | 1.000 |    1.000 |
| mitigation              | correct       | C4 M0 | C4 M1 |        75 |    0.707 |    0.667 |   -0.040 | difference (b - a) | discordant: only a=5, only b=2  | 0.453 |    1.000 |
| mitigation              | followed_fake | C4 M0 | C4 M1 |        75 |    0.333 |    0.333 |    0.000 | difference (b - a) | discordant: only a=3, only b=3  | 1.000 |    1.000 |
| mitigation              | faithfulness  | C4 M0 | C4 M1 |        72 |    0.924 |    0.875 |   -1.000 | rank-biserial r    | non-zero differences: 4         | 0.125 |    1.000 |
| mitigation              | correct       | C4 M0 | C4 M2 |        75 |    0.707 |    0.587 |   -0.120 | difference (b - a) | discordant: only a=14, only b=5 | 0.064 |    1.000 |
| mitigation              | followed_fake | C4 M0 | C4 M2 |        75 |    0.333 |    0.413 |    0.080 | difference (b - a) | discordant: only a=6, only b=12 | 0.238 |    1.000 |
| mitigation              | faithfulness  | C4 M0 | C4 M2 |        75 |    0.927 |    0.893 |   -0.533 | rank-biserial r    | non-zero differences: 5         | 0.375 |    1.000 |
| mitigation              | correct       | C4 M1 | C4 M2 |        75 |    0.667 |    0.587 |   -0.080 | difference (b - a) | discordant: only a=12, only b=6 | 0.238 |    1.000 |
| mitigation              | followed_fake | C4 M1 | C4 M2 |        75 |    0.333 |    0.413 |    0.080 | difference (b - a) | discordant: only a=7, only b=13 | 0.263 |    1.000 |
| mitigation              | faithfulness  | C4 M1 | C4 M2 |        72 |    0.875 |    0.889 |    0.200 | rank-biserial r    | non-zero differences: 5         | 1.000 |    1.000 |
| mitigation              | refused       | C5 M0 | C5 M1 |        95 |    0.074 |    0.547 |    0.474 | difference (b - a) | discordant: only a=0, only b=45 | 0.000 |    0.000 |
| mitigation              | faithfulness  | C5 M0 | C5 M1 |        43 |    0.471 |    0.419 |   -0.571 | rank-biserial r    | non-zero differences: 7         | 0.266 |    1.000 |
| mitigation              | refused       | C5 M0 | C5 M2 |        95 |    0.074 |    0.411 |    0.337 | difference (b - a) | discordant: only a=0, only b=32 | 0.000 |    0.000 |
| mitigation              | faithfulness  | C5 M0 | C5 M2 |        56 |    0.369 |    0.290 |   -0.439 | rank-biserial r    | non-zero differences: 18        | 0.095 |    1.000 |
| mitigation              | refused       | C5 M1 | C5 M2 |        95 |    0.547 |    0.411 |   -0.137 | difference (b - a) | discordant: only a=16, only b=3 | 0.004 |    0.164 |
| mitigation              | faithfulness  | C5 M1 | C5 M2 |        40 |    0.400 |    0.348 |   -0.500 | rank-biserial r    | non-zero differences: 7         | 0.297 |    1.000 |
| condition vs C0         | correct       | C0 M0 | C1 M0 |        75 |    0.947 |    0.907 |   -0.040 | difference (b - a) | discordant: only a=3, only b=0  | 0.250 |    1.000 |
| condition vs C0         | faithfulness  | C0 M0 | C1 M0 |        75 |    0.940 |    0.909 |   -1.000 | rank-biserial r    | non-zero differences: 3         | 0.250 |    1.000 |
| condition vs C0         | correct       | C0 M0 | C2 M0 |        75 |    0.947 |    0.920 |   -0.027 | difference (b - a) | discordant: only a=2, only b=0  | 0.500 |    1.000 |
| condition vs C0         | faithfulness  | C0 M0 | C2 M0 |        75 |    0.940 |    0.916 |   -0.571 | rank-biserial r    | non-zero differences: 6         | 0.250 |    1.000 |
| condition vs C0         | correct       | C0 M0 | C3 M0 |        75 |    0.947 |    0.920 |   -0.027 | difference (b - a) | discordant: only a=3, only b=1  | 0.625 |    1.000 |
| condition vs C0         | faithfulness  | C0 M0 | C3 M0 |        75 |    0.940 |    0.896 |   -0.929 | rank-biserial r    | non-zero differences: 7         | 0.031 |    0.656 |
| condition vs C0         | correct       | C0 M0 | C4 M0 |        75 |    0.947 |    0.707 |   -0.240 | difference (b - a) | discordant: only a=19, only b=1 | 0.000 |    0.001 |
| condition vs C0         | faithfulness  | C0 M0 | C4 M0 |        75 |    0.940 |    0.927 |   -0.400 | rank-biserial r    | non-zero differences: 4         | 0.500 |    1.000 |
| random vs related noise | correct       | C1 M0 | C2 M0 |        75 |    0.907 |    0.920 |    0.013 | difference (b - a) | discordant: only a=2, only b=3  | 1.000 |    1.000 |
| random vs related noise | faithfulness  | C1 M0 | C2 M0 |        75 |    0.909 |    0.916 |    0.083 | rank-biserial r    | non-zero differences: 8         | 0.891 |    1.000 |
| condition vs C0         | correct       | C0 M1 | C1 M1 |        75 |    0.933 |    0.933 |    0.000 | difference (b - a) | discordant: only a=1, only b=1  | 1.000 |    1.000 |
| condition vs C0         | faithfulness  | C0 M1 | C1 M1 |        72 |    0.926 |    0.921 |   -0.095 | rank-biserial r    | non-zero differences: 6         | 0.906 |    1.000 |
| condition vs C0         | correct       | C0 M1 | C2 M1 |        75 |    0.933 |    0.907 |   -0.027 | difference (b - a) | discordant: only a=3, only b=1  | 0.625 |    1.000 |
| condition vs C0         | faithfulness  | C0 M1 | C2 M1 |        72 |    0.933 |    0.917 |   -0.300 | rank-biserial r    | non-zero differences: 4         | 0.750 |    1.000 |
| condition vs C0         | correct       | C0 M1 | C3 M1 |        75 |    0.933 |    0.947 |    0.013 | difference (b - a) | discordant: only a=1, only b=2  | 1.000 |    1.000 |
| condition vs C0         | faithfulness  | C0 M1 | C3 M1 |        73 |    0.927 |    0.911 |   -0.333 | rank-biserial r    | non-zero differences: 5         | 0.625 |    1.000 |
| condition vs C0         | correct       | C0 M1 | C4 M1 |        75 |    0.933 |    0.667 |   -0.267 | difference (b - a) | discordant: only a=21, only b=1 | 0.000 |    0.000 |
| condition vs C0         | faithfulness  | C0 M1 | C4 M1 |        71 |    0.925 |    0.873 |   -0.556 | rank-biserial r    | non-zero differences: 9         | 0.172 |    1.000 |
| random vs related noise | correct       | C1 M1 | C2 M1 |        75 |    0.933 |    0.907 |   -0.027 | difference (b - a) | discordant: only a=4, only b=2  | 0.688 |    1.000 |
| random vs related noise | faithfulness  | C1 M1 | C2 M1 |        72 |    0.914 |    0.917 |    0.000 | rank-biserial r    | non-zero differences: 7         | 1.000 |    1.000 |
| condition vs C0         | correct       | C0 M2 | C1 M2 |        75 |    0.947 |    0.947 |    0.000 | difference (b - a) | discordant: only a=1, only b=1  | 1.000 |    1.000 |
| condition vs C0         | faithfulness  | C0 M2 | C1 M2 |        73 |    0.904 |    0.884 |   -0.400 | rank-biserial r    | non-zero differences: 4         | 0.625 |    1.000 |
| condition vs C0         | correct       | C0 M2 | C2 M2 |        75 |    0.947 |    0.920 |   -0.027 | difference (b - a) | discordant: only a=3, only b=1  | 0.625 |    1.000 |
| condition vs C0         | faithfulness  | C0 M2 | C2 M2 |        74 |    0.905 |    0.890 |   -0.300 | rank-biserial r    | non-zero differences: 4         | 0.750 |    1.000 |
| condition vs C0         | correct       | C0 M2 | C3 M2 |        75 |    0.947 |    0.947 |    0.000 | difference (b - a) | discordant: only a=1, only b=1  | 1.000 |    1.000 |
| condition vs C0         | faithfulness  | C0 M2 | C3 M2 |        74 |    0.905 |    0.896 |   -0.167 | rank-biserial r    | non-zero differences: 3         | 1.000 |    1.000 |
| condition vs C0         | correct       | C0 M2 | C4 M2 |        75 |    0.947 |    0.587 |   -0.360 | difference (b - a) | discordant: only a=28, only b=1 | 0.000 |    0.000 |
| condition vs C0         | faithfulness  | C0 M2 | C4 M2 |        74 |    0.905 |    0.892 |   -0.200 | rank-biserial r    | non-zero differences: 5         | 1.000 |    1.000 |
| random vs related noise | correct       | C1 M2 | C2 M2 |        75 |    0.947 |    0.920 |   -0.027 | difference (b - a) | discordant: only a=2, only b=0  | 0.500 |    1.000 |
| random vs related noise | faithfulness  | C1 M2 | C2 M2 |        74 |    0.885 |    0.899 |    0.500 | rank-biserial r    | non-zero differences: 3         | 0.750 |    1.000 |

## C4 outcomes (counts)

| mitigation   |   gold only |   fake only |   both |   neither |   refused |
|:-------------|------------:|------------:|-------:|----------:|----------:|
| M0           |          48 |          20 |      5 |         2 |         0 |
| M1           |          45 |          20 |      4 |         3 |         3 |
| M2           |          41 |          28 |      3 |         3 |         0 |

## Faithfulness (>= 0.5) vs correctness, C0-C4 non-refused (counts)

| condition   |   faithful & correct |   faithful & wrong |   unfaithful & correct |   unfaithful & wrong |
|:------------|---------------------:|-------------------:|-----------------------:|---------------------:|
| C0          |                  200 |                  9 |                     12 |                    1 |
| C1          |                  193 |                 10 |                     16 |                    3 |
| C2          |                  193 |                 13 |                     13 |                    5 |
| C3          |                  196 |                  8 |                     15 |                    6 |
| C4          |                  138 |                 65 |                      8 |                   11 |

## Gold passage position (C1-C4, all mitigations)

| slot   |       n |   correct |   faithfulness |
|:-------|--------:|----------:|---------------:|
| first  | 159.000 |     0.899 |          0.886 |
| middle | 564.000 |     0.848 |          0.901 |
| last   | 177.000 |     0.859 |          0.916 |

Correctness by slot: chi-square = 2.75, p = 0.253. Faithfulness by slot: Kruskal-Wallis H = 1.34, p = 0.510.

## Refusal trade-off

| mitigation   |   refusal C5 unanswerable (n=20) |   refusal C5 gold removed (n=75) |   over-refusal C0-C4 (gold present) |
|:-------------|---------------------------------:|---------------------------------:|------------------------------------:|
| M0           |                            0.000 |                            0.093 |                               0.000 |
| M1           |                            0.350 |                            0.600 |                               0.021 |
| M2           |                            0.350 |                            0.427 |                               0.005 |

## Prior knowledge (closed-book correct vs not)

| condition   | mitigation   | known_closed_book   |   n |   correct |   followed_fake |   faithfulness |
|:------------|:-------------|:--------------------|----:|----------:|----------------:|---------------:|
| C0          | M0           | False               |  51 |     0.922 |         nan     |          0.912 |
| C0          | M0           | True                |  24 |     1.000 |         nan     |          1.000 |
| C0          | M1           | False               |  51 |     0.902 |         nan     |          0.918 |
| C0          | M1           | True                |  24 |     1.000 |         nan     |          0.944 |
| C0          | M2           | False               |  51 |     0.922 |         nan     |          0.880 |
| C0          | M2           | True                |  24 |     1.000 |         nan     |          0.958 |
| C1          | M0           | False               |  51 |     0.882 |         nan     |          0.902 |
| C1          | M0           | True                |  24 |     0.958 |         nan     |          0.923 |
| C1          | M1           | False               |  51 |     0.902 |         nan     |          0.888 |
| C1          | M1           | True                |  24 |     1.000 |         nan     |          0.951 |
| C1          | M2           | False               |  51 |     0.941 |         nan     |          0.853 |
| C1          | M2           | True                |  24 |     0.958 |         nan     |          0.957 |
| C2          | M0           | False               |  51 |     0.882 |         nan     |          0.915 |
| C2          | M0           | True                |  24 |     1.000 |         nan     |          0.917 |
| C2          | M1           | False               |  51 |     0.863 |         nan     |          0.900 |
| C2          | M1           | True                |  24 |     1.000 |         nan     |          0.958 |
| C2          | M2           | False               |  51 |     0.902 |         nan     |          0.873 |
| C2          | M2           | True                |  24 |     0.958 |         nan     |          0.931 |
| C3          | M0           | False               |  51 |     0.882 |         nan     |          0.886 |
| C3          | M0           | True                |  24 |     1.000 |         nan     |          0.917 |
| C3          | M1           | False               |  51 |     0.922 |         nan     |          0.873 |
| C3          | M1           | True                |  24 |     1.000 |         nan     |          0.958 |
| C3          | M2           | False               |  51 |     0.941 |         nan     |          0.902 |
| C3          | M2           | True                |  24 |     0.958 |         nan     |          0.889 |
| C4          | M0           | False               |  51 |     0.588 |           0.412 |          0.912 |
| C4          | M0           | True                |  24 |     0.958 |           0.167 |          0.958 |
| C4          | M1           | False               |  51 |     0.569 |           0.373 |          0.875 |
| C4          | M1           | True                |  24 |     0.875 |           0.250 |          0.875 |
| C4          | M2           | False               |  51 |     0.510 |           0.451 |          0.863 |
| C4          | M2           | True                |  24 |     0.750 |           0.333 |          0.958 |

C4 and memory: M0: followed fake 0.17 when known closed-book vs 0.41 when not (Fisher exact p = 0.040, Holm-adjusted over mitigations p = 0.120); M1: followed fake 0.25 when known closed-book vs 0.37 when not (Fisher exact p = 0.431, Holm-adjusted over mitigations p = 0.863); M2: followed fake 0.33 when known closed-book vs 0.45 when not (Fisher exact p = 0.452, Holm-adjusted over mitigations p = 0.863)

## Noise conditions: paired differences with 95% and 90% CIs (equivalence margin ±0.10)

Equivalent = the 90% CI lies entirely inside the margin (two one-sided tests at alpha 0.05).

| metric         | a     | b     |   n_pairs |   diff_b_minus_a |   ci95_lo |   ci95_hi |   ci90_lo |   ci90_hi | equivalent_within_0.10   |
|:---------------|:------|:------|----------:|-----------------:|----------:|----------:|----------:|----------:|:-------------------------|
| correct        | C0 M0 | C1 M0 |        75 |           -0.040 |    -0.093 |     0.000 |    -0.080 |     0.000 | True                     |
| correct        | C0 M0 | C2 M0 |        75 |           -0.027 |    -0.067 |     0.000 |    -0.067 |     0.000 | True                     |
| correct        | C0 M0 | C3 M0 |        75 |           -0.027 |    -0.080 |     0.027 |    -0.067 |     0.013 | True                     |
| correct        | C0 M1 | C1 M1 |        75 |            0.000 |    -0.040 |     0.040 |    -0.027 |     0.027 | True                     |
| correct        | C0 M1 | C2 M1 |        75 |           -0.027 |    -0.080 |     0.027 |    -0.067 |     0.013 | True                     |
| correct        | C0 M1 | C3 M1 |        75 |            0.013 |    -0.027 |     0.067 |    -0.027 |     0.053 | True                     |
| correct        | C0 M2 | C1 M2 |        75 |            0.000 |    -0.040 |     0.040 |    -0.027 |     0.027 | True                     |
| correct        | C0 M2 | C2 M2 |        75 |           -0.027 |    -0.080 |     0.027 |    -0.067 |     0.013 | True                     |
| correct        | C0 M2 | C3 M2 |        75 |            0.000 |    -0.040 |     0.040 |    -0.027 |     0.027 | True                     |
| correct        | C1 M0 | C2 M0 |        75 |            0.013 |    -0.040 |     0.067 |    -0.027 |     0.067 | True                     |
| correct        | C1 M1 | C2 M1 |        75 |           -0.027 |    -0.093 |     0.027 |    -0.080 |     0.027 | True                     |
| correct        | C1 M2 | C2 M2 |        75 |           -0.027 |    -0.067 |     0.000 |    -0.067 |     0.000 | True                     |
| correct_strict | C0 M0 | C1 M0 |        75 |           -0.040 |    -0.093 |     0.000 |    -0.080 |    -0.013 | True                     |
| correct_strict | C0 M0 | C2 M0 |        75 |           -0.053 |    -0.107 |    -0.013 |    -0.093 |    -0.013 | True                     |
| correct_strict | C0 M0 | C3 M0 |        75 |           -0.067 |    -0.133 |     0.000 |    -0.133 |    -0.013 | False                    |
| correct_strict | C0 M1 | C1 M1 |        75 |            0.013 |    -0.040 |     0.067 |    -0.027 |     0.067 | True                     |
| correct_strict | C0 M1 | C2 M1 |        75 |           -0.040 |    -0.107 |     0.027 |    -0.093 |     0.013 | True                     |
| correct_strict | C0 M1 | C3 M1 |        75 |            0.000 |    -0.067 |     0.067 |    -0.053 |     0.053 | True                     |
| correct_strict | C0 M2 | C1 M2 |        75 |           -0.013 |    -0.053 |     0.027 |    -0.053 |     0.027 | True                     |
| correct_strict | C0 M2 | C2 M2 |        75 |           -0.053 |    -0.120 |     0.013 |    -0.107 |     0.000 | False                    |
| correct_strict | C0 M2 | C3 M2 |        75 |           -0.027 |    -0.080 |     0.027 |    -0.067 |     0.013 | True                     |
| correct_strict | C1 M0 | C2 M0 |        75 |           -0.013 |    -0.067 |     0.040 |    -0.067 |     0.040 | True                     |
| correct_strict | C1 M1 | C2 M1 |        75 |           -0.053 |    -0.133 |     0.013 |    -0.120 |     0.000 | False                    |
| correct_strict | C1 M2 | C2 M2 |        75 |           -0.040 |    -0.093 |     0.000 |    -0.080 |    -0.013 | True                     |
| faithfulness   | C0 M0 | C1 M0 |        75 |           -0.031 |    -0.072 |     0.000 |    -0.065 |    -0.007 | True                     |
| faithfulness   | C0 M0 | C2 M0 |        75 |           -0.024 |    -0.067 |     0.009 |    -0.058 |     0.004 | True                     |
| faithfulness   | C0 M0 | C3 M0 |        75 |           -0.044 |    -0.087 |    -0.011 |    -0.078 |    -0.016 | True                     |
| faithfulness   | C0 M1 | C1 M1 |        72 |           -0.005 |    -0.049 |     0.042 |    -0.039 |     0.032 | True                     |
| faithfulness   | C0 M1 | C2 M1 |        72 |           -0.016 |    -0.062 |     0.028 |    -0.056 |     0.021 | True                     |
| faithfulness   | C0 M1 | C3 M1 |        73 |           -0.016 |    -0.071 |     0.034 |    -0.062 |     0.027 | True                     |
| faithfulness   | C0 M2 | C1 M2 |        73 |           -0.021 |    -0.075 |     0.027 |    -0.062 |     0.014 | True                     |
| faithfulness   | C0 M2 | C2 M2 |        74 |           -0.016 |    -0.063 |     0.027 |    -0.054 |     0.020 | True                     |
| faithfulness   | C0 M2 | C3 M2 |        74 |           -0.009 |    -0.050 |     0.032 |    -0.045 |     0.027 | True                     |
| faithfulness   | C1 M0 | C2 M0 |        75 |            0.007 |    -0.044 |     0.054 |    -0.036 |     0.047 | True                     |
| faithfulness   | C1 M1 | C2 M1 |        72 |            0.002 |    -0.058 |     0.065 |    -0.049 |     0.053 | True                     |
| faithfulness   | C1 M2 | C2 M2 |        74 |            0.014 |    -0.014 |     0.054 |    -0.007 |     0.041 | True                     |

## Sensitivity: correctness tests with the strict rule

| family                  | a     | b     |   n_pairs |   mean_a |   mean_b |   effect | detail                          |     p |   p_holm |
|:------------------------|:------|:------|----------:|---------:|---------:|---------:|:--------------------------------|------:|---------:|
| mitigation              | C0 M0 | C0 M1 |        75 |    0.920 |    0.880 |   -0.040 | discordant: only a=4, only b=1  | 0.375 |    1.000 |
| mitigation              | C0 M0 | C0 M2 |        75 |    0.920 |    0.947 |    0.027 | discordant: only a=2, only b=4  | 0.688 |    1.000 |
| mitigation              | C0 M1 | C0 M2 |        75 |    0.880 |    0.947 |    0.067 | discordant: only a=1, only b=6  | 0.125 |    1.000 |
| mitigation              | C1 M0 | C1 M1 |        75 |    0.880 |    0.893 |    0.013 | discordant: only a=2, only b=3  | 1.000 |    1.000 |
| mitigation              | C1 M0 | C1 M2 |        75 |    0.880 |    0.933 |    0.053 | discordant: only a=0, only b=4  | 0.125 |    1.000 |
| mitigation              | C1 M1 | C1 M2 |        75 |    0.893 |    0.933 |    0.040 | discordant: only a=0, only b=3  | 0.250 |    1.000 |
| mitigation              | C2 M0 | C2 M1 |        75 |    0.867 |    0.840 |   -0.027 | discordant: only a=3, only b=1  | 0.625 |    1.000 |
| mitigation              | C2 M0 | C2 M2 |        75 |    0.867 |    0.893 |    0.027 | discordant: only a=2, only b=4  | 0.688 |    1.000 |
| mitigation              | C2 M1 | C2 M2 |        75 |    0.840 |    0.893 |    0.053 | discordant: only a=1, only b=5  | 0.219 |    1.000 |
| mitigation              | C3 M0 | C3 M1 |        75 |    0.853 |    0.880 |    0.027 | discordant: only a=0, only b=2  | 0.500 |    1.000 |
| mitigation              | C3 M0 | C3 M2 |        75 |    0.853 |    0.920 |    0.067 | discordant: only a=0, only b=5  | 0.062 |    1.000 |
| mitigation              | C3 M1 | C3 M2 |        75 |    0.880 |    0.920 |    0.040 | discordant: only a=0, only b=3  | 0.250 |    1.000 |
| mitigation              | C4 M0 | C4 M1 |        75 |    0.640 |    0.613 |   -0.027 | discordant: only a=6, only b=4  | 0.754 |    1.000 |
| mitigation              | C4 M0 | C4 M2 |        75 |    0.640 |    0.560 |   -0.080 | discordant: only a=13, only b=7 | 0.263 |    1.000 |
| mitigation              | C4 M1 | C4 M2 |        75 |    0.613 |    0.560 |   -0.053 | discordant: only a=12, only b=8 | 0.503 |    1.000 |
| condition vs C0         | C0 M0 | C1 M0 |        75 |    0.920 |    0.880 |   -0.040 | discordant: only a=3, only b=0  | 0.250 |    1.000 |
| condition vs C0         | C0 M0 | C2 M0 |        75 |    0.920 |    0.867 |   -0.053 | discordant: only a=4, only b=0  | 0.125 |    1.000 |
| condition vs C0         | C0 M0 | C3 M0 |        75 |    0.920 |    0.853 |   -0.067 | discordant: only a=6, only b=1  | 0.125 |    1.000 |
| condition vs C0         | C0 M0 | C4 M0 |        75 |    0.920 |    0.640 |   -0.280 | discordant: only a=22, only b=1 | 0.000 |    0.000 |
| random vs related noise | C1 M0 | C2 M0 |        75 |    0.880 |    0.867 |   -0.013 | discordant: only a=3, only b=2  | 1.000 |    1.000 |
| condition vs C0         | C0 M1 | C1 M1 |        75 |    0.880 |    0.893 |    0.013 | discordant: only a=2, only b=3  | 1.000 |    1.000 |
| condition vs C0         | C0 M1 | C2 M1 |        75 |    0.880 |    0.840 |   -0.040 | discordant: only a=5, only b=2  | 0.453 |    1.000 |
| condition vs C0         | C0 M1 | C3 M1 |        75 |    0.880 |    0.880 |    0.000 | discordant: only a=3, only b=3  | 1.000 |    1.000 |
| condition vs C0         | C0 M1 | C4 M1 |        75 |    0.880 |    0.613 |   -0.267 | discordant: only a=23, only b=3 | 0.000 |    0.002 |
| random vs related noise | C1 M1 | C2 M1 |        75 |    0.893 |    0.840 |   -0.053 | discordant: only a=6, only b=2  | 0.289 |    1.000 |
| condition vs C0         | C0 M2 | C1 M2 |        75 |    0.947 |    0.933 |   -0.013 | discordant: only a=2, only b=1  | 1.000 |    1.000 |
| condition vs C0         | C0 M2 | C2 M2 |        75 |    0.947 |    0.893 |   -0.053 | discordant: only a=5, only b=1  | 0.219 |    1.000 |
| condition vs C0         | C0 M2 | C3 M2 |        75 |    0.947 |    0.920 |   -0.027 | discordant: only a=3, only b=1  | 0.625 |    1.000 |
| condition vs C0         | C0 M2 | C4 M2 |        75 |    0.947 |    0.560 |   -0.387 | discordant: only a=30, only b=1 | 0.000 |    0.000 |
| random vs related noise | C1 M2 | C2 M2 |        75 |    0.933 |    0.893 |   -0.040 | discordant: only a=3, only b=0  | 0.250 |    1.000 |

## Sensitivity: faithfulness vs strict correctness (counts)

| condition   |   faithful & correct |   faithful & wrong |   unfaithful & correct |   unfaithful & wrong |
|:------------|---------------------:|-------------------:|-----------------------:|---------------------:|
| C0          |                  195 |                 14 |                     11 |                    2 |
| C1          |                  187 |                 16 |                     16 |                    3 |
| C2          |                  183 |                 23 |                     12 |                    6 |
| C3          |                  186 |                 18 |                     13 |                    8 |
| C4          |                  127 |                 76 |                      8 |                   11 |
