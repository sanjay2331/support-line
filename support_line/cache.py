"""Project 5. Cache a repeated question, and stop if the caller speaks over the reply."""

from __future__ import annotations

from dataclasses import dataclass

from support_line.corpus import CORPUS_VERSION
from support_line.gate import Contract, answer_question


def _key(question: str) -> str:
    return " ".join(question.lower().split())


@dataclass
class CallResult:
    contract: Contract
    cache_hit: bool
    model_called: bool
    cancelled: bool
    latency_ms: int


class CallCache:
    def __init__(self, version: str = CORPUS_VERSION) -> None:
        self.version = version
        self._store: dict[tuple[str, str], Contract] = {}

    def ask(self, question: str, barge_in: bool = False) -> CallResult:
        if barge_in:
            return CallResult(
                contract=Contract("I will stop.", (), 0.0, True, "barge_in"),
                cache_hit=False,
                model_called=False,
                cancelled=True,
                latency_ms=20,
            )
        cache_key = (_key(question), self.version)
        cached = self._store.get(cache_key)
        if cached is not None:
            return CallResult(cached, True, False, False, 15)
        contract = answer_question(question)
        # A fallback never spends a generation. A hit is cached for this corpus version.
        model_called = not contract.should_fallback
        if model_called:
            self._store[cache_key] = contract
        return CallResult(contract, False, model_called, False, 180 if model_called else 40)

    def drop_version(self, version: str) -> None:
        self.version = version
