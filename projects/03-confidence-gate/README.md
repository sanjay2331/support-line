# 3. Confidence gate

A question with no overlap falls back to the menu and cites nothing. A policy question cites the chunk that was actually retrieved. A citation that was not retrieved is rejected.

```bash
PYTHONPATH=. python3 -c "from support_line.gate import answer_question; print(answer_question('what is the weather in hassan today'))"
```
