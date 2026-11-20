"""
banker_logic.py  -  Pure logic for the Banker's Algorithm (no GUI code here).

Formulas used (same as the Problem 1 solution document):
    Need      = Max - Allocation
    Available = Total - (sum of all Allocation)
    A process can finish if  Need <= Work
    When it finishes:        Work = Work + Allocation
"""

SAMPLE = {
    "total": [9, 5, 7],
    "alloc": [[1, 0, 1], [2, 1, 0], [3, 0, 2], [0, 2, 1]],
    "maxm":  [[4, 2, 2], [3, 2, 2], [6, 1, 3], [2, 3, 2]],
}


def fmt(vec):
    """[3, 2, 3] -> '(3, 2, 3)'"""
    return "(" + ", ".join(str(v) for v in vec) + ")"


def leq(a, b):
    """True if every value of a is <= the matching value of b."""
    return all(x <= y for x, y in zip(a, b))


def compute_need(alloc, maxm):
    return [[m - a for m, a in zip(max_row, alloc_row)]
            for max_row, alloc_row in zip(maxm, alloc)]


def compute_available(total, alloc):
    used = [sum(col) for col in zip(*alloc)]
    return [t - u for t, u in zip(total, used)]


def safety_check(alloc, need, available):
    """
    Run the safety algorithm.

    Returns a dict:
        safe        -> True / False
        sequence    -> list of process indexes (the safe sequence)
        steps       -> one dict per process that finished:
                       index, need, alloc, work_before, work_after
        stuck       -> process indexes that could never finish
        final_work  -> Work vector at the end
    """
    n = len(alloc)
    work = list(available)
    finish = [False] * n
    sequence, steps = [], []

    progress = True
    while progress:
        progress = False
        for i in range(n):
            if not finish[i] and leq(need[i], work):
                before = work[:]
                work = [w + a for w, a in zip(work, alloc[i])]
                finish[i] = True
                sequence.append(i)
                progress = True
                steps.append({
                    "index": i,
                    "need": need[i][:],
                    "alloc": alloc[i][:],
                    "work_before": before,
                    "work_after": work[:],
                })

    stuck = [i for i in range(n) if not finish[i]]
    return {
        "safe": not stuck,
        "sequence": sequence,
        "steps": steps,
        "stuck": stuck,
        "final_work": work,
    }


def request_resource(pid, request, total, alloc, maxm):
    """
    Resource-Request algorithm.

    Returns a dict: granted (bool), reason (str), result (safety result or None),
    and new_alloc (the allocation matrix if the request is granted, else None).
    """
    need = compute_need(alloc, maxm)
    available = compute_available(total, alloc)

    if not leq(request, need[pid]):
        return {"granted": False, "result": None, "new_alloc": None,
                "reason": f"Denied: P{pid} asked for more than its remaining Need "
                          f"{fmt(need[pid])}. It exceeded its maximum claim."}

    if not leq(request, available):
        return {"granted": False, "result": None, "new_alloc": None,
                "reason": f"P{pid} must WAIT: the request {fmt(request)} is more than "
                          f"the Available resources {fmt(available)}."}

    # Pretend to give the resources, then run the safety check.
    new_alloc = [row[:] for row in alloc]
    new_alloc[pid] = [a + r for a, r in zip(new_alloc[pid], request)]
    new_need = compute_need(new_alloc, maxm)
    new_avail = compute_available(total, new_alloc)
    result = safety_check(new_alloc, new_need, new_avail)

    if result["safe"]:
        seq = " -> ".join(f"P{i}" for i in result["sequence"])
        return {"granted": True, "result": result, "new_alloc": new_alloc,
                "reason": f"GRANTED: the system stays SAFE.\nSafe sequence: {seq}"}

    return {"granted": False, "result": result, "new_alloc": None,
            "reason": "Denied: granting this request would leave the system in an "
                      "UNSAFE state, so P%d must wait." % pid}


if __name__ == "__main__":
    need = compute_need(SAMPLE["alloc"], SAMPLE["maxm"])
    avail = compute_available(SAMPLE["total"], SAMPLE["alloc"])
    res = safety_check(SAMPLE["alloc"], need, avail)
    print("Need     :", need)
    print("Available:", avail)
    print("Safe?    :", res["safe"], "->", " -> ".join(f"P{i}" for i in res["sequence"]))
