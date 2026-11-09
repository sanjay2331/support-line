# 2. Hybrid FAQ search

Keyword rank finds the exact code CB-4421. A paraphrase such as "I lost my plastic and want it stopped" shares no words with the article, so the synonym channel carries it. The two ranks are fused.

```bash
PYTHONPATH=. python3 -c "from support_line.search import hybrid_search; print(hybrid_search('quote confirmation code CB-4421')[0])"
```
