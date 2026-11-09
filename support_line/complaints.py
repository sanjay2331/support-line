"""Project 7. A complaint is drafted, then filed only after a person approves."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Complaint:
    product: str
    reason: str
    status: str = "awaiting_approval"
    injected_override: bool = False


@dataclass
class ComplaintDesk:
    filed: list[Complaint] = field(default_factory=list)
    pending: Complaint | None = None

    def draft(self, product: str, reason: str, page_text: str = "") -> Complaint:
        override = "skip approval" in page_text.lower() or "skip approval" in reason.lower()
        self.pending = Complaint(product, reason, "awaiting_approval", override)
        return self.pending

    def decide(self, approve: bool) -> Complaint:
        if self.pending is None:
            raise RuntimeError("nothing is waiting")
        # An injected instruction does not change this branch.
        self.pending.status = "filed" if approve else "rejected"
        if approve:
            self.filed.append(self.pending)
        done = self.pending
        self.pending = None
        return done
