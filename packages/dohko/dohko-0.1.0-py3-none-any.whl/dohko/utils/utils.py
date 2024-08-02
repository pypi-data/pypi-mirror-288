from typing import List, Iterator, Union, Tuple
from sympy import FiniteField, Symbol
from sympy.polys.domains.modularinteger import ModularInteger
from dohko.polynomials.poly import (
    LinearPoly,
    QuadraticPoly,
)


def my_resize(
    vec: List[FiniteField], sz: int, domain: FiniteField
) -> List[FiniteField]:
    return vec + [domain(0)] * (sz - len(vec)) if len(vec) < sz else vec


def my_resize_pol(
    vec: List[FiniteField], sz: int, polynom: Union[LinearPoly, QuadraticPoly]
) -> List[FiniteField]:
    return vec + [polynom] * (sz - len(vec)) if len(vec) < sz else vec


def init_half_table(
    beta_f: List[FiniteField],
    beta_s: List[FiniteField],
    r: Iterator[FiniteField],
    init: FiniteField,
    first_half: int,
    second_half: int,
    domain: FiniteField,
) -> tuple[List[FiniteField], List[FiniteField]]:
    beta_f[0] = init
    beta_s[0] = domain(1)

    for i in range(first_half):
        for j in range(1 << i):
            tmp = beta_f[j] * r[i]
            beta_f[j | (1 << i)] = tmp
            beta_f[j] = beta_f[j] - tmp

    for i in range(second_half):
        for j in range(1 << i):
            tmp = beta_s[j] * r[i + first_half]
            beta_s[j | (1 << i)] = tmp
            beta_s[j] = beta_s[j] - tmp
    return beta_f, beta_s


def init_beta_table_base(
    beta_g: List[FiniteField],
    g_length: int,
    r: Iterator[FiniteField],
    init: FiniteField,
    domain: FiniteField,
) -> List[FiniteField]:
    if g_length == -1:
        return beta_g
    assert len(beta_g) >= 1 << g_length, "beta_g should be at least 2^g_length in size"
    first_half = g_length >> 1
    second_half = g_length - first_half
    beta_f: List[FiniteField] = [domain(0)] * (1 << first_half)
    beta_s: List[FiniteField] = [domain(0)] * (1 << second_half)
    mask_fhalf = (1 << first_half) - 1
    if init != domain(0):
        beta_f, beta_s = init_half_table(
            beta_f, beta_s, r, init, first_half, second_half, domain
        )
        for i in range(1 << g_length):
            beta_g[i] = beta_f[i & mask_fhalf] * beta_s[i >> first_half]
    else:
        for i in range(1 << g_length):
            beta_g[i] = domain(0)
    return beta_g


def init_beta_table_alpha(
    beta_g: List[FiniteField],
    g_length: int,
    r_0: Iterator[FiniteField],
    r_1: Iterator[FiniteField],
    alpha: FiniteField,
    beta: FiniteField,
    domain: FiniteField,
) -> List[FiniteField]:
    first_half = g_length >> 1
    second_half = g_length - first_half
    beta_f: List[FiniteField] = [domain(0)] * (1 << first_half)
    beta_s: List[FiniteField] = [domain(0)] * (1 << second_half)
    mask_fhalf = (1 << first_half) - 1
    assert len(beta_g) >= 1 << g_length, "beta_g should be at least 2^g_length in size"
    if beta != domain(0):
        beta_f, beta_s = init_half_table(
            beta_f, beta_s, r_1, beta, first_half, second_half, domain
        )
        for i in range(1 << g_length):
            beta_g[i] = beta_f[i & mask_fhalf] * beta_s[i >> first_half]
    else:
        for i in range(1 << g_length):
            beta_g[i] = domain(0)

    if alpha == domain(0):
        return beta_g
    beta_f, beta_s = init_half_table(
        beta_f, beta_s, r_0, alpha, first_half, second_half, domain
    )
    for i in range(1 << g_length):
        beta_g[i] += beta_f[i & mask_fhalf] * beta_s[i >> first_half]
    return beta_g


