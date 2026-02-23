from b13phase.phase_digits import digits_from_int, digits_to_int, digits_add, digits_inc
from b13phase.constants import BASE

def test_roundtrip():
    n = 6
    for x in [0, 1, 123, BASE-1, BASE, BASE+1, 123456789]:
        d = digits_from_int(x, n)
        assert digits_to_int(d) == x

def test_add_simple():
    n = 4
    a = digits_from_int(1000, n)
    b = digits_from_int(2500, n)
    s, carry = digits_add(a, b)
    assert digits_to_int(s) == 3500
    assert carry == 0

def test_add_with_carry():
    n = 2
    a = [0, BASE-1]
    b = [0, 1]
    s, carry = digits_add(a, b)
    assert s == [1, 0]
    assert carry == 0

def test_inc():
    d = [0, BASE-1]
    out, carry = digits_inc(d, 1)
    assert out == [1, 0]
    assert carry == 0
