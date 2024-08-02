from dohko.zkgrad.zkgrad.arithmetics.fp16 import FP16x16
from dohko.zkgrad.zkgrad.arithmetics.base import ONE, HALF, TWO
from dohko.zkgrad.tests.utils import assert_precise


def test_cosh():
    a = FP16x16(TWO, False)
    assert_precise(a.cosh(), 246550, "invalid two")  # 3.5954653836066

    a = FP16x16(ONE, False)
    assert_precise(a.cosh(), 101127, "invalid one")  # 1.42428174592510

    a = FP16x16.ZERO()
    assert_precise(a.cosh(), ONE, "invalid zero")

    a = FP16x16(ONE, True)
    assert_precise(a.cosh(), 101127, "invalid neg one")  # 1.42428174592510

    a = FP16x16(TWO, True)
    assert_precise(a.cosh(), 246568, "invalid neg two")  # 3.5954653836066


def test_sinh():
    a = FP16x16(TWO, False)
    assert_precise(a.sinh(), 237681, "invalid two")  # 3.48973469357602

    a = FP16x16(ONE, False)
    assert_precise(a.sinh(), 77018, "invalid one")  # 1.13687593250230

    a = FP16x16.ZERO()
    assert_precise(a.sinh(), 0, "invalid zero")

    a = FP16x16(ONE, True)
    assert_precise(a.sinh(), -77018, "invalid neg one")  # -1.13687593250230

    a = FP16x16(TWO, True)
    assert_precise(a.sinh(), -237699, "invalid neg two")  # -3.48973469357602


def test_tanh():
    a = FP16x16(TWO, False)
    assert_precise(a.tanh(), 63179, "invalid two")  # 0.75314654693321

    a = FP16x16(ONE, False)
    assert_precise(a.tanh(), 49912, "invalid one")  # 0.59499543433175

    a = FP16x16.ZERO()
    assert_precise(a.tanh(), 0, "invalid zero")

    a = FP16x16(ONE, True)
    assert_precise(a.tanh(), -49912, "invalid neg one")  # -0.59499543433175

    a = FP16x16(TWO, True)
    assert_precise(a.tanh(), -63179, "invalid neg two")  # 0.75314654693321


def test_acosh():
    a = FP16x16(246559, False)  # 3.5954653836066
    assert_precise(a.acosh(), 131072, "invalid two")

    a = FP16x16(101127, False)  # 1.42428174592510
    assert_precise(a.acosh(), ONE, "invalid one")

    a = FP16x16(ONE, False)  # 1
    assert_precise(a.acosh(), 0, "invalid zero")


def test_asinh():
    a = FP16x16(237690, False)  # 3.48973469357602
    assert_precise(a.asinh(), 131072, "invalid two")

    a = FP16x16(77018, False)  # 1.13687593250230
    assert_precise(a.asinh(), ONE, "invalid one")

    a = FP16x16.ZERO()
    assert_precise(a.asinh(), 0, "invalid zero")

    a = FP16x16(77018, True)  # -1.13687593250230
    assert_precise(a.asinh(), -ONE, "invalid neg one")

    a = FP16x16(237690, True)  # -3.48973469357602
    assert_precise(a.asinh(), -131017, "invalid neg two")


def test_atanh():
    a = FP16x16(58982, False)  # 0.9
    assert_precise(a.atanh(), 96483, "invalid 0.9")  # 1.36892147623689

    a = FP16x16(HALF, False)  # 0.5
    assert_precise(a.atanh(), 35999, "invalid half")  # 0.42914542526098

    a = FP16x16.ZERO()
    assert_precise(a.atanh(), 0, "invalid zero")

    a = FP16x16(HALF, True)  # -0.5
    assert_precise(a.atanh(), -35999, "invalid neg half")  # -0.42914542526098

    a = FP16x16(58982, True)  # -0.9
    assert_precise(a.atanh(), -96483, "invalid -0.9")  # -1.36892147623689
