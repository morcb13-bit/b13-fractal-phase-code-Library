# B13 Fractal Phase Library (BASE = 3120)

Integer-first fractal phase representation using radix-3120.

This library demonstrates a **machine-oriented phase representation**
where a circle is discretized into BASE=3120 and extended fractally
using radix digits.

The core philosophy is simple:

> Phase is stored and manipulated using integer addision only.  
> Trigonometric evaluation is secondary.

---

## ✨ Why BASE = 3120?

BASE=3120 has several useful properties:

- Divisible by 10 (useful for sector construction)
- Less than 2^12 → each digit fits in **12 bits**
- Enables compact packing:
  - 5 digits fit in a single 64-bit word (12×5 = 60 bits)

---

## 🧠 Core Concept

A phase is represented as radix-3120 digits:
