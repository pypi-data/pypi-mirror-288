from dohko.zkgrad.zkgrad.arithmetics.base import FP16x16Base
from dohko.zkgrad.zkgrad.engine import Value
from typing import List, Set, Dict, Union, Type
from collections import defaultdict
from uuid import uuid4
import math
from dohko.circuits.circuit import LayeredCircuit, Gate, GateType, Layer
from abc import ABC, abstractmethod

powers_of_2 = {
    0: 1,
    1: 2,
    2: 4,
    3: 8,
    4: 16,
    5: 32,
    6: 64,
    7: 128,
    8: 256,
    9: 512,
    10: 1024,
    11: 2048,
    12: 4096,
    13: 8192,
    14: 16384,
    15: 32768,
    16: 65536,
    17: 131072,
    18: 262144,
    19: 524288,
    20: 1048576,
    21: 2097152,
    22: 4194304,
    23: 8388608,
    24: 16777216,
    25: 33554432,
    26: 67108864,
    27: 134217728,
    28: 268435456,
    29: 536870912,
    30: 1073741824,
    31: 2147483648,
}


TGRAPH = Union[Type["GraphFp16"]]
TVALUE = Union[Type[FP16x16Base]]


def _is_power_of_two(x: int):
    return x in powers_of_2.values() and x < powers_of_2[31]


def connect_circuit(
    circuit_layers: List[List["Graph"]],
    Graph: TGRAPH,
    Value: TVALUE,
):
    circuit = circuit_layers[:]
    for idx, layer in enumerate(circuit[:-1]):
        for node_id, node in enumerate(layer):
            current_layer_idx = idx
            last_node = node
            stop_clause = not hasattr(node, "_prev")
            last_node_id = node_id
            while current_layer_idx < len(circuit) and stop_clause:

                node = Graph(
                    last_node,
                    (Value(last_node._mag, last_node._sign), None),
                    "relay",
                )
                node.layer_id = current_layer_idx
                if current_layer_idx == idx:
                    circuit[current_layer_idx][node_id] = node
                else:
                    previous_connected_node = circuit[current_layer_idx - 1][
                        last_node_id
                    ]
                    previous_connected_node._prev = (node, None)
                    circuit[current_layer_idx].append(node)
                    last_node_id = len(circuit[current_layer_idx]) - 1
                current_layer_idx += 1
                last_node = node
                next_node = last_node._prev[0]
                stop_clause = not hasattr(next_node, "_prev")
    return circuit


def to_circuit(
    output: "Graph",
    Graph: TGRAPH,
    Value: TVALUE,
):
    # topological order all of the children in the graph
    topo: List[GraphFp16] = []
    layers: Dict[int, List[GraphFp16]] = defaultdict(list)
    non_linearities: Dict[int, Dict[str, List[GraphFp16]]] = defaultdict(
        lambda: defaultdict(list)
    )
    visited: Set[GraphFp16] = set()

    def build_topo(v: GraphFp16, layer_id=0):
        if v.id not in visited:
            visited.add(v.id)
            if hasattr(v, "_prev"):
                for child in v._prev:
                    build_topo(child, layer_id + 1)
            topo.append(v)
            if hasattr(v, "nl_op") and v.nl_op:
                non_linearities[layer_id][v.nl_op].append(v)
            layers[layer_id].append(v)

    build_topo(output)
    layer_indices = sorted(layers.keys())
    circuit_layers = [layers[i] for i in layer_indices]
    connected_circuit_layers = connect_circuit(circuit_layers, Graph, Value)
    connected_circuit_indices = defaultdict(list)
    for lidx, connected_layer in enumerate(connected_circuit_layers):
        for node in connected_layer:
            connected_circuit_indices[lidx].append(
                (node._mag, node._prev if hasattr(node, "_prev") else None)
            )
    # Add layer metadata to each circuit node
    for idx, layer in enumerate(connected_circuit_layers[:-1]):
        next_layer = (
            connected_circuit_layers[idx + 1]
            if idx + 1 < len(connected_circuit_layers)
            else []
        )
        next_layer_ids = [n.id for n in next_layer]

        for node in layer:
            node.layer_id = idx
            left_child, right_child = node._prev
            left_child_id = left_child.id
            right_child_id = right_child.id if right_child else None
            next_layer_ids = [n.id for n in next_layer]
            if left_child_id in next_layer_ids:
                left_idx = next_layer_ids.index(left_child_id)
                node.left_child_idx = left_idx
                if right_child is not None:
                    right_child.layer_id = idx + 1
            else:
                pass
            if right_child_id in next_layer_ids:
                node.right_child_idx = next_layer_ids.index(right_child_id)
                left_child.layer_id = idx + 1

    # Add dummy gates to the last layer if the number of elements is not a power of 2
    num_elements_current_layer = len(connected_circuit_layers[0])
    layer = connected_circuit_layers[0]
    corrected_num_elements_current_layer = 0
    if not _is_power_of_two(num_elements_current_layer):
        for i in range(32):
            if num_elements_current_layer <= powers_of_2[i]:
                corrected_num_elements_current_layer = powers_of_2[i]
                break
        if corrected_num_elements_current_layer == 0:
            raise ValueError("Number of elements in the next layer is too large")
    remaining_elements_current_layer = (
        corrected_num_elements_current_layer - num_elements_current_layer
    )
    if remaining_elements_current_layer > 0:
        for i in range(remaining_elements_current_layer):
            new_node = Graph(
                Value(0, False),
                (Value(0, False), None),
                "relay",
                dummy_gate=True,
            )
            new_node.layer_id = idx
            new_node.left_child_idx = num_elements_current_layer + i
            layer.append(new_node)
    for idx in range(1, len(connected_circuit_layers)):
        layer = connected_circuit_layers[idx]
        num_elements_last_layer = len(connected_circuit_layers[idx - 1])
        num_elements_current_layer = len(layer)
        max_elements = max(num_elements_current_layer, num_elements_last_layer)
        corrected_num_elements_current_layer = 0
        if not _is_power_of_two(max_elements):
            for i in range(32):
                if num_elements_current_layer > powers_of_2[i]:
                    continue
                if num_elements_current_layer <= powers_of_2[i]:
                    corrected_num_elements_current_layer = powers_of_2[i]
                    break
            if corrected_num_elements_current_layer == 0:
                raise ValueError("Number of elements in the next layer is too large")
        else:
            corrected_num_elements_current_layer = max_elements
        remaining_elements_current_layer = (
            corrected_num_elements_current_layer - num_elements_current_layer
        )
        if remaining_elements_current_layer > 0:
            for i in range(remaining_elements_current_layer):
                new_node = Graph(
                    Value(0, False),
                    (Value(0, False), None),
                    "relay",
                    dummy_gate=True,
                )
                new_node.layer_id = idx
                new_node.left_child_idx = num_elements_current_layer + i
                layer.append(new_node)
    return connected_circuit_layers, non_linearities


def compile_layered_circuit(output: "Graph", Graph: TGRAPH, Value: TVALUE):
    connected_circuit_layers, non_linearities = to_circuit(output, Graph, Value)
    circuit = LayeredCircuit()
    circuit.size = len(connected_circuit_layers)
    circuit.total_depth = len(connected_circuit_layers)
    circuit.circuit = [Layer()] * len(connected_circuit_layers)
    for idx, layer in enumerate(reversed(connected_circuit_layers)):
        layer_arr = []
        circuit.circuit[idx].bitLength = (
            int(math.log2(len(layer))) if len(layer) > 1 else 1
        )
        circuit.circuit[idx].size = len(layer)
        for node in layer:
            if idx == 0:
                layer_arr.append(Gate(GateType.Input, 0, node._mag, 0, 0, False))
            else:
                left_child = node._prev[0]
                right_child = node._prev[1]
                left_child_idx = node.left_child_idx
                right_child_idx = node.right_child_idx if right_child else 0
                gate_type = GateType.Mul
                if gate_type == "relay":
                    gate_type = GateType.Relay
                elif gate_type == "+":
                    gate_type = GateType.Add
                layer_arr.append(
                    Gate(
                        gate_type,
                        node.layer_id,
                        left_child_idx,
                        right_child_idx,
                        0,
                        False,
                    )
                )
            circuit.circuit[idx].gates = layer_arr
    return circuit, non_linearities


