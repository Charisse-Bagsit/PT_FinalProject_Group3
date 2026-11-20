from banker_logic import BankersAlgorithm
from banker_models import RequestResult, SafetyResult
from vector_utils import fmt_vec


def format_state(b: BankersAlgorithm):
    cols = "  ".join(f"{r:>3}" for r in b.resource_names)
    lines = [
        f"Total     : {fmt_vec(b.total)}",
        f"Allocated : {fmt_vec(b.total_allocated)}",
        f"Available : {fmt_vec(b.available)}",
        "",
        f"{'Process':<8} | Allocation {cols} | Max {cols} | Need {cols}",
    ]
    need = b.need
    for i in range(b.n):
        a = "  ".join(f"{x:>3}" for x in b.allocation[i])
        m = "  ".join(f"{x:>3}" for x in b.max_claim[i])
        n = "  ".join(f"{x:>3}" for x in need[i])
        lines.append(
            f"{b.process_names[i]:<8} | {'':<10} {a} | {'':<3} {m} | {'':<4} {n}"
        )
    return "\n".join(lines)


def format_safety(b: BankersAlgorithm, r: SafetyResult):
    lines = [
        f"Work = Available = {fmt_vec(r.initial_work)}",
        "Finish = " + str([False] * b.n),
        "",
    ]
    for s in r.steps:
        lines.append(f"Iteration {s.iteration}: Work = {fmt_vec(s.work_before)}")
        for c in s.comparisons:
            lines.append(
                f"   Check {c.process}: Need {fmt_vec(c.need)} <= Work {fmt_vec(c.work)} -> "
                f"{'TRUE' if c.passed else 'FALSE'}"
            )
        if s.process:
            lines.append(
                f"   {s.process} finishes, releases {fmt_vec(s.allocation_released)}"
            )
            lines.append(
                f"   Work = {fmt_vec(s.work_before)} + {fmt_vec(s.allocation_released)} "
                f"= {fmt_vec(s.work_after)}"
            )
        else:
            lines.append("   No unfinished process can proceed.")
        lines.append(f"   Finish = {s.finish}")
    lines += ["", "Result: " + r.message]
    return "\n".join(lines)


def format_request(b: BankersAlgorithm, r: RequestResult):
    need_i = b.need[b.process_index(r.process)]
    lines = [
        f"Request by {r.process}: {fmt_vec(r.request)}",
        f"Request <= Need      : {fmt_vec(r.request)} <= {fmt_vec(need_i)} -> {r.need_ok}",
    ]
    if r.available_ok is not None:
        lines.append(
            f"Request <= Available : {fmt_vec(r.request)} <= {fmt_vec(b.available)} -> {r.available_ok}"
        )
    if r.tentative_available is not None:
        lines += [
            f"Tentative Available  : {fmt_vec(r.tentative_available)}",
            f"Tentative Allocation : {fmt_vec(r.tentative_allocation)}",
            f"Tentative Need       : {fmt_vec(r.tentative_need)}",
        ]
    if r.safety is not None:
        lines += ["", "Safety check on tentative state:", format_safety(b, r.safety)]
    lines += ["", f"Decision: {r.decision} - {r.reason}"]
    return "\n".join(lines)
