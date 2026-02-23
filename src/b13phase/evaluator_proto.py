"""
evaluator_proto.py
==================

Prototype evaluator for multi-digit phase -> (cos, sin) integer vector.

Important:
- The phase representation (digits) is exact.
- This evaluator is *experimental* and intentionally labeled "proto".

What it does:
- Uses Level0 table from digit-0 as a base vector.
- Applies lower digits as small rotation-like corrections.

This is useful for demonstrations and pipeline shaping, but not guaranteed to be
a mathematically exact refinement of angle.

If/when you want a "production evaluator", replace this module.
"""

from __future__ import annotations
from typing import List, Tuple
from .constants import BASE
from .level0_table import COS_TABLE, SIN_TABLE


def fractal_cos_sin_proto(digits: List[int]) -> Tuple[int, int]:
    """
    digits: MSD->LSD radix-BASE digits (length >= 1)
    returns: (cx, cy) scaled roughly by BASE
    """
    if len(digits) < 1:
        raise ValueError("digits must have length >= 1")
    for v in digits:
        if v < 0 or v >= BASE:
            raise ValueError("digit out of range")

    coarse = digits[0]
    cx = COS_TABLE[coarse]
    cy = SIN_TABLE[coarse]

    # Rotation-like corrections (prototype)
    for l in range(1, len(digits)):
        fine = digits[l]
        scale = BASE ** l
        new_cx = (cx * scale - cy * fine) // scale
        new_cy = (cy * scale + cx * fine) // scale
        cx, cy = new_cx, new_cy

    return cx, cy
