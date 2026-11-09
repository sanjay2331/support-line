"""Project 6. A balance is spoken only when the core tool returned it."""

from __future__ import annotations

import re
from dataclasses import dataclass

_LEDGER = {"4421": 15230.50, "1008": 840.00}
_LAST4 = re.compile(r"\b(\d{4})\b")


@dataclass(frozen=True)
class BalanceReply:
    spoken: str
    amount: float | None
    source: str
    refused: bool


def get_balance(last4: str) -> float | None:
    return _LEDGER.get(last4)


def reply_balance(utterance: str, caller_last4: str) -> BalanceReply:
    text = utterance.lower()
    if any(phrase in text for phrase in ("someone else", "another person", "wife's account", "his account", "her account")):
        return BalanceReply(
            "I can only read the account of the person on this call.",
            None,
            "refused",
            True,
        )
    found = _LAST4.findall(utterance)
    last4 = found[-1] if found else caller_last4
    if last4 != caller_last4:
        return BalanceReply(
            "I can only read the account of the person on this call.",
            None,
            "refused",
            True,
        )
    amount = get_balance(last4)
    if amount is None:
        return BalanceReply("I could not find that account on the core system.", None, "core_tool", False)
    return BalanceReply(f"The available balance is {amount:.2f} rupees.", amount, "core_tool", False)
