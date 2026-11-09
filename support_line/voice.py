"""Project 4. A Hindi-English mix still picks the product, and the reply stays short enough to speak."""

from __future__ import annotations

import re

_PRODUCTS = (
    ("cards", ("debit card", "credit card", "card", "कार्ड")),
    ("loans", ("home loan", "emi", "loan", "लोन")),
    ("savings", ("savings", "bachat", "balance", "बकाया")),
    ("complaints", ("complaint", "shikayat", "शिकायत")),
)
_SPOKEN_WORD_CAP = 25


def detect_product(utterance: str) -> str:
    text = utterance.lower()
    for product, phrases in _PRODUCTS:
        if any(phrase in text for phrase in phrases):
            return product
    return "any"


def is_code_mixed(utterance: str) -> bool:
    has_devanagari = bool(re.search(r"[\u0900-\u097f]", utterance))
    has_latin = bool(re.search(r"[A-Za-z]", utterance))
    hinglish_markers = any(word in utterance.lower() for word in ("mera", "karo", "hai", "ka"))
    return (has_devanagari and has_latin) or (hinglish_markers and has_latin)


def spoken(text: str, limit: int = _SPOKEN_WORD_CAP) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit])
