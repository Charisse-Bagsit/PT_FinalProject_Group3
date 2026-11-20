from typing import List, Sequence

Vector = List[int]
Matrix = List[Vector]


def vec_add(a: Sequence[int], b: Sequence[int]):
    # Component-wise a + b.
    return [x + y for x, y in zip(a, b)]


def vec_sub(a: Sequence[int], b: Sequence[int]):
    # Component-wise a - b.
    return [x - y for x, y in zip(a, b)]


def vec_leq(a: Sequence[int], b: Sequence[int]):
    # Component-wise a <= b (every resource must pass).
    return all(x <= y for x, y in zip(a, b))


def fmt_vec(v: Sequence[int]):
    # (3, 3, 2) style text.
    return "(" + ", ".join(str(x) for x in v) + ")"
