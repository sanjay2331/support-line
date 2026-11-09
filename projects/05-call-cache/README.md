# 5. Call cache

The first confident answer is stored. The same question on the next call does not call the model. Changing the corpus version misses the cache. If the caller speaks over the reply, generation is cancelled.

```bash
PYTHONPATH=. python3 -c "from support_line.cache import CallCache; c=CallCache(); q='why is there a minimum balance fee'; print(c.ask(q).model_called, c.ask(q).cache_hit)"
```
