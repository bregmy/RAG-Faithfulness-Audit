# Summary: full (generator: qwen3:8b, judge: haiku)

Answers: 1485 · judged: 293

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. They count as incorrect and are not refusals.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   no_answer_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|-----------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.947 |                 0.92  |          0     |                0 |          0.5   |              0.874 |               1     |              nan     |          4 |
| C0          | M1           |  75 |          0.933 |                 0.88  |          0.027 |                0 |          0.5   |              0.854 |               1     |              nan     |          4 |
| C0          | M2           |  75 |          0.947 |                 0.947 |          0.013 |                0 |          0.875 |              0.932 |               1     |              nan     |          5 |
| C1          | M0           |  75 |          0.907 |                 0.88  |          0     |                0 |          0.75  |              0.89  |               0.25  |              nan     |          4 |
| C1          | M1           |  75 |          0.933 |                 0.893 |          0.027 |                0 |          0.5   |              0.865 |               0.25  |              nan     |          4 |
| C1          | M2           |  75 |          0.947 |                 0.933 |          0.013 |                0 |          0.625 |              0.92  |               0.25  |              nan     |          4 |
| C2          | M0           |  75 |          0.92  |                 0.867 |          0     |                0 |          0.75  |              0.827 |               0.371 |              nan     |          4 |
| C2          | M1           |  75 |          0.907 |                 0.84  |          0.013 |                0 |          0.75  |              0.951 |               0.371 |              nan     |          4 |
| C2          | M2           |  75 |          0.92  |                 0.893 |          0     |                0 |          0.5   |              0.904 |               0.371 |              nan     |          4 |
| C3          | M0           |  75 |          0.92  |                 0.853 |          0     |                0 |          0.625 |              0.85  |               0.22  |              nan     |          4 |
| C3          | M1           |  75 |          0.947 |                 0.88  |          0     |                0 |          0.5   |              0.685 |               0.22  |              nan     |          4 |
| C3          | M2           |  75 |          0.947 |                 0.92  |          0     |                0 |          0.5   |              0.943 |               0.22  |              nan     |          4 |
| C4          | M0           |  75 |          0.707 |                 0.64  |          0     |                0 |          0.86  |              0.899 |               0.56  |                0.333 |         75 |
| C4          | M1           |  75 |          0.667 |                 0.613 |          0.04  |                0 |          0.74  |              0.884 |               0.56  |                0.333 |         75 |
| C4          | M2           |  75 |          0.587 |                 0.56  |          0     |                0 |          0.767 |              0.907 |               0.56  |                0.413 |         75 |
| C5          | M0           |  95 |          0.074 |                 0.074 |          0.074 |                0 |          0.417 |              0.935 |               0.162 |              nan     |          7 |
| C5          | M1           |  95 |          0.547 |                 0.547 |          0.547 |                0 |          0.625 |              0.845 |               0.162 |              nan     |          7 |
| C5          | M2           |  95 |          0.411 |                 0.411 |          0.411 |                0 |          0.333 |              0.901 |               0.162 |              nan     |          5 |
| closed_book | closed_book  |  75 |          0.32  |                 0.187 |          0     |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
