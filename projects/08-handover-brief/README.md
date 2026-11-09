# 8. Handover brief

When the call goes to a person, the packet names the intent, what was retrieved, and what was refused. It does not copy an account number into the summary.

```bash
PYTHONPATH=. python3 -c "from support_line.handover import build_handover; from support_line.router import route; print(build_handover(route('I want a human'), ['card-block'], ['other_account']).summary)"
```
