# b13-fractal-phase-code-Library

# B13 Fractal Phase (3120-radix) — integer-first phase representation

This project demonstrates an **integer-first** representation of phase on a circle using
a radix-3120 ("BASE=3120") fractal index. The key design is to separate:

1) **Phase representation & arithmetic (exact integer)**
2) **Trigonometric evaluation (cos/sin)**
   - Level0 table (3120 samples) is deterministic integer table
   - Higher-digit refinement is currently *prototype / experimental*

## Why BASE=3120?
- BASE=3120 is divisible by 10 (handy for a 10-sector scaffold)
- BASE=3120 < 2^12, so each digit fits in 12 bits
- Enables:
  - "infinite digits" via digit arrays (exact add/carry)
  - compact uint64 packing for **5 digits** (12*5=60 bits)

## Modules
- `phase_digits.py`:
  - exact radix-3120 digit-array representation
  - exact add/sub/inc with carry
- `phase_packed_u64.py`:
  - exact radix-3120 arithmetic for **5 digits** packed into one uint64
- `level0_table.py`:
  - deterministic integer cos/sin table for digit-0 (3120 points)
- `evaluator_proto.py`:
  - prototype evaluator that applies small corrections from lower digits (experimental)
- `demo.py`:
  - prints resolution table, shows indexing examples, and a quick evaluator demo

## Correctness notes
- Exact:
  - digit decomposition, digit addition/carry, packing/unpacking, Level0 table generation
- Experimental:
  - multi-digit cos/sin refinement in `evaluator_proto.py`

## Quick start
```bash
python -m b13phase.demo
