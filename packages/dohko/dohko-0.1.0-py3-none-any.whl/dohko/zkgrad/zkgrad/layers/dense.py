from typing import List
from dohko.zkgrad.zkgrad.engine import Value
from dohko.zkgrad.zkgrad.layers.neuron import Neuron


class DenseLayer:
    def __init__(self, dim_in: int, dim_out: int):
        self.neurons = [Neuron(dim_in) for _ in range(dim_out)]

    def __call__(self, x):
        return [n(x) for n in self.neurons]

    def parameters(self) -> List[Value]:
        return [p for neuron in self.neurons for p in neuron.parameters()]
