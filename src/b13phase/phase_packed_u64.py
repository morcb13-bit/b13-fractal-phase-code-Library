"""
phase_packed_u64.py
===================

Exact radix-BASE (BASE=3120) phase representation for the "single-machine-word" case.

Since BASE=3120 < 2^12, each digit fits in 12 bits.
Therefore we can pack 5 digits into uint64 (12*5=60 bits).

This gives a compact, fast representation close to "machine language limits":
- exactly 5 radix digits in one 64-bit word
- exact digit-wise addition with carry (radix-BASE)
"""

from __future__ import annotations
from typing import List, Tuple
from .constants import BASE

BITS_PER_DIGIT: int = 12
MASK: int = (1 << BITS_PER_DIGIT) - 1

# 12*5=60 bits used, fits in uint64
U64_DIGITS: int = 5


def pack_u64_digits(d: List[int]) -> int:
    """Pack 5 digits (MSD->LSD) into a single integer (int used as uint64 carrier)."""
    if len(d) != U64_DIGITS:
        raise ValueError(f"expected {U64_DIGITS} digits")
    x = 0
    for v in d:
        if v < 0 or v >= BASE:
            raise ValueError("digit out of range")
        x = (x << BITS_PER_DIGIT) | v
    return x


def unpack_u64_digits(x: int) -> List[int]:
    """Unpack packed integer into 5 digits (MSD->LSD)."""
    d = [0] * U64_DIGITS
    for i in range(U64_DIGITS - 1, -1, -1):
        d[i] = x & MASK
        x >>= BITS_PER_DIGIT
    # digits are 0..4095 by mask; validate BASE range
    for v in d:
        if v >= BASE:
            # This signals packed value is invalid for BASE=3120 digit range
            raise ValueError("packed digit exceeds BASE-1; invalid packed value")
    return d


def add_u64_packed(a: int, b: int) -> Tuple[int, int]:
    """
    Add two packed u64 phases in radix-BASE, exact.

    Returns (packed_sum, carry_out).
    carry_out is 0 or 1 (overflow beyond 5 digits).
    """
    da = unpack_u64_digits(a)
    db = unpack_u64_digits(b)

    out = [0] * U64_DIGITS
    carry = 0
    for i in range(U64_DIGITS - 1, -1, -1):
        s = da[i] + db[i] + carry
        if s >= BASE:
            s -= BASE
            carry = 1
        else:
            carry = 0
        out[i] = s

    return pack_u64_digits(out), carry