def init_beta_table(
    beta_g: List[FiniteField],
    g_length: int,
    r_0: Iterator[FiniteField],
    r_1: Iterator[FiniteField],
    domain: FiniteField,
    alpha: FiniteField = None,
    beta: FiniteField = None,
) -> List[FiniteField]:
    if alpha is None and beta is None:
        return init_beta_table_base(beta_g, g_length, r_0, r_1, domain)
    return init_beta_table_alpha(beta_g, g_length, r_0, r_1, alpha, beta, domain)


from sympy import symbols, prod, Poly


def integer_to_binary_tuple(index, dimension):
    """Convert an integer index to a binary tuple, appropriately ordered."""
    # Convert to binary and fill with zeros to match the dimension
    binary_str = bin(index)[2:].zfill(dimension)
    # Convert string to tuple of integers, reversed if MSB should lead
    return tuple(int(bit) for bit in reversed(binary_str))  # Reverse if needed


def construct_multilinear_polynomial(dimension, values):
    """Construct and return the multilinear polynomial from given values."""
    vars = symbols(f"x0:{dimension}")
    polynomial = 0
    for index, value in enumerate(values):
        vertex = integer_to_binary_tuple(index, dimension)
        terms = [vars[i] if bit else 1 - vars[i] for i, bit in enumerate(vertex)]
        polynomial += value * prod(terms)
    return polynomial, vars


def build_z_polynomial(num_vars: int, domain: FiniteField, vars: List[Symbol]) -> tuple:
    """Construct a polynomial for the Z function."""
    vars = symbols(f"x0:{num_vars}")
    Z = Poly(1, *vars, domain=domain)
    for x in vars:
        Z = Poly(Z * x * (1 - x), *vars, domain=domain)
    return Z, vars


def build_zr_polynomial(num_vars: int, R: QuadraticPoly, domain: FiniteField) -> tuple:
    """Construct a polynomial for the Z function."""
    vars = symbols(f"x{num_vars}:{2*num_vars}")
    x = vars[-1]
    Z = build_z_polynomial(num_vars, domain, vars)[0]
    r_poly = Poly(R.a * x**2 + R.b * x + R.c, *vars, domain=domain)
    return Z * r_poly, vars


def build_input_zk_mle(
    num_vars: int,
    evaluations: List[ModularInteger],
    R: QuadraticPoly,
    domain: FiniteField,
) -> tuple:
    """Construct the input for the ZK MLE algorithm."""
    mle_poly, vars = construct_multilinear_polynomial(num_vars, evaluations)
    zr_poly, zk_vars = build_zr_polynomial(num_vars, R, domain)
    zk_mle = Poly(mle_poly + zr_poly, domain=domain)
    zk_mle_evaluations = []
    for i in range(1 << num_vars):
        vertex = integer_to_binary_tuple(i, num_vars)
        subs = {}
        for j in range(num_vars):
            # {zk_mle.gens[j]: vertex[j] for j in range(2*num_vars)}
            subs[vars[j]] = vertex[j]
            subs[zk_vars[j]] = vertex[j]
        zk_mle_evaluations.append(zk_mle.subs(subs))
    return zk_mle, zk_mle_evaluations


def build_quotients_from_zk_mle(
    zk_mle_evaluations: List[ModularInteger],
    random_point: List[ModularInteger],
    num_vars: int,
    domain: FiniteField,
) -> List[Tuple[List[ModularInteger], Poly]]:
    """Build the quotients from the ZK MLE polynomial and its evaluations."""
    Q = []
    preR = zk_mle_evaluations
    for l in reversed(range(1, num_vars + 1)):
        Ql = [domain.zero] * 2 ** (l - 1)
        Rl = [domain.zero] * 2 ** (l - 1)
        for i in range(1 << l):
            bit_idx = integer_to_binary_tuple(i, l)
            b1 = bit_idx + 2 ** (l - 1)
            b0 = bit_idx
            Ql[bit_idx] = preR[b1] - preR[b0]
            Rl[bit_idx] = (
                preR[b0] * (1 - random_point[l - 1]) + preR[b1] * random_point[l - 1]
            )
        Ql_mle = construct_multilinear_polynomial(l, Ql)[0]
        quotient = (Ql, Ql_mle)
        preR = Rl
        Q.append(quotient)
    return Q
