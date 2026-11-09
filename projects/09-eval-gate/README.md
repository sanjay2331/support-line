# 9. Eval gate

`data/eval_questions.jsonl` labels the chunk that must appear, and the questions that must fall back. The current index passes. An index that only returns the first article fails.

```bash
PYTHONPATH=. python3 -c "from support_line.evaluate import evaluate; print(evaluate(False)); print(evaluate(True))"
```
