"""Project 2. Keyword search plus a synonym channel, fused with reciprocal rank."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from support_line.corpus import Faq, load_faqs

_TOKEN = re.compile(r"[a-z0-9]+|[\u0900-\u097f]+", re.IGNORECASE)
_STOP = {
    "a", "an", "the", "is", "in", "to", "of", "for", "and", "or", "my", "i",
    "it", "on", "was", "want", "that", "this", "there", "when", "why", "what",
    "how", "do", "does", "with", "from", "be", "if", "are", "can", "me",
}
_SYNONYMS = {
    "lost": "block",
    "stolen": "block",
    "stop": "block",
    "stopped": "block",
    "plastic": "card",
    "charges": "fee",
    "charge": "fee",
}


@dataclass(frozen=True)
class Hit:
    faq: Faq
    score: float
    lexical_rank: int
    dense_rank: int
    lexical_score: float
    dense_score: float


def tokenize(text: str) -> list[str]:
    return [tok.lower() for tok in _TOKEN.findall(text) if tok.lower() not in _STOP]


def _expand(tokens: list[str]) -> list[str]:
    expanded = list(tokens)
    for tok in tokens:
        if tok in _SYNONYMS:
            expanded.append(_SYNONYMS[tok])
    return expanded


def _bm25(query: list[str], docs: list[list[str]], k1: float = 1.2, b: float = 0.75) -> list[float]:
    n = len(docs)
    avg = sum(len(doc) for doc in docs) / n
    df: dict[str, int] = {}
    for doc in docs:
        for tok in set(doc):
            df[tok] = df.get(tok, 0) + 1
    scores: list[float] = []
    for doc in docs:
        tf: dict[str, int] = {}
        for tok in doc:
            tf[tok] = tf.get(tok, 0) + 1
        score = 0.0
        for tok in query:
            if tok not in tf:
                continue
            idf = math.log(1 + (n - df.get(tok, 0) + 0.5) / (df.get(tok, 0) + 0.5))
            freq = tf[tok]
            denom = freq + k1 * (1 - b + b * len(doc) / avg)
            score += idf * freq * (k1 + 1) / denom
        scores.append(score)
    return scores


def _ranks(scores: list[float]) -> list[int]:
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    ranks = [0] * len(scores)
    for place, idx in enumerate(order, start=1):
        ranks[idx] = place
    return ranks


def hybrid_search(question: str, faqs: list[Faq] | None = None, product: str | None = None, k: int = 3) -> list[Hit]:
    faqs = list(faqs or load_faqs())
    if product and product != "any":
        filtered = [faq for faq in faqs if faq.product == product]
        faqs = filtered or faqs
    lexical_docs = [tokenize(faq.text) for faq in faqs]
    dense_docs = [_expand(doc) for doc in lexical_docs]
    query = tokenize(question)
    lexical = _bm25(query, lexical_docs)
    dense = _bm25(_expand(query), dense_docs)
    lex_rank = _ranks(lexical)
    den_rank = _ranks(dense)
    fused: list[Hit] = []
    for i, faq in enumerate(faqs):
        # Reciprocal rank fusion. Higher is better.
        score = 1 / (60 + lex_rank[i]) + 1 / (60 + den_rank[i])
        fused.append(Hit(faq, score, lex_rank[i], den_rank[i], lexical[i], dense[i]))
    fused.sort(key=lambda hit: hit.score, reverse=True)
    return fused[:k]
