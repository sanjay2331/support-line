"""Project 9. A labeled set fails the run when retrieval gets worse."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from support_line.corpus import ROOT, load_faqs
from support_line.gate import answer_question
from support_line.search import hybrid_search

EVAL_PATH = ROOT / "data" / "eval_questions.jsonl"


@dataclass(frozen=True)
class EvalReport:
    recall_at_3: float
    fallback_accuracy: float
    passed: bool
    misses: tuple[str, ...]


def load_questions(path: Path = EVAL_PATH) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _recall(question: str, expected: list[str], broken: bool) -> bool:
    if broken:
        # A bad index that only ever returns the first FAQ.
        top = [load_faqs()[0].id]
    else:
        top = [hit.faq.id for hit in hybrid_search(question, k=3)]
    return any(eid in top for eid in expected)


def evaluate(broken: bool = False) -> EvalReport:
    misses: list[str] = []
    recall_hits = 0
    recall_total = 0
    fallback_hits = 0
    fallback_total = 0
    for row in load_questions():
        if row["expect_fallback"]:
            fallback_total += 1
            contract = answer_question(row["question"])
            ok = contract.should_fallback if not broken else False
            fallback_hits += int(ok)
            if not ok:
                misses.append(row["id"])
            continue
        recall_total += 1
        ok = _recall(row["question"], row["expected_ids"], broken)
        recall_hits += int(ok)
        if not ok:
            misses.append(row["id"])
    recall = recall_hits / recall_total
    fallback = fallback_hits / fallback_total
    passed = recall >= 0.99 and fallback >= 0.99 and not broken
    return EvalReport(recall, fallback, passed, tuple(misses))
