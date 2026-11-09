"""Project 10. Injection, another person's account, and raw text in the log."""

from __future__ import annotations

import hashlib

from support_line.accounts import reply_balance
from support_line.complaints import ComplaintDesk


SYSTEM_PROMPT = "You answer only from retrieved support articles."


def resist_prompt_leak(utterance: str) -> str:
    text = utterance.lower()
    if "system prompt" in text or "ignore your instructions" in text:
        return "I can help with a product question."
    return "Ask a product question."


def log_utterance(utterance: str) -> dict[str, str]:
    digest = hashlib.sha256(utterance.encode("utf-8")).hexdigest()[:12]
    return {"utterance_sha256": digest, "stored_text": ""}


def injection_cannot_file(page_text: str) -> str:
    desk = ComplaintDesk()
    desk.draft("cards", "card was charged twice", page_text)
    # The caller has not approved. The page text must not file the ticket.
    return desk.pending.status if desk.pending else "missing"
