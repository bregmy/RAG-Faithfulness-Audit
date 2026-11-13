# Summary: pilot

Answers: 158 · judged: 150

- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. `correct_strict_rate` requires the exact gold answer.
- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.
- `context_precision`: share of passages in the context that the judge rated relevant to the question.
- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.

| condition   | mitigation   |   n |   correct_rate |   correct_strict_rate |   refusal_rate |   faithfulness |   answer_relevancy |   context_precision |   followed_fake_rate |   n_judged |
|:------------|:-------------|----:|---------------:|----------------------:|---------------:|---------------:|-------------------:|--------------------:|---------------------:|-----------:|
| C0          | M0           |   8 |          1     |                 1     |            0   |          0.938 |              0.915 |               1     |              nan     |          8 |
| C0          | M1           |   8 |          1     |                 1     |            0   |          0.938 |              0.915 |               1     |              nan     |          8 |
| C0          | M2           |   8 |          1     |                 1     |            0   |          1     |              0.921 |               1     |              nan     |          8 |
| C1          | M0           |   8 |          1     |                 1     |            0   |          1     |              0.91  |               0.25  |              nan     |          8 |
| C1          | M1           |   8 |          1     |                 1     |            0   |          1     |              0.915 |               0.25  |              nan     |          8 |
| C1          | M2           |   8 |          1     |                 1     |            0   |          0.875 |              0.907 |               0.25  |              nan     |          8 |
| C2          | M0           |   8 |          0.75  |                 0.75  |            0   |          0.875 |              0.906 |               0.438 |              nan     |          8 |
| C2          | M1           |   8 |          0.75  |                 0.75  |            0   |          0.875 |              0.932 |               0.438 |              nan     |          8 |
| C2          | M2           |   8 |          0.75  |                 0.75  |            0   |          0.875 |              0.931 |               0.438 |              nan     |          8 |
| C3          | M0           |   8 |          1     |                 1     |            0   |          0.969 |              0.91  |               0.25  |              nan     |          8 |
| C3          | M1           |   8 |          1     |                 1     |            0   |          1     |              0.912 |               0.25  |              nan     |          8 |
| C3          | M2           |   8 |          1     |                 1     |            0   |          1     |              0.925 |               0.25  |              nan     |          8 |
| C4          | M0           |   8 |          0.75  |                 0.75  |            0   |          1     |              0.934 |               0.656 |                0.125 |          8 |
| C4          | M1           |   8 |          0.875 |                 0.875 |            0   |          1     |              0.91  |               0.656 |                0.125 |          8 |
| C4          | M2           |   8 |          1     |                 1     |            0   |          1     |              0.903 |               0.656 |                0.125 |          8 |
| C5          | M0           |  10 |          0.1   |                 0.1   |            0.1 |          0.444 |              0.76  |               0.225 |              nan     |         10 |
| C5          | M1           |  10 |          0.4   |                 0.4   |            0.4 |          0.417 |              0.813 |               0.225 |              nan     |         10 |
| C5          | M2           |  10 |          0.3   |                 0.3   |            0.3 |          0.357 |              0.887 |               0.225 |              nan     |         10 |
| closed_book | closed_book  |   8 |          0.25  |                 0.125 |            0   |        nan     |            nan     |             nan     |              nan     |          0 |
