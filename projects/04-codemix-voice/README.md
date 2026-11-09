# 4. Code-mix voice reply

"mera debit card block karo" is marked as mixed language and routed to cards. Spoken text is capped at 25 words so it can be read on a call.

```bash
PYTHONPATH=. python3 -c "from support_line.voice import detect_product, is_code_mixed; u='mera debit card block karo'; print(detect_product(u), is_code_mixed(u))"
```
