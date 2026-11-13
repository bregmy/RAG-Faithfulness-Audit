# Summary: full_llama3.1-8b (generator: llama3.1:8b, judge: local)

Answers: 1485 · judged: 1410

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. They count as incorrect and are not refusals.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   no_answer_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|-----------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.973 |                 0.933 |          0     |                0 |          0.939 |              0.858 |               0.987 |              nan     |         75 |
| C0          | M1           |  75 |          0.947 |                 0.933 |          0.04  |                0 |          0.941 |              0.808 |               0.987 |              nan     |         75 |
| C0          | M2           |  75 |          0.213 |                 0.227 |          0.76  |                0 |          0.963 |              0.755 |               0.987 |              nan     |         75 |
| C1          | M0           |  75 |          1     |                 0.987 |          0     |                0 |          0.941 |              0.788 |               0.247 |              nan     |         75 |
| C1          | M1           |  75 |          0.947 |                 0.933 |          0.04  |                0 |          0.887 |              0.715 |               0.247 |              nan     |         75 |
| C1          | M2           |  75 |          0.053 |                 0.053 |          0.947 |                0 |          0.75  |              0.776 |               0.247 |              nan     |         75 |
| C2          | M0           |  75 |          0.987 |                 0.933 |          0     |                0 |          0.907 |              0.823 |               0.327 |              nan     |         75 |
| C2          | M1           |  75 |          0.88  |                 0.88  |          0.093 |                0 |          0.961 |              0.729 |               0.327 |              nan     |         75 |
| C2          | M2           |  75 |          0.227 |                 0.227 |          0.773 |                0 |          0.941 |              0.807 |               0.327 |              nan     |         75 |
| C3          | M0           |  75 |          0.987 |                 0.933 |          0     |                0 |          0.931 |              0.814 |               0.187 |              nan     |         75 |
| C3          | M1           |  75 |          0.867 |                 0.84  |          0.12  |                0 |          0.937 |              0.715 |               0.187 |              nan     |         75 |
| C3          | M2           |  75 |          0.307 |                 0.307 |          0.693 |                0 |          0.913 |              0.788 |               0.187 |              nan     |         75 |
| C4          | M0           |  75 |          0.707 |                 0.64  |          0     |                0 |          0.896 |              0.824 |               0.557 |                0.453 |         75 |
| C4          | M1           |  75 |          0.6   |                 0.56  |          0.133 |                0 |          0.831 |              0.741 |               0.557 |                0.48  |         75 |
| C4          | M2           |  75 |          0.133 |                 0.12  |          0.773 |                0 |          0.794 |              0.81  |               0.557 |                0.107 |         75 |
| C5          | M0           |  95 |          0.274 |                 0.274 |          0.274 |                0 |          0.601 |              0.771 |               0.124 |              nan     |         95 |
| C5          | M1           |  95 |          0.789 |                 0.789 |          0.789 |                0 |          0.475 |              0.668 |               0.124 |              nan     |         95 |
| C5          | M2           |  95 |          0.989 |                 0.989 |          0.989 |                0 |          0     |              1     |               0.124 |              nan     |         95 |
| closed_book | closed_book  |  75 |          0.4   |                 0.307 |          0.027 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
