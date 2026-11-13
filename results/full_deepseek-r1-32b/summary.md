# Summary: full_deepseek-r1-32b (generator: deepseek-r1:32b, judge: local)

Answers: 1485 · judged: 1377

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.947 |                 0.893 |          0     |          0.893 |              0.925 |               0.987 |              nan     |         75 |
| C0          | M1           |  75 |          0.947 |                 0.92  |          0     |          0.888 |              0.896 |               0.987 |              nan     |         75 |
| C0          | M2           |  75 |          0.987 |                 0.973 |          0     |          0.916 |              0.922 |               0.987 |              nan     |         75 |
| C1          | M0           |  75 |          0.96  |                 0.92  |          0     |          0.894 |              0.922 |               0.247 |              nan     |         75 |
| C1          | M1           |  75 |          0.973 |                 0.933 |          0     |          0.887 |              0.909 |               0.247 |              nan     |         75 |
| C1          | M2           |  75 |          0.96  |                 0.92  |          0     |          0.905 |              0.927 |               0.247 |              nan     |         74 |
| C2          | M0           |  75 |          0.933 |                 0.88  |          0     |          0.935 |              0.924 |               0.327 |              nan     |         75 |
| C2          | M1           |  75 |          0.947 |                 0.92  |          0     |          0.917 |              0.923 |               0.327 |              nan     |         75 |
| C2          | M2           |  75 |          0.947 |                 0.907 |          0     |          0.932 |              0.913 |               0.327 |              nan     |         75 |
| C3          | M0           |  75 |          0.933 |                 0.893 |          0     |          0.931 |              0.929 |               0.187 |              nan     |         75 |
| C3          | M1           |  75 |          0.947 |                 0.907 |          0     |          0.916 |              0.932 |               0.187 |              nan     |         75 |
| C3          | M2           |  75 |          0.96  |                 0.92  |          0     |          0.931 |              0.927 |               0.187 |              nan     |         75 |
| C4          | M0           |  75 |          0.747 |                 0.68  |          0     |          0.91  |              0.92  |               0.557 |                0.227 |         72 |
| C4          | M1           |  75 |          0.667 |                 0.587 |          0     |          0.899 |              0.939 |               0.557 |                0.28  |         67 |
| C4          | M2           |  75 |          0.72  |                 0.68  |          0.013 |          0.96  |              0.92  |               0.557 |                0.32  |         63 |
| C5          | M0           |  95 |          0.263 |                 0.263 |          0.263 |          0.42  |              0.88  |               0.124 |              nan     |         87 |
| C5          | M1           |  95 |          0.611 |                 0.611 |          0.611 |          0.641 |              0.857 |               0.124 |              nan     |         94 |
| C5          | M2           |  95 |          0.674 |                 0.674 |          0.674 |          0.452 |              0.874 |               0.124 |              nan     |         95 |
| closed_book | closed_book  |  75 |          0.36  |                 0.28  |          0     |        nan     |            nan     |             nan     |              nan     |          0 |
