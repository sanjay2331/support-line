"""Project 8. The person who picks up the call gets a short packet, not a raw dump."""

from __future__ import annotations

from dataclasses import dataclass

from support_line.router import Route


@dataclass(frozen=True)
class Handover:
    intent: str
    product: str
    path: str
    retrieved_ids: tuple[str, ...]
    refused: tuple[str, ...]
    summary: str


def build_handover(route: Route, retrieved_ids: list[str], refused: list[str]) -> Handover:
    summary = (
        f"{route.intent} on {route.product}. "
        f"Retrieved {', '.join(retrieved_ids) or 'nothing'}. "
        f"Refused {', '.join(refused) or 'nothing'}."
    )
    return Handover(route.intent, route.product, route.path, tuple(retrieved_ids), tuple(refused), summary)
