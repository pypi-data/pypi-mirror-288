from dohko.zkgrad.zkgrad.arithmetics.fp16 import FP16x16


def max(a: FP16x16, b: FP16x16) -> FP16x16:
    return a if a >= b else b


def min(a: FP16x16, b: FP16x16) -> FP16x16:
    return a if a <= b else b


def xor(a: FP16x16, b: FP16x16) -> bool:
    zero = FP16x16.ZERO()
    return (a == zero or b == zero) and a != b


def or_(a: FP16x16, b: FP16x16) -> bool:
    zero = FP16x16.ZERO()
    return not (a == zero and b == zero)


def and_(a: FP16x16, b: FP16x16) -> bool:
    zero = FP16x16.ZERO()
    return not (a == zero or b == zero)


def where(a: FP16x16, b: FP16x16, c: FP16x16) -> FP16x16:
    zero = FP16x16.ZERO()
    return c if a == zero else b


def bitwise_and(a: FP16x16, b: FP16x16) -> FP16x16:
    return FP16x16(a._mag & b._mag, a._sign & b._sign)


def bitwise_xor(a: FP16x16, b: FP16x16) -> FP16x16:
    return FP16x16(a._mag ^ b._mag, a._sign ^ b._sign)


def bitwise_or(a: FP16x16, b: FP16x16) -> FP16x16:
    return FP16x16(a._mag | b._mag, a._sign | b._sign)