class FP16x16(FP16x16Base):
    def __add__(self, other) -> "FP16x16":
        result = super().__add__(other)
        if self.id == other.id:
            other = FP16x16Base.new(other._mag, other._sign)
        return GraphFp16(result, (self, other), "+")

    def __mul__(self, other) -> "FP16x16":
        result = super().__mul__(other)
        if self.id == other.id:
            other_ = FP16x16Base.new(other._mag, other._sign)
            return GraphFp16(result, (self, other_), "*")
        # TODO: Implement this circuit reduction technique
        # elif not len(other.prev) and len(self.prev) > 1:
        #     left_right = self._prev[1]
        #     left_left = self._prev[0]
        #     if not len(left_right.prev):
        #         self = GraphFp16(result, (left_left, left_right * other), "+")
        return GraphFp16(result, (self, other), "*")

    def __radd__(self, other):  # other + self
        return self + other

    def __sub__(self, other) -> "FP16x16":
        result = super().__sub__(other)
        if self.id == other.id:
            other = FP16x16Base.new(other._mag, other._sign)
        return GraphFp16(result, (self, -other), "+")

    def __pow__(self, other) -> "FP16x16":
        result = super().__pow__(other)
        if self.id == other.id:
            current = FP16x16Base.new(self._mag, self._sign)
            other = FP16x16Base.new(other._mag, other._sign)
            self = current
        return GraphFp16(result, (self, other), "**")

    def __rmul__(self, other):  # other * self
        return self * other

    def relay(self) -> "FP16x16":
        relay_value = FP16x16Base.new(self._mag, False)
        return GraphFp16(self, (relay_value, None), "relay")

    def exp(self) -> "FP16x16":
        result = super().exp()
        if self._mag == 0:
            return GraphFp16(result, (result, 0), "*", "exp")
        divisor = result / self
        return GraphFp16(result, (self, divisor), "*", "exp")

    def ln(self) -> "FP16x16":
        result = super().ln()
        if self._mag == 0:
            return GraphFp16(result, (result, 0), "*", "ln")
        divisor = result / self
        return GraphFp16(result, (self, divisor), "*", "log")

    def sqrt(self) -> "FP16x16":
        result = super().sqrt()
        if self._mag == 0:
            return GraphFp16(result, (result, 0), "*", "sqrt")
        divisor = result / self
        return GraphFp16(result, (result, divisor), "*", "sqrt")

    def tanh(self) -> "FP16x16":
        result = super().tanh()
        if self._mag == 0:
            return GraphFp16(result, (result, 0), "*", "tanh")
        divisor = result / self
        return GraphFp16(result, (self, divisor), "*", "tanh")

    @staticmethod
    def new_unscaled(mag: int, sign: bool = False) -> "FP16x16":
        result = FP16x16Base.new_unscaled(mag, sign)
        return FP16x16(result._mag, result._sign)


class Graph(ABC):
    @abstractmethod
    def to_circuit(self) -> "LayeredCircuit":
        pass

    @abstractmethod
    def compile_layered_circuit(self) -> "LayeredCircuit":
        pass


class GraphFp16(Graph, FP16x16, Value):
    def __init__(
        self,
        data: FP16x16Base,
        _children=(),
        _op="",
        nl_op="",
        no_grad=True,
        dummy_gate=False,
    ):
        assert len(_children) in [0, 2]
        FP16x16.__init__(self, data._mag, data._sign)
        Value.__init__(self, data, _children, _op, no_grad=no_grad)
        self.nl_op = nl_op
        self.layer_id = None
        self.left_child_idx = None
        self.right_child_idx = None
        self.dummy_gate = dummy_gate

    @staticmethod
    def to_circuit(output: "GraphFp16"):
        return to_circuit(output, GraphFp16, FP16x16)

    @staticmethod
    def compile_layered_circuit(output: "GraphFp16"):
        return compile_layered_circuit(output, GraphFp16, FP16x16)
