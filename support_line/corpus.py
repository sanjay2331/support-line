"""Load the synthetic FAQ corpus."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAQ_PATH = ROOT / "data" / "faqs.jsonl"
CORPUS_VERSION = "faqs-v1"


@dataclass(frozen=True)
class Faq:
    id: str
    product: str
    language: str
    text: str


def load_faqs(path: Path = FAQ_PATH) -> list[Faq]:
    faqs: list[Faq] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        faqs.append(Faq(row["id"], row["product"], row["language"], row["text"]))
    return faqs
