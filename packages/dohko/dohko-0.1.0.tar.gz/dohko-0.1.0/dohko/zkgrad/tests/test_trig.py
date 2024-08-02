import pytest
from dohko.zkgrad.zkgrad.arithmetics.fp16 import FP16x16
from dohko.zkgrad.zkgrad.arithmetics.base import ONE, HALF_PI, PI
from dohko.zkgrad.tests.utils import assert_precise, assert_relative


def test_atan():
    a = FP16x16(2 * ONE, False)
    assert_relative(a.atan(), 72558, "invalid two")

    a = FP16x16.ONE()
    assert_relative(a.atan(), 51472, "invalid one")

    a = FP16x16(ONE // 2, False)
    assert_relative(a.atan(), 30386, "invalid half")

    a = FP16x16.ZERO()
    assert a.atan()._mag == 0, "invalid zero"

    a = FP16x16(ONE // 2, True)
    assert_relative(a.atan(), -30386, "invalid neg half")

    a = FP16x16(ONE, True)
    assert_relative(a.atan(), -51472, "invalid neg one")

    a = FP16x16(2 * ONE, True)
    assert_relative(a.atan(), -72558, "invalid neg two")


def test_atan_fast():
    error_margin = 84  # 1e-5

    a = FP16x16(2 * ONE, False)
    assert_relative(a.atan_fast(), 72558, "invalid two", error_margin)

    a = FP16x16.ONE()
    assert_relative(a.atan_fast(), 51472, "invalid one", error_margin)

    a = FP16x16(ONE // 2, False)
    assert_relative(a.atan_fast(), 30386, "invalid half", error_margin)

    a = FP16x16.ZERO()
    assert a.atan_fast()._mag == 0, "invalid zero"

    a = FP16x16(ONE // 2, True)
    assert_relative(a.atan_fast(), -30386, "invalid neg half", error_margin)

    a = FP16x16(ONE, True)
    assert_relative(a.atan_fast(), -51472, "invalid neg one", error_margin)

    a = FP16x16(2 * ONE, True)
    assert_relative(a.atan_fast(), -72558, "invalid neg two", error_margin)


def test_asin():
    error = 84  # 1e-5

    a = FP16x16.ONE()
    assert_relative(a.asin(), HALF_PI, "invalid one")

    a = FP16x16(ONE // 2, False)
    assert_relative(a.asin(), 34315, "invalid half", error)

    a = FP16x16.ZERO()
    assert_precise(a.asin(), 0, "invalid zero")

    a = FP16x16(ONE // 2, True)
    assert_relative(a.asin(), -34315, "invalid neg half", error)

    a = FP16x16(ONE, True)
    assert_relative(a.asin(), -HALF_PI, "invalid neg one")


def test_asin_fail():
    a = FP16x16(2 * ONE, False)
    with pytest.raises(
        Exception
    ):  # Replace Exception with the specific exception if known
        a.asin()


def test_acos():
    error = 84  # 1e-5

    a = FP16x16.ONE()
    assert a.acos()._mag == 0, "invalid one"

    a = FP16x16(ONE // 2, False)
    assert_relative(a.acos(), 68629, "invalid half", error)

    a = FP16x16.ZERO()
    assert_relative(a.acos(), HALF_PI, "invalid zero")

    a = FP16x16(ONE // 2, True)
    assert_relative(a.acos(), 137258, "invalid neg half", error)

    a = FP16x16(ONE, True)
    assert_relative(a.acos(), PI, "invalid neg one")


# The tests for acos_fast
def test_acos_fast():
    error = 84  # 1e-5

    a = FP16x16.ONE()
    assert a.acos_fast()._mag == 0, "invalid one"

    a = FP16x16(ONE // 2, False)
    assert_relative(a.acos_fast(), 68629, "invalid half", error)

    a = FP16x16.ZERO()
    assert_relative(a.acos_fast(), HALF_PI, "invalid zero")

    a = FP16x16(ONE // 2, True)
    assert_relative(a.acos_fast(), 137258, "invalid neg half", error)

    a = FP16x16(ONE, True)
    assert_relative(a.acos_fast(), PI, "invalid neg one")


# The test that should fail if the input is outside the domain [-1, 1]
def test_acos_fail():
    a = FP16x16(2 * ONE, True)
    with pytest.raises(
        Exception
    ):  # Replace Exception with the specific exception if known
        a.acos()


def test_cos():
    a = FP16x16(HALF_PI, False)
    assert a.cos()._mag == 0, "invalid half pi"

    a = FP16x16(HALF_PI // 2, False)
    assert_relative(a.cos(), 46341, "invalid quarter pi")

    a = FP16x16(PI, False)
    assert_relative(a.cos(), -ONE, "invalid pi")

    a = FP16x16(HALF_PI, True)
    assert_precise(a.cos(), 0, "invalid neg half pi")

    a = FP16x16.new_unscaled(17, False)
    assert_relative(a.cos(), -18033, "invalid 17")

    a = FP16x16.new_unscaled(17, True)
    assert_relative(a.cos(), -18033, "invalid -17")


def test_cos_fast():
    error = 84  # 1e-5

    a = FP16x16(HALF_PI, False)
    assert a.cos_fast()._mag == 0, "invalid half pi"

    a = FP16x16(HALF_PI // 2, False)
    assert_precise(a.cos_fast(), 46341, "invalid quarter pi", error)

    a = FP16x16(PI, False)
    assert_precise(a.cos_fast(), -ONE, "invalid pi", error)

    a = FP16x16(HALF_PI, True)
    assert_precise(a.cos_fast(), 0, "invalid neg half pi", error)

    a = FP16x16.new_unscaled(17, False)
    assert_precise(a.cos_fast(), -18033, "invalid 17", error)


def test_sin():
    a = FP16x16(HALF_PI, False)
    assert_precise(a.sin()._mag, ONE, "invalid half pi")

    a = FP16x16(HALF_PI // 2, False)
    assert_precise(a.sin(), 46341, "invalid quarter pi")

    a = FP16x16(PI, False)
    assert a.sin()._mag == 0, "invalid pi"

    a = FP16x16(HALF_PI, True)
    assert_precise(a.sin(), -ONE, "invalid neg half pi")

    a = FP16x16.new_unscaled(17, False)
    assert_precise(a.sin(), -63006, "invalid 17")

    a = FP16x16.new_unscaled(17, True)
    assert_precise(a.sin(), 63006, "invalid -17")


def test_sin_fast():
    error = 84  # 1e-5

    a = FP16x16(HALF_PI, False)
    assert_precise(a.sin_fast(), ONE, "invalid half pi", error)

    a = FP16x16(HALF_PI // 2, False)
    assert_precise(a.sin_fast(), 46341, "invalid quarter pi", error)

    a = FP16x16(PI, False)
    assert a.sin_fast()._mag == 0, "invalid pi"

    a = FP16x16(HALF_PI, True)
    assert_precise(a.sin_fast(), -ONE, "invalid neg half pi", error)

    a = FP16x16.new_unscaled(17, False)
    assert_precise(a.sin_fast(), -63006, "invalid -17", error)

    a = FP16x16.new_unscaled(17, True)
    assert_precise(a.sin_fast(), 63006, "invalid 17", error)


def test_tan():
    a = FP16x16(HALF_PI // 2, False)
    assert_precise(a.tan()._mag, ONE, "invalid quarter pi")

    a = FP16x16(PI, False)
    assert_precise(a.tan()._mag, 0, "invalid pi")

    a = FP16x16.new_unscaled(17, False)
    assert_precise(a.tan()._mag, 228990, "invalid 17")

    a = FP16x16.new_unscaled(17, True)
    assert_precise(a.tan(), -228952, "invalid -17")
