# Summary: full_llama3.1-8b (generator: llama3.1:8b, judge: gemini)

Answers: 1485 · judged: 225

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. They count as incorrect and are not refusals.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   no_answer_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|-----------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |  75 |          0.973 |                 0.933 |          0     |                0 |        nan     |            nan     |               1     |              nan     |          0 |
| C0          | M1           |  75 |          0.947 |                 0.933 |          0.04  |                0 |        nan     |            nan     |               1     |              nan     |          0 |
| C0          | M2           |  75 |          0.213 |                 0.227 |          0.76  |                0 |        nan     |            nan     |               1     |              nan     |          0 |
| C1          | M0           |  75 |          1     |                 0.987 |          0     |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C1          | M1           |  75 |          0.947 |                 0.933 |          0.04  |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C1          | M2           |  75 |          0.053 |                 0.053 |          0.947 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M0           |  75 |          0.987 |                 0.933 |          0     |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M1           |  75 |          0.88  |                 0.88  |          0.093 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C2          | M2           |  75 |          0.227 |                 0.227 |          0.773 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M0           |  75 |          0.987 |                 0.933 |          0     |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M1           |  75 |          0.867 |                 0.84  |          0.12  |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C3          | M2           |  75 |          0.307 |                 0.307 |          0.693 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C4          | M0           |  75 |          0.707 |                 0.64  |          0     |                0 |          0.887 |              0.846 |               0.547 |                0.453 |         75 |
| C4          | M1           |  75 |          0.6   |                 0.56  |          0.133 |                0 |          0.914 |              0.752 |               0.547 |                0.48  |         75 |
| C4          | M2           |  75 |          0.133 |                 0.12  |          0.773 |                0 |          0.765 |              0.835 |               0.547 |                0.107 |         75 |
| C5          | M0           |  95 |          0.274 |                 0.274 |          0.274 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C5          | M1           |  95 |          0.789 |                 0.789 |          0.789 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| C5          | M2           |  95 |          0.989 |                 0.989 |          0.989 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
| closed_book | closed_book  |  75 |          0.4   |                 0.307 |          0.027 |                0 |        nan     |            nan     |             nan     |              nan     |          0 |
