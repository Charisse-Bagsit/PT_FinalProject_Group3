from dataclasses import dataclass
from typing import List, Optional

from vector_utils import Vector


class BankerError(ValueError):
    """Raised when the input data is invalid."""


@dataclass
class Comparison:
    """One 'Need <= Work' test."""

    process: str
    need: Vector
    work: Vector
    passed: bool


@dataclass
class SafetyStep:
    """One iteration of the safety algorithm."""

    iteration: int
    work_before: Vector
    comparisons: List[Comparison]  # every test made during this iteration
    process: Optional[str]  # process selected (None = nobody could run)
    allocation_released: Optional[Vector]
    work_after: Vector
    finish: List[bool]  # Finish flags after this iteration


@dataclass
class SafetyResult:
    is_safe: bool
    safe_sequence: List[str]
    steps: List[SafetyStep]
    initial_work: Vector
    final_finish: List[bool]
    unfinished: List[str]  # processes that could not finish (unsafe)

    @property
    def message(self) -> str:
        if self.is_safe:
            return (
                "SAFE STATE. Safe sequence: < " + ", ".join(self.safe_sequence) + " >"
            )
        return "UNSAFE STATE. Cannot finish: " + ", ".join(self.unfinished)


@dataclass
class RequestResult:
    process: str
    request: Vector
    need_ok: bool  # Request <= Need
    available_ok: Optional[bool]  # Request <= Available (None if not reached)
    decision: str  # "GRANT", "WAIT" or "ERROR"
    reason: str
    tentative_available: Optional[Vector] = None
    tentative_allocation: Optional[Vector] = None  # row of the requesting process
    tentative_need: Optional[Vector] = None  # row of the requesting process
    safety: Optional[SafetyResult] = None
