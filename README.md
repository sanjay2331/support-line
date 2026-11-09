# Support line

Ten small projects from one job: a production support assistant that answers from company knowledge, stays short enough to speak, and hands off when it is not sure.

The corpus in `data/` is synthetic. There are no bank documents, call recordings, or customer records.

Run everything:

```bash
python3 -m unittest tests.test_support_line -v
python3 -m support_line.demo
```

Stdlib only. Python 3.11+.

| # | Project | Market failure it closes |
|---|---|---|
| 1 | [Intent router](projects/01-intent-router) | Sending every utterance to a large model |
| 2 | [Hybrid FAQ search](projects/02-hybrid-faq-search) | Vector search missing an exact product code |
| 3 | [Confidence gate](projects/03-confidence-gate) | Speaking a policy that was never retrieved |
| 4 | [Code-mix voice reply](projects/04-codemix-voice) | Hinglish questions answered with a chat essay |
| 5 | [Call cache](projects/05-call-cache) | Paying the model again for the same question, and talking over the caller |
| 6 | [Account facts from tools](projects/06-account-facts) | A model inventing a balance |
| 7 | [Complaint approval](projects/07-complaint-approval) | A ticket filed because a page said to skip approval |
| 8 | [Handover brief](projects/08-handover-brief) | A person picking up the call with no context |
| 9 | [Eval gate](projects/09-eval-gate) | A retrieval change shipping after quality dropped |
| 10 | [Safety checks](projects/10-safety-checks) | Prompt injection, another person's account, raw utterances in logs |
