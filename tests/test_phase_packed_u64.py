from b13phase.phase_packed_u64 import pack_u64_digits, unpack_u64_digits, add_u64_packed, U64_DIGITS
from b13phase.constants import BASE

def test_pack_unpack():
    d = [1, 2, 3, 4, 5]
    x = pack_u64_digits(d)
    assert unpack_u64_digits(x) == d

def test_add_no_overflow():
    a = pack_u64_digits([0, 0, 0, 0, 3000])
    b = pack_u64_digits([0, 0, 0, 0, 500])
    s, carry = add_u64_packed(a, b)
    assert unpack_u64_digits(s) == [0, 0, 0, 1, 380]  # 3500 = 1*3120 + 380
    assert carry == 0

def test_add_overflow_out_of_5_digits():
    # Maximum digits all BASE-1 plus 1 -> overflow carry out
    a = pack_u64_digits([BASE-1]*U64_DIGITS)
    b = pack_u64_digits([0, 0, 0, 0, 1])
    s, carry = add_u64_packed(a, b)
    assert unpack_u64_digits(s) == [0]*U64_DIGITS
    assert carry == 1
