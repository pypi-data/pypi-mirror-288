import random
from dohko.commitments.plookup.setup import Setup
from dohko.commitments.plookup.program import Params
from dohko.commitments.plookup.prover import Prover, Proof
from dohko.commitments.plookup.verifier import Verifier
import matplotlib.pyplot as plt
import time


# setup: public setup includes srs
# public_table: public table
# witness: values to lookup
def prover(setup: Setup, params: Params, witness: list[int]):
    print("Beginning prover test")

    # print"table: ", params.table)
    # print"witness: ", witness)

    prover = Prover(setup, params)
    proof = prover.prove(witness)
    print("Prover test success")

    return proof


def prover_simple_array(setup: Setup, params: Params):
    print("Beginning prover_simple_array test")
    # values to lookup
    witness = [1, 1, 5, 5, 6, 6, 5]  # twinkle twinkle little star
    proof = prover(setup, params, witness)
    return proof


def prover_random_lookup(setup: Setup, params: Params, size: int):
    print("Beginning prover_random_lookup test")
    # values to lookup
    witness = []
    for _ in range(size):
        witness.append(random.randint(1, size))

    proof = prover(setup, params, witness)
    return proof


def verifier(setup: Setup, params: Params, proof: Proof):
    print("Beginning verifier test")
    verifier = Verifier(setup, params)
    assert verifier.verify(proof)
    print("Verifier test success")


def simple_test():
    # random number, normally comes from MPC(Multi-Party Computation)
    tau = 100
    # public table
    table = [1, 2, 3, 4, 5, 6, 7, 8]

    group_order_N = len(table)
    # number of powers of tau
    powers = group_order_N * 3
    # do setup
    setup = Setup(powers, tau)
    # set public params
    params = Params(table)
    # run prover
    proof = prover_simple_array(setup, params)
    # run verifier
    verifier(setup, params, proof)


def random_test(size):
    # random number, normally comes from MPC(Multi-Party Computation)
    tau = 100

    # public table
    # table = [1...256]
    table = []
    for i in range(1, size + 1):
        table.append(i)

    group_order_N = len(table)
    # number of powers of tau
    powers = group_order_N * 3
    # do setup
    s = time.time()
    setup = Setup(powers, tau)
    end = time.time() - s
    print("Setup time: ", time.time() - s)
    # set public params
    s = time.time()
    params = Params(table)
    params_end = time.time() - s
    print("Params time: ", time.time() - s)
    # run prover
    s = time.time()
    proof = prover_random_lookup(setup, params, 2)
    prover_end = time.time() - s
    print("Prover time: ", time.time() - s)
    # run verifier
    s = time.time()
    verifier(setup, params, proof)
    verifier_end = time.time() - s
    print("Verifier time: ", time.time() - s)
    return end, params_end, verifier_end, prover_end


if __name__ == "__main__":

    # s = time.time()
    # simple_test()
    # print("Simple test time: ", time.time() - s)
    sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
    durations = []
    for size in sizes:
        s = time.time()
        setup_time, params_time, verifier_time, prover_time = random_test(size)
        # end = time.time() - s
        durations.append((prover_time, setup_time, params_time, verifier_time))
        print(
            f"Table with size: {size}, Prover test time: {prover_time}s, Setup time: {setup_time}s, Params time: {params_time}s, Verifier time: {verifier_time}s"
        )
        # print("Random test time: ", end)
    X = [x for i, x in enumerate(sizes)]
    Ysetup = [y[1] for y in durations]
    Yparams = [y[2] for y in durations]
    Yprover = [y[0] for y in durations]
    Yverifier = [y[3] for y in durations]
    for i, duration in enumerate(durations):
        print(f"Computing a table with size: {sizes[i]} took: {duration}s")
    # print(X, Ysetup)
    plt.plot(X, Ysetup, label="Setup Time")
    plt.plot(X, Yprover, label="Prover Time")
    plt.plot(X, Yverifier, label="Verifier Time")
    plt.plot(X, Yparams, label="Params Time")
    plt.xlabel("Layer Size")  # add X-axis label
    plt.ylabel("Time")  # add Y-axis label
    plt.title("Complexity chart")  # add title
    plt.legend(loc="best")
    plt.show()
