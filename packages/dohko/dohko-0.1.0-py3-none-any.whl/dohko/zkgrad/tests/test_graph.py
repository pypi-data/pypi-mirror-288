from dohko.zkgrad.zkgrad.engine import Value
import numpy as np
from dohko.prover.prover import ZkProver
from dohko.commitments.mkzg.ecc import curve_order
from sympy import FiniteField
from dohko.zkgrad.zkgrad.utils.visualize import draw_dot

DOMAIN = FiniteField(curve_order)


def test_circuit_generation_value_numpy():
    A = np.array([[Value(1), Value(2)], [Value(2), Value(1)]])
    B = np.array([[Value(3), Value(4)]])
    C = A * B
    assert len(C) == 2
    circuit, _ = Value.compile_layered_circuit(C[0][0])
    assert ZkProver(circuit, DOMAIN).prove()


def test_circuit_generation_value_scalars():
    A = Value(1)
    B = Value(2)
    C = A + B
    for i in range(2):
        one = Value(i)
        C = C * one
    circuit, _, layers = Value.compile_layered_circuit(C, True)
    draw_dot(layers[0][0]).render("l", format="png", cleanup=True)
    assert ZkProver(circuit, DOMAIN).prove()


# @TODO: Fix this!
def test_new():
    A = Value(3)
    B = Value(2)
    C = A * B
    D = Value(1)
    E = C * D
    F = B * E
    draw_dot(F).render(
        "dohko/zkgrad/tests/assets/F_non_layered", format="png", cleanup=True
    )
    layers = Value.proprocess_circuit(F, True)
    draw_dot(layers[-1][0]).render(
        "dohko/zkgrad/tests/assets/non_layered", format="png", cleanup=True
    )
    # assert ZkProver(circuit, DOMAIN).prove()


def test_circuit_generation_value_scalars_non_layered_operations():
    A = Value(3)
    B = Value(2)
    C = A * B
    D = Value(1)
    E = C * D
    F = B * E
    draw_dot(F).render(
        "dohko/zkgrad/tests/assets/new_F_layered", format="png", cleanup=True
    )
    circuit, _, layers = Value.compile_layered_circuit(F, True)
    draw_dot(layers[0][0]).render(
        "dohko/zkgrad/tests/assets/new_layered", format="png", cleanup=True
    )
    assert ZkProver(circuit, DOMAIN).prove()


def test_circuit_generation_value_scalars_non_layered_operations_right():
    A = Value(3.77)
    B = Value(0.47)
    C = A + B
    D = A + B
    E = Value(0.05)
    F = D * E
    G = Value(0.99)
    H = F * G
    I = C * H
    draw_dot(I).render(
        "dohko/zkgrad/tests/assets/before_non_layered_right", format="png", cleanup=True
    )
    circuit, _, layers = Value.compile_layered_circuit(I, True)
    # layers = Value.proprocess_circuit(I, True)
    draw_dot(layers[0][0]).render(
        "dohko/zkgrad/tests/assets/non_layered_right", format="png", cleanup=True
    )
    assert ZkProver(circuit, DOMAIN).prove()


def test_circuit_generation_value_numpy_tensor():
    A = np.array(
        [
            [[Value(1), Value(2)], [Value(2), Value(1)]],
            [[Value(1), Value(2)], [Value(2), Value(1)]],
        ]
    )
    B = np.array(
        [
            [[Value(3), Value(4)], [Value(3), Value(4)]],
            [[Value(3), Value(4)], [Value(3), Value(4)]],
        ]
    )
    C = A + B

    circuit, _ = Value.compile_layered_circuit(C[0][0][0])
    assert len(C) == 2
    assert circuit.size == 3
    assert ZkProver(circuit, DOMAIN).prove()


def test_circuit_generation_matrix_multiplication():
    A = np.array([[Value(1), Value(2)], [Value(2), Value(1)]])
    B = np.array([Value(3), Value(4)])
    C = A @ B
    circuit, _ = Value.compile_layered_circuit(C[0])
    draw_dot(C[0]).render(
        "dohko/zkgrad/tests/assets/matrix_multiplication", format="png", cleanup=True
    )
    assert circuit.size == 4
    assert ZkProver(circuit, DOMAIN).prove()
