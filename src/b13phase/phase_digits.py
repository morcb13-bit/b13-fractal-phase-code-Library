"""
phase_digits.py
===============

Exact radix-BASE (BASE=3120) phase representation using a digit array.

Representation
--------------
A phase is represented as a list of digits:
    d = [d0, d1, ..., d(n-1)]  (MSD -> LSD)

Each digit di is an integer in [0, BASE).

This is the "infinite fractal" option:
- you can increase n (digits) as far as you like
- operations are exact integer + carry

This is the most "B13 addision-like" core.
"""

from __future__ import annotations
from typing import List, Tuple
from .constants import BASE


def digits_zero(n: int) -> List[int]:
    """Create a zero phase with n digits (MSD->LSD)."""
    if n <= 0:
        raise ValueError("n must be >= 1")
    return [0] * n


def digits_from_int(x: int, n: int) -> List[int]:
    """
    Convert non-negative integer x into radix-BASE digits (MSD->LSD) of length n.

    Requires: 0 <= x < BASE^n
    """
    if n <= 0:
        raise ValueError("n must be >= 1")
    if x < 0:
        raise ValueError("x must be >= 0")

    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = x % BASE
        x //= BASE
    if x != 0:
        raise ValueError("x does not fit in n digits")
    return out


def digits_to_int(d: List[int]) -> int:
    """Convert radix-BASE digits (MSD->LSD) into an integer."""
    x = 0
    for v in d:
        if v < 0 or v >= BASE:
            raise ValueError("digit out of range")
        x = x * BASE + v
    return x


def digits_add(a: List[int], b: List[int]) -> Tuple[List[int], int]:
    """
    Add two digit arrays (same length), radix-BASE, exact with carry.

    Returns (sum_digits, carry_out) where carry_out is 0 or 1.
    """
    if len(a) != len(b):
        raise ValueError("digit arrays must have the same length")
    n = len(a)
    out = [0] * n

    carry = 0
    for i in range(n - 1, -1, -1):
        ai, bi = a[i], b[i]
        if not (0 <= ai < BASE and 0 <= bi < BASE):
            raise ValueError("digit out of range")

        s = ai + bi + carry
        if s >= BASE:
            s -= BASE
            carry = 1
        else:
            carry = 0
        out[i] = s

    return out, carry


def digits_inc(d: List[int], step: int = 1) -> Tuple[List[int], int]:
    """
    Increment digit array by a small integer step (typically step < BASE).

    Returns (new_digits, carry_out).
    """
    if step < 0:
        raise ValueError("step must be >= 0")
    if step >= BASE:
        # You *can* support this with repeated carry, but keep it simple for public API:
        raise ValueError("step must be < BASE for this helper")

    out = d[:]  # copy
    n = len(out)

    carry = step
    for i in range(n - 1, -1, -1):
        if carry == 0:
            break
        v = out[i]
        if not (0 <= v < BASE):
            raise ValueError("digit out of range")

        v += carry
        if v >= BASE:
            out[i] = v - BASE
            carry = 1
        else:
            out[i] = v
            carry = 0

    return out, (1 if carry else 0)


def digits_phase(idx: int, n: int) -> List[int]:
    """
    Alias for digits_from_int: interpret idx in [0, BASE^n) as phase digits (MSD->LSD).
    """
    return digits_from_int(idx, n)
