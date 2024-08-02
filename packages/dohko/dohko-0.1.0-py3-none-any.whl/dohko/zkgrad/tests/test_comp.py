from dohko.zkgrad.zkgrad.arithmetics.fp16 import FP16x16
from dohko.zkgrad.zkgrad.arithmetics.comp import (
    max,
    min,
    bitwise_and,
    bitwise_xor,
    bitwise_or,
)


def test_max():
    a = FP16x16.new_unscaled(1)
    b = FP16x16.new_unscaled(0)
    c = FP16x16.new_unscaled(1, True)

    assert max(a, a) == a
    assert max(a, b) == a
    assert max(a, c) == a
    assert max(b, a) == a
    assert max(b, b) == b
    assert max(b, c) == b
    assert max(c, a) == a
    assert max(c, b) == b
    assert max(c, c) == c


def test_min():
    a = FP16x16.new_unscaled(1)
    b = FP16x16.new_unscaled(0)
    c = FP16x16.new_unscaled(1, True)

    assert min(a, a) == a
    assert min(a, b) == b
    assert min(a, c) == c
    assert min(b, a) == b
    assert min(b, b) == b
    assert min(b, c) == c
    assert min(c, a) == c
    assert min(c, b) == c
    assert min(c, c) == c


def test_bitwise_and():
    a = FP16x16(225280)
    b = FP16x16(4160843776, True)
    c = FP16x16(94208)

    assert bitwise_and(a, b) == c


def test_bitwise_xor():
    a = FP16x16(225280)
    b = FP16x16(4160843776, True)
    c = FP16x16(4160880640, True)

    assert bitwise_xor(a, b) == c


def test_bitwise_or():
    a = FP16x16(225280)
    b = FP16x16(4160843776, True)
    c = FP16x16(4160974848, True)

    assert bitwise_or(a, b) == c
