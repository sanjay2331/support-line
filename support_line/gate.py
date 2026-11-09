"""Project 3. Answer only when retrieval is strong enough, and only cite what was retrieved."""

from __future__ import annotations

from dataclasses import dataclass

from support_line.corpus import load_faqs
from support_line.search import Hit, hybrid_search


@dataclass(frozen=True)
class Contract:
    answer: str
    citations: tuple[str, ...]
    confidence: float
    should_fallback: bool
    fallback_reason: str | None


def answer_question(question: str, product: str | None = None) -> Contract:
    hits = hybrid_search(question, product=product, k=3)
    top = hits[0] if hits else None
    # Reciprocal rank always nominates a winner. Confidence is the raw overlap.
    if top is None or (top.lexical_score <= 0 and top.dense_score <= 0):
        return Contract(
            answer="I am not sure enough to answer that. I will return you to the menu.",
            citations=(),
            confidence=0.0,
            should_fallback=True,
            fallback_reason="low_confidence",
        )
    chosen = _grounded(hits)
    return Contract(
        answer=chosen.faq.text,
        citations=(chosen.faq.id,),
        confidence=chosen.score,
        should_fallback=False,
        fallback_reason=None,
    )


def _grounded(hits: list[Hit]) -> Hit:
    """The spoken answer may only name a chunk that is in the retrieved set."""
    allowed = {hit.faq.id for hit in hits}
    top = hits[0]
    if top.faq.id not in allowed:
        raise RuntimeError("citation was not retrieved")
    return top


def reject_ungrounded(citations: list[str], retrieved_ids: list[str]) -> bool:
    return any(cid not in retrieved_ids for cid in citations) or not citations and not retrieved_ids


def spoken_or_fallback(question: str) -> Contract:
    contract = answer_question(question)
    if contract.should_fallback:
        return contract
    faqs = {faq.id: faq for faq in load_faqs()}
    for cid in contract.citations:
        if cid not in faqs:
            return Contract(
                answer="I am not sure enough to answer that. I will return you to the menu.",
                citations=(),
                confidence=contract.confidence,
                should_fallback=True,
                fallback_reason="citation_not_in_corpus",
            )
    return contract
