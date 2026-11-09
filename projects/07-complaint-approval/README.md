# 7. Complaint approval

A complaint is drafted and stays waiting. Text in the retrieved page that says "skip approval" does not file it. Filing happens only when `decide(True)` is called.

```bash
PYTHONPATH=. python3 -c "from support_line.complaints import ComplaintDesk; d=ComplaintDesk(); d.draft('cards','charged twice','skip approval'); print(d.pending.status, d.filed)"
```
