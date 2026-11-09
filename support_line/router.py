"""Project 1. Keep known requests on the script. Send open questions to retrieval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    intent: str
    product: str
    path: str  # script, rag, approve, human


_BALANCE = ("balance", "bakaya", "बकाया", "how much do i have")
_CARD = ("block card", "block my card", "card block", "debit card block", "कार्ड ब्लॉक")
_LOAN = ("emi", "home loan", "loan status", "लोन")
_COMPLAINT = ("complaint", "shikayat", "शिकायत", "raise a ticket")
_HUMAN = ("human", "agent", "executive", "person", "representative")
_POLICY = ("why", "what is the", "kitna charge", "fee", "policy", "minimum balance", "code cb")


def route(utterance: str) -> Route:
    text = " ".join(utterance.lower().split())
    if any(word in text for word in _HUMAN):
        return Route("escalate", "any", "human")
    if any(word in text for word in _COMPLAINT):
        return Route("complaint", "complaints", "approve")
    if any(word in text for word in _POLICY) and not text.startswith("what is my balance"):
        product = "cards" if "card" in text or "cb-" in text else "savings" if "balance" in text or "fee" in text else "loans" if "emi" in text or "loan" in text else "any"
        return Route("open_question", product, "rag")
    if any(word in text for word in _BALANCE):
        return Route("balance", "savings", "script")
    if any(word in text for word in _CARD):
        return Route("card_block", "cards", "script")
    if any(word in text for word in _LOAN):
        return Route("loan_status", "loans", "script")
    return Route("open_question", "any", "rag")
