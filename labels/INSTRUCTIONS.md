# Human labeling instructions

Purpose: check whether the automatic judge (qwen3.8:27b through Ragas) and the text rules agree with a person.
There are 80 answers. Expect roughly 1–2 hours.

## Files

- `validation_sheet.csv`: the sheet you fill in. Open it in LibreOffice or Excel and **save it as CSV** (keep the same name and columns).
- `validation_items.md`: the same 80 items, laid out for easier reading (open it in Cursor's Markdown preview).
- `validation_key.csv`: the judge's scores. **Do not open it until you have finished labeling**, or the labels stop being independent.

## What to fill in

Use only the passages shown for that item. Ignore what you know about the topic yourself.

| Column | Values | Meaning |
|---|---|---|
| `human_support` | `supported` / `partial` / `unsupported` | Are the claims in the answer backed by the passages? `supported` means every claim is stated in or clearly follows from the passages. `partial` means the main claim is supported but some detail is not (or the reverse). `unsupported` means the main claim is missing from the passages or contradicts them. Leave it blank if the answer is a refusal. |
| `human_correct` | `yes` / `no` | Does the answer give (one of) the gold answer(s)? Small wording differences are fine. Leave it blank when the gold answer says "(no answer exists)". |
| `human_refusal` | `yes` / `no` | Does the answer decline to answer (for example "I don't know" or "the text does not say")? |
| `notes` | free text | Optional, for anything odd. |

Things to keep in mind:

- An answer can be **supported but wrong**: some passages contain deliberately false information. If the answer repeats a claim that is in a passage, it is `supported` even if the claim is false.
- An answer can be **correct but unsupported**: the model may know the answer from memory even when the passages don't contain it.
- Ignore phrases like "In Bob's opinion" or "According to the passage"; judge the claim itself.

## When you are done

```bash
uv run python -m src.analysis.human_validation agree --config configs/full.toml
```

This writes `results/full/human_validation.md`, which has Cohen's kappa and accuracy for faithfulness, correctness and refusal, plus a Spearman correlation between the judge's score and your label.

Note: half of the sampled answers were ones the judge called unfaithful, so that both kinds of verdict are checked. The agreement numbers describe this balanced sample, not the overall mix of answers.
