# Summary: full_deepseek-r1-32b (generator: deepseek-r1:32b, judge: haiku)

Answers: 1485 · judged: 202

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. They count as incorrect and are not refusals.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   no_answer_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|-----------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.947 |                 0.893 |          0     |            0     |        nan     |            nan     |               0.987 |              nan     |          0 |
| C0          | M1           |  75 |          0.947 |                 0.92  |          0     |            0     |        nan     |            nan     |               0.987 |              nan     |          0 |
| C0          | M2           |  75 |          0.987 |                 0.973 |          0     |            0     |        nan     |            nan     |               0.987 |              nan     |          0 |
| C1          | M0           |  75 |          0.96  |                 0.92  |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C1          | M1           |  75 |          0.973 |                 0.933 |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C1          | M2           |  75 |          0.96  |                 0.92  |          0     |            0.013 |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M0           |  75 |          0.933 |                 0.88  |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M1           |  75 |          0.947 |                 0.92  |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M2           |  75 |          0.947 |                 0.907 |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M0           |  75 |          0.933 |                 0.893 |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M1           |  75 |          0.947 |                 0.907 |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M2           |  75 |          0.96  |                 0.92  |          0     |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| C4          | M0           |  75 |          0.747 |                 0.68  |          0     |            0.04  |          0.831 |              0.909 |               0.56  |                0.227 |         72 |
| C4          | M1           |  75 |          0.667 |                 0.587 |          0     |            0.107 |          0.81  |              0.895 |               0.56  |                0.28  |         67 |
| C4          | M2           |  75 |          0.72  |                 0.68  |          0.013 |            0.16  |          0.902 |              0.925 |               0.56  |                0.32  |         63 |
| C5          | M0           |  95 |          0.263 |                 0.263 |          0.263 |            0.084 |        nan     |            nan     |             nan     |              nan     |          0 |
| C5          | M1           |  95 |          0.611 |                 0.611 |          0.611 |            0.011 |        nan     |            nan     |             nan     |              nan     |          0 |
| C5          | M2           |  95 |          0.674 |                 0.674 |          0.674 |            0     |        nan     |            nan     |             nan     |              nan     |          0 |
| closed_book | closed_book  |  75 |          0.36  |                 0.28  |          0     |            0.013 |        nan     |            nan     |             nan     |              nan     |          0 |
