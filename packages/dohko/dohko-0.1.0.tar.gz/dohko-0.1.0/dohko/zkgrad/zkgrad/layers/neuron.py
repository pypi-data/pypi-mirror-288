import random
from typing import List
from dohko.zkgrad.zkgrad.engine import Value


class Neuron:
    def __init__(self, dim: int):
        self.weights = [Value(random.uniform(-1, 1)) for _ in range(dim)]
        self.bias = Value(random.uniform(-1, 1))

    def __call__(self, x):
        activation: Value = sum((w * x for w, x in zip(self.weights, x)), self.bias)
        return activation.tanh()

    def parameters(self) -> List[Value]:
        return self.weights + [self.bias]
