# 6. Account facts from tools

The balance is read from a small ledger tool. The reply names that source. A request for another person's last four digits is refused, and no amount is returned.

```bash
PYTHONPATH=. python3 -c "from support_line.accounts import reply_balance; print(reply_balance('what is my balance', '4421'))"
```
