# 1. Intent router

Known requests stay on the script. "What is my balance" does not call retrieval. "Why is there a minimum balance fee" does. "Connect me to an agent" escalates.

```bash
PYTHONPATH=. python3 -c "from support_line.router import route; print(route('what is my balance'))"
```
