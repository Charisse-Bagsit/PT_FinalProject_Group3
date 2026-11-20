from copy import deepcopy
from typing import List, Optional, Sequence

from vector_utils import Matrix, Vector, fmt_vec, vec_add, vec_leq, vec_sub
from banker_models import (
    BankerError,
    Comparison,
    RequestResult,
    SafetyResult,
    SafetyStep,
)

# re-exported so the GUI can do:  from banker_logic import BankersAlgorithm, BankerError
__all__ = [
    "BankersAlgorithm",
    "BankerError",
    "SafetyResult",
    "SafetyStep",
    "Comparison",
    "RequestResult",
]


class BankersAlgorithm:
    def __init__(
        self,
        total: Sequence[int],
        allocation: Sequence[Sequence[int]],
        max_claim: Sequence[Sequence[int]],
        process_names: Optional[Sequence[str]] = None,
        resource_names: Optional[Sequence[str]] = None,
    ):
        self.total: Vector = [int(x) for x in total]
        self.allocation: Matrix = [[int(x) for x in row] for row in allocation]
        self.max_claim: Matrix = [[int(x) for x in row] for row in max_claim]

        self.n = len(self.allocation)  # number of processes
        self.m = len(self.total)  # number of resource types

        self.process_names = (
            list(process_names) if process_names else [f"P{i}" for i in range(self.n)]
        )
        self.resource_names = (
            list(resource_names)
            if resource_names
            else [chr(65 + j) for j in range(self.m)]
        )

        self.validate()

    # ---------------- validation ----------------
    def validate(self):
        if self.n == 0 or self.m == 0:
            raise BankerError("There must be at least 1 process and 1 resource type.")
        if len(self.max_claim) != self.n:
            raise BankerError(
                "Allocation and Max must have the same number of processes."
            )
        if len(self.process_names) != self.n:
            raise BankerError(
                "process_names length must equal the number of processes."
            )
        if len(self.resource_names) != self.m:
            raise BankerError(
                "resource_names length must equal the number of resource types."
            )

        for name, mat in (("Allocation", self.allocation), ("Max", self.max_claim)):
            for i, row in enumerate(mat):
                if len(row) != self.m:
                    raise BankerError(
                        f"{name} row {self.process_names[i]} must have {self.m} values."
                    )
                if any(x < 0 for x in row):
                    raise BankerError(
                        f"{name} values cannot be negative ({self.process_names[i]})."
                    )
        if any(x < 0 for x in self.total):
            raise BankerError("Total resources cannot be negative.")

        for i in range(self.n):
            if not vec_leq(self.allocation[i], self.max_claim[i]):
                raise BankerError(
                    f"{self.process_names[i]}: Allocation {fmt_vec(self.allocation[i])} "
                    f"exceeds Max {fmt_vec(self.max_claim[i])}."
                )
        if not vec_leq(self.total_allocated, self.total):
            raise BankerError(
                f"Total allocated {fmt_vec(self.total_allocated)} exceeds Total {fmt_vec(self.total)}."
            )

    # ---------------- derived values ----------------
    @property
    def need(self) -> Matrix:
        """Need = Max - Allocation."""
        return [vec_sub(self.max_claim[i], self.allocation[i]) for i in range(self.n)]

    @property
    def total_allocated(self) -> Vector:
        """Column sums of Allocation."""
        return [
            sum(self.allocation[i][j] for i in range(self.n)) for j in range(self.m)
        ]

    @property
    def available(self):
        """Available = Total - column sums of Allocation."""
        return vec_sub(self.total, self.total_allocated)

    # ---------------- safety algorithm ----------------
    def safety_check(
        self,
        available: Optional[Sequence[int]] = None,
        allocation: Optional[Matrix] = None,
        need: Optional[Matrix] = None,
    ) -> SafetyResult:
        """
        Run the safety algorithm on the current state (no arguments) or on a
        tentative state (used by request_resources). Each iteration scans from
        process index 0 and picks the first unfinished one with Need <= Work.
        """
        alloc = allocation if allocation is not None else self.allocation
        nd = need if need is not None else self.need
        work: Vector = list(available if available is not None else self.available)

        finish = [False] * self.n
        sequence: List[str] = []
        steps: List[SafetyStep] = []
        initial_work = list(work)
        iteration = 0

        while True:
            iteration += 1
            work_before = list(work)
            comparisons: List[Comparison] = []
            chosen = None

            for i in range(self.n):
                if finish[i]:
                    continue
                ok = vec_leq(nd[i], work)
                comparisons.append(
                    Comparison(self.process_names[i], list(nd[i]), list(work), ok)
                )
                if ok:
                    chosen = i
                    break

            if chosen is None:
                if comparisons:  # record the failed pass
                    steps.append(
                        SafetyStep(
                            iteration,
                            work_before,
                            comparisons,
                            None,
                            None,
                            list(work),
                            list(finish),
                        )
                    )
                break

            released = list(alloc[chosen])
            work = vec_add(work, released)
            finish[chosen] = True
            sequence.append(self.process_names[chosen])
            steps.append(
                SafetyStep(
                    iteration,
                    work_before,
                    comparisons,
                    self.process_names[chosen],
                    released,
                    list(work),
                    list(finish),
                )
            )

            if all(finish):
                break

        is_safe = all(finish)
        unfinished = [self.process_names[i] for i in range(self.n) if not finish[i]]
        return SafetyResult(
            is_safe, sequence, steps, initial_work, list(finish), unfinished
        )

    # ---------------- resource request ----------------
    def request_resources(
        self, process, request: Sequence[int], apply: bool = False
    ) -> RequestResult:
        """
        Resource-request algorithm. `process` may be an index or a name.
        If apply=True and the request is GRANTED, the state is updated.
        """
        i = self.process_index(process)
        pname = self.process_names[i]
        req = [int(x) for x in request]

        if len(req) != self.m:
            raise BankerError(f"Request must have {self.m} values.")
        if any(x < 0 for x in req):
            raise BankerError("Request values cannot be negative.")

        need_i = self.need[i]

        # Step 1: Request <= Need ?
        if not vec_leq(req, need_i):
            return RequestResult(
                pname,
                req,
                need_ok=False,
                available_ok=None,
                decision="ERROR",
                reason=f"Request {fmt_vec(req)} > Need {fmt_vec(need_i)}: "
                f"{pname} exceeded its maximum claim.",
            )

        # Step 2: Request <= Available ?
        avail = self.available
        if not vec_leq(req, avail):
            return RequestResult(
                pname,
                req,
                need_ok=True,
                available_ok=False,
                decision="WAIT",
                reason=f"Request {fmt_vec(req)} > Available {fmt_vec(avail)}: "
                f"{pname} must wait.",
            )

        # Step 3: tentative allocation
        t_avail = vec_sub(avail, req)
        t_alloc_i = vec_add(self.allocation[i], req)
        t_need_i = vec_sub(need_i, req)

        t_alloc = deepcopy(self.allocation)
        t_alloc[i] = t_alloc_i
        t_need = deepcopy(self.need)
        t_need[i] = t_need_i

        # Step 4: safety check on the tentative state
        safety = self.safety_check(available=t_avail, allocation=t_alloc, need=t_need)

        if safety.is_safe:
            decision = "GRANT"
            reason = (
                "Tentative state is SAFE, request GRANTED. Safe sequence: < "
                + ", ".join(safety.safe_sequence)
                + " >"
            )
            if apply:
                self.allocation = t_alloc
        else:
            decision = "WAIT"
            reason = (
                "Tentative state is UNSAFE, request not granted (rolled back). "
                f"{pname} must wait."
            )

        return RequestResult(
            pname,
            req,
            True,
            True,
            decision,
            reason,
            t_avail,
            t_alloc_i,
            t_need_i,
            safety,
        )

    def process_index(self, process):
        """Accepts an index (int) or a process name (str)."""
        if isinstance(process, int):
            if 0 <= process < self.n:
                return process
            raise BankerError(f"Process index {process} out of range.")
        if process in self.process_names:
            return self.process_names.index(process)
        raise BankerError(f"Unknown process '{process}'.")
