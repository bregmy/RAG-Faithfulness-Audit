# Summary: full (generator: qwen3:8b, judge: local)

Answers: 1485 · judged: 1410

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. They count as incorrect and are not refusals.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   no_answer_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|-----------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.947 |                 0.92  |          0     |                0 |          0.94  |              0.916 |               0.987 |              nan     |         75 |
| C0          | M1           |  75 |          0.933 |                 0.88  |          0.027 |                0 |          0.927 |              0.911 |               0.987 |              nan     |         75 |
| C0          | M2           |  75 |          0.947 |                 0.947 |          0.013 |                0 |          0.905 |              0.914 |               0.987 |              nan     |         75 |
| C1          | M0           |  75 |          0.907 |                 0.88  |          0     |                0 |          0.909 |              0.92  |               0.247 |              nan     |         75 |
| C1          | M1           |  75 |          0.933 |                 0.893 |          0.027 |                0 |          0.909 |              0.92  |               0.247 |              nan     |         75 |
| C1          | M2           |  75 |          0.947 |                 0.933 |          0.013 |                0 |          0.885 |              0.919 |               0.247 |              nan     |         75 |
| C2          | M0           |  75 |          0.92  |                 0.867 |          0     |                0 |          0.916 |              0.914 |               0.327 |              nan     |         75 |
| C2          | M1           |  75 |          0.907 |                 0.84  |          0.013 |                0 |          0.919 |              0.895 |               0.327 |              nan     |         75 |
| C2          | M2           |  75 |          0.92  |                 0.893 |          0     |                0 |          0.891 |              0.922 |               0.327 |              nan     |         75 |
| C3          | M0           |  75 |          0.92  |                 0.853 |          0     |                0 |          0.896 |              0.912 |               0.187 |              nan     |         75 |
| C3          | M1           |  75 |          0.947 |                 0.88  |          0     |                0 |          0.9   |              0.902 |               0.187 |              nan     |         75 |
| C3          | M2           |  75 |          0.947 |                 0.92  |          0     |                0 |          0.898 |              0.919 |               0.187 |              nan     |         75 |
| C4          | M0           |  75 |          0.707 |                 0.64  |          0     |                0 |          0.927 |              0.921 |               0.557 |                0.333 |         75 |
| C4          | M1           |  75 |          0.667 |                 0.613 |          0.04  |                0 |          0.875 |              0.903 |               0.557 |                0.333 |         75 |
| C4          | M2           |  75 |          0.587 |                 0.56  |          0     |                0 |          0.893 |              0.92  |               0.557 |                0.413 |         75 |
| C5          | M0           |  95 |          0.074 |                 0.074 |          0.074 |                0 |          0.33  |              0.864 |               0.124 |              nan     |         95 |
| C5          | M1           |  95 |          0.547 |                 0.547 |          0.547 |                0 |          0.419 |              0.855 |               0.124 |              nan     |         95 |
| C5          | M2           |  95 |          0.411 |                 0.411 |          0.411 |                0 |          0.29  |              0.892 |               0.124 |              nan     |         95 |
| closed_book | closed_book  |  75 |          0.32  |                 0.187 |          0     |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
