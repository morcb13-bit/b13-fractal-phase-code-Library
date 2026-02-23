"""
demo.py
=======

A small CLI demo:
- prints resolution table
- shows digit decomposition and packed-u64 usage
- shows evaluator_proto outputs at a few canonical points

Run:
    python -m b13phase.demo
"""

from __future__ import annotations
from .constants import BASE, INT64_MAX
from .phase_digits import digits_from_int, digits_to_int, digits_add
from .phase_packed_u64 import U64_DIGITS, pack_u64_digits, unpack_u64_digits, add_u64_packed
from .evaluator_proto import fractal_cos_sin_proto


def total_subdivisions(n_digits: int) -> int:
    return BASE ** n_digits


def show_resolution(max_digits: int = 8) -> None:
    print("=== Resolution table (BASE=3120) ===")
    print(f"{'digits':>6} {'BASE^digits':>28} {'int64':>6} {'deg/step':>14}")
    print("-" * 64)
    for n in range(1, max_digits + 1):
        total = total_subdivisions(n)
        ok = total <= INT64_MAX
        deg = 360.0 / total
        print(f"{n:6d} {total:28,d} {('OK' if ok else 'NO'):>6} {deg:14.2e}")
        if not ok:
            break
    print()


def demo_digits() -> None:
    print("=== Digit-array phase demo ===")
    n = 6  # arbitrary: can be larger (practically unbounded)
    total = total_subdivisions(n)
    print(f"digits={n}, total indices=BASE^digits={total:,}")

    idx = 123456789
    d = digits_from_int(idx, n)
    back = digits_to_int(d)
    print("idx:", idx)
    print("digits(MSD->LSD):", d)
    print("roundtrip:", back, "(ok)" if back == idx else "(mismatch)")
    print()

    a = digits_from_int(1000, n)
    b = digits_from_int(2500, n)
    s, carry = digits_add(a, b)
    print("1000 + 2500 in radix-3120 =>", digits_to_int(s), "carry:", carry)
    print()


def demo_packed_u64() -> None:
    print("=== Packed-u64 phase demo (5 digits) ===")
    d = [1, 2, 3, 4, 5]
    x = pack_u64_digits(d)
    d2 = unpack_u64_digits(x)
    print("digits:", d)
    print("packed:", x)
    print("unpacked:", d2)
    print()

    a = pack_u64_digits([0, 0, 0, 0, 3000])
    b = pack_u64_digits([0, 0, 0, 0, 500])
    s, carry = add_u64_packed(a, b)
    print("3000 + 500 (LSD) =>", unpack_u64_digits(s), "carry:", carry)
    print()


def demo_eval() -> None:
    print("=== Prototype evaluator demo ===")
    # Use digits length 3 for demo
    n = 3
    total = total_subdivisions(n)

    checkpoints = [
        (0, "0°"),
        (total // 4, "90°"),
        (total // 2, "180°"),
        (total * 3 // 4, "270°"),
    ]

    print(f"digits={n}, total={total:,}, deg/step={360.0/total:.2e}")
    print(f"{'angle':>6} {'idx':>18} {'digits':>22} {'cos':>8} {'sin':>8} {'|v|^2/BASE^2':>16}")
    print("-" * 90)

    ideal_sq = BASE * BASE
    for idx, label in checkpoints:
        d = digits_from_int(idx, n)
        cx, cy = fractal_cos_sin_proto(d)
        ratio = (cx * cx + cy * cy) / ideal_sq
        print(f"{label:>6} {idx:18,d} {str(d):>22} {cx:8d} {cy:8d} {ratio:16.6f}")
    print()


def main() -> None:
    show_resolution()
    demo_digits()
    demo_packed_u64()
    demo_eval()


if __name__ == "__main__":
    main()
