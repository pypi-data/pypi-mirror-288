import math
from typing import List, Set
from typing import List, Set, Dict, Union, Type
from collections import defaultdict
from uuid import uuid4
import math
from dohko.circuits.circuit import LayeredCircuit, Gate, GateType, Layer
from dohko.commitments.mkzg.ecc import curve_order
import time
from concurrent.futures import ThreadPoolExecutor


SCALE = 1e8
SHIFT = 1e16


def scale_number(x: "Value", scale=SCALE, shift=SHIFT):
    if x.scaled:
        return x
    x.scaled = True
    x.data = int(round(x.data, 6) * scale + shift)
    return x


def scaled_multiplication(x: "Value", y: "Value", scale=10, shift=0):
    if not x.scaled or not y.scaled:
        raise ValueError("Both values are already scaled")
    z = (
        ((x.data * y.data) - (x.data + y.data) * shift + pow(shift, 2)) / scale
    ) + shift
    return Value(z, [x, y], "*")


powers_of_2 = {
    # 0: 1,  # @TODO: Remove this and add a feature to libra prover to handle outputs with a single value
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


TGRAPH = Union[Type["Value"]]
TVALUE = Union[Type["Value"]]


class CircuitPreprocessor:
    def __init__(self, output: "Value", Graph: TGRAPH, Value: TVALUE):
        self.Graph = Graph
        self.output = output
        self.Value = Value
        self.used_nodes_ids = {}
        self.circuit_layers = self.output.get_layers()
        self.circuit = list(self.circuit_layers[:])

    def preprocess_node_path(
        self,
        layer: List["Value"],
        node: "Value",
        idx: int,
    ):
        node_layer_id = node.layer_id
        next_nodes: List["Value"] = node.next
        for next_node in next_nodes:
            next_node_layer_id = next_node.layer_id
            is_immediate_layer_above = next_node_layer_id - node_layer_id == 1
            self.used_nodes_ids[next_node.id] = next_node
            if is_immediate_layer_above and next_node._op != "relay":
                next_node_children = next_node._prev
                next_node_children_ids = [
                    n.id for n in next_node_children if n is not None
                ]
                left_child_id = next_node_children_ids[0]
                right_child_id = (
                    next_node_children_ids[1] if len(next_node_children) > 1 else None
                )
                current_layer_node_ids = [n.id for n in layer]
                if left_child_id in current_layer_node_ids:
                    left_child_idx = current_layer_node_ids.index(left_child_id)
                    next_node.left_child_idx = left_child_idx
                if right_child_id in current_layer_node_ids:
                    right_child_idx = current_layer_node_ids.index(right_child_id)
                    next_node.right_child_idx = right_child_idx
                # used_nodes.append(next_node)

            elif not is_immediate_layer_above:
                layer_diff = next_node_layer_id - node_layer_id
                layer_to_insert = node_layer_id + 1
                current_past_node = node
                current_past_node_layer_idx = [
                    n.id for n in self.circuit[layer_to_insert - 1]
                ].index(current_past_node.id)
                while layer_diff > 1:
                    bottom_relay = Value(
                        node.data,
                        [current_past_node, None],
                        "relay",
                    )

                    current_past_node.next.append(bottom_relay)
                    self.used_nodes_ids[bottom_relay.id] = bottom_relay
                    bottom_relay._prev = [current_past_node, None]
                    bottom_relay.layer_id = layer_to_insert
                    self.circuit[layer_to_insert].append(bottom_relay)
                    bottom_relay.left_child_idx = current_past_node_layer_idx
                    bottom_relay.right_child_idx = None
                    current_past_node = bottom_relay
                    layer_diff -= 1
                    layer_to_insert += 1
                    current_past_node_layer_idx = len(self.circuit[layer_to_insert]) - 1
                node_idx_prev = [n.id for n in next_node._prev if n is not None].index(
                    node.id
                )
                next_node._prev[node_idx_prev] = bottom_relay
                next_node.left_child_idx = node_idx_prev
                next_node.right_child_idx = None
            if not len(node._prev) and idx > 0:
                current_node_layer_id = node.layer_id
                current_node = node
                layer_to_insert = next_node_layer_id + 1
                input_layer = 0
                current_node_layer_diff = current_node_layer_id - input_layer
                while current_node_layer_diff > 0:
                    bottom_relay = Value(
                        node.data,
                    )
                    current_node._prev = [bottom_relay, None]
                    current_node._op = "relay"
                    bottom_relay.layer_id = current_node_layer_id - 1
                    bottom_relay.next.append(current_node)
                    self.circuit[current_node_layer_id - 1].append(bottom_relay)
                    current_node.left_child_idx = (
                        len(self.circuit[current_node_layer_id - 1]) - 1
                    )
                    current_node.right_child_idx = None
                    current_node_layer_diff -= 1
                    current_node_layer_id -= 1
                    self.used_nodes_ids[bottom_relay.id] = bottom_relay
                    current_node = bottom_relay

    def preprocess_circuit(self):
        for idx, layer in enumerate(self.circuit):
            futures = []

            with ThreadPoolExecutor() as executor:
                for node_idx, node in enumerate(layer):
                    future = executor.submit(
                        self.preprocess_node_path, layer, node, idx
                    )
                    futures.append(future)
        [future.result() for future in futures]
        return self.circuit


def _is_power_of_two(x: int):
    return x in powers_of_2.values() and x < powers_of_2[31]


def fix_layer(node: "Value", circuit: List[List["Value"]]) -> List[List["Value"]]:
    if node.data == 2.0:
        print("Node data", node.data)
    next_nodes = node.next
    if not len(next_nodes):
        return circuit
    layer_ids = [n.layer_id for n in next_nodes if n.layer_id is not None]
    if node.layer_id == 0 and not len(layer_ids):
        return circuit
    max_layer_id = max(layer_ids)
    if node.layer_id < max_layer_id:
        current_node_layer_id = node.layer_id
        current_node_layer_idx = circuit[current_node_layer_id].index(node)
        circuit[current_node_layer_id].pop(current_node_layer_idx)
        correct_layer_id = max_layer_id + 1
        try:
            circuit[correct_layer_id]
        except:
            correct_layer_id = correct_layer_id - 1
        node.layer_id = correct_layer_id
        circuit[correct_layer_id].append(node)
    return circuit


def connect_circuit_above(
    circuit_layers: List[List["Value"]],
    Graph: TGRAPH,
    Value: TVALUE,
    id_layers: Dict[int, int],
):
    circuit = circuit_layers[:]
    for idx, layer in enumerate(circuit[1:]):
        idx += 1
        for node_id, node in enumerate(layer):
            for node_output in node.next:
                node_output_layer = node_output.layer_id
                last_node = node
                current_node_layer = node.layer_id
                if current_node_layer - node_output_layer > 1:
                    while current_node_layer > node_output_layer + 1:
                        next_node = Value(last_node.data)
                        next_node.layer_id = current_node_layer - 1
                        next_node._prev = (last_node, None)
                        last_node.next.append(next_node)
                        id_layers[next_node.id] = current_node_layer - 1
                        next_node._op = "relay"
                        current_node_layer -= 1
                        circuit[current_node_layer].append(next_node)
                        last_node = next_node
                    prev_index = [x.id for x in node_output._prev].index(node.id)
                    node_output._prev[prev_index] = last_node
    return circuit


def connect_circuit_below(
    circuit_layers: List[List["Value"]],
    Graph: TGRAPH,
    Value: TVALUE,
):
    circuit = circuit_layers[:]
    for idx, layer in enumerate(circuit):
        if idx == 0:
            if len(layer) == 1:
                first_node = layer[0]
                second_node = Graph(
                    first_node.data,
                    [first_node._prev[1], first_node._prev[0]],
                    first_node._op,
                )
                layer.append(second_node)
        for node_id, node in enumerate(layer):
            current_layer_idx = idx
            last_node = node
            stop_clause = not len(node._prev)
            if idx == len(circuit) - 1:
                continue
            while current_layer_idx < len(circuit) - 1 and stop_clause:
                next_node = Value(last_node.data)
                last_node._prev = (next_node, None)
                last_node._op = "relay"
                last_node.layer_id = current_layer_idx
                if current_layer_idx > idx:
                    circuit[current_layer_idx].append(last_node)
                current_layer_idx += 1
                last_node = next_node
                stop_clause = not len(next_node._prev)
    return circuit


def connect_circuit(
    circuit_layers: List[List["Value"]],
    Graph: TGRAPH,
    Value: TVALUE,
    id_layers: Dict[int, int],
):
    circuit = circuit_layers[:]
    start = time.time()
    circuit = connect_circuit_above(circuit_layers[:], Graph, Value, id_layers)
    print("Time to connect above", time.time() - start)
    print("Circuit layers", len(circuit))
    start = time.time()
    circuit = connect_circuit_below(circuit[:], Graph, Value)
    print("Time to connect below", time.time() - start)
    return circuit


def preprocess_circuit(
    output: "Value",
    Graph: TGRAPH,
    Value: TVALUE,
):
    circuit_layers = output.get_layers()
    circuit = list(circuit_layers[:])
    used_nodes_ids = {}

    def process_immediate_node(
        node: "Value", layer: List["Value"], used_nodes_ids: Dict[int, "Value"]
    ):
        node_layer_id = node.layer_id
        next_nodes = node.next
        for next_node in next_nodes:
            next_node_layer_id = next_node.layer_id
            is_immediate_layer_above = next_node_layer_id - node_layer_id == 1
            used_nodes_ids[next_node.id] = next_node
            if is_immediate_layer_above and next_node._op != "relay":
                next_node_children = next_node._prev
                next_node_children_ids = [
                    n.id for n in next_node_children if n is not None
                ]
                left_child_id = next_node_children_ids[0]
                right_child_id = (
                    next_node_children_ids[1] if len(next_node_children) > 1 else None
                )
                current_layer_node_ids = [n.id for n in layer]
                if left_child_id in current_layer_node_ids:
                    left_child_idx = current_layer_node_ids.index(left_child_id)
                    next_node.left_child_idx = left_child_idx
                if right_child_id in current_layer_node_ids:
                    right_child_idx = current_layer_node_ids.index(right_child_id)
                    next_node.right_child_idx = right_child_idx
            if len(next_node.next):
                process_immediate_node(next_node, layer, used_nodes_ids)

    counter = 0
    for idx, layer in enumerate(circuit):

        for node_idx, node in enumerate(layer):
            # if node.new:
            #     continue
            node_layer_id = node.layer_id
            next_nodes = node.next
            for next_node in next_nodes:
                counter += 1
                next_node_layer_id = next_node.layer_id
                is_immediate_layer_above = next_node_layer_id - node_layer_id == 1
                used_nodes_ids[next_node.id] = next_node
                if is_immediate_layer_above and next_node._op != "relay":
                    next_node_children = next_node._prev
                    next_node_children_ids = [
                        n.id for n in next_node_children if n is not None
                    ]
                    left_child_id = next_node_children_ids[0]
                    right_child_id = (
                        next_node_children_ids[1]
                        if len(next_node_children) > 1
                        else None
                    )
                    current_layer_node_ids = [n.id for n in layer]
                    if left_child_id in current_layer_node_ids:
                        left_child_idx = current_layer_node_ids.index(left_child_id)
                        next_node.left_child_idx = left_child_idx
                    if right_child_id in current_layer_node_ids:
                        right_child_idx = current_layer_node_ids.index(right_child_id)
                        next_node.right_child_idx = right_child_idx
                    # used_nodes.append(next_node)

                elif not is_immediate_layer_above:
                    layer_diff = next_node_layer_id - node_layer_id
                    layer_to_insert = node_layer_id + 1
                    current_past_node = node
                    current_past_node_layer_idx = [
                        n.id for n in circuit[layer_to_insert - 1]
                    ].index(current_past_node.id)
                    while layer_diff > 1:
                        counter += 1
                        bottom_relay = Value(
                            node.data,
                            [current_past_node, None],
                            "relay",
                        )
                        bottom_relay.new = True
                        current_past_node.next.append(bottom_relay)
                        used_nodes_ids[bottom_relay.id] = bottom_relay
                        bottom_relay._prev = [current_past_node, None]
                        bottom_relay.layer_id = layer_to_insert
                        circuit[layer_to_insert].append(bottom_relay)
                        bottom_relay.left_child_idx = current_past_node_layer_idx
                        bottom_relay.right_child_idx = None
                        current_past_node = bottom_relay
                        layer_diff -= 1
                        layer_to_insert += 1
                        current_past_node_layer_idx = len(circuit[layer_to_insert]) - 1
                    node_idx_prev = [
                        n.id for n in next_node._prev if n is not None
                    ].index(node.id)
                    next_node._prev[node_idx_prev] = bottom_relay
                    next_node.left_child_idx = node_idx_prev
                    next_node.right_child_idx = None
                is_not_connected_to_root = not len(node._prev) and idx > 0
                if is_not_connected_to_root:
                    current_node_layer_id = node.layer_id
                    current_node = node
                    layer_to_insert = next_node_layer_id + 1
                    input_layer = 0
                    current_node_layer_diff = current_node_layer_id - input_layer
                    while current_node_layer_diff > 0:
                        counter += 1
                        bottom_relay = Value(
                            node.data,
                        )
                        bottom_relay.new = True
                        current_node._prev = [bottom_relay, None]
                        current_node._op = "relay"
                        bottom_relay.layer_id = current_node_layer_id - 1
                        bottom_relay.next.append(current_node)
                        circuit[current_node_layer_id - 1].append(bottom_relay)
                        current_node.left_child_idx = (
                            len(circuit[current_node_layer_id - 1]) - 1
                        )
                        current_node.right_child_idx = None
                        current_node_layer_diff -= 1
                        current_node_layer_id -= 1
                        used_nodes_ids[bottom_relay.id] = bottom_relay
                        current_node = bottom_relay
    # breakpoint()
    return circuit


def to_circuit(
    output: "Value",
    Graph: TGRAPH,
    Value: TVALUE,
):
    non_linearities: Dict[int, Dict[str, List[Value]]] = defaultdict(
        lambda: defaultdict(list)
    )
    start = time.time()
    connected_circuit_layers = list(reversed(preprocess_circuit(output, Graph, Value)))
    print("Time to preprocess circuit", time.time() - start)
    start = time.time()
    layers_len = len(connected_circuit_layers)
    range_len = range(layers_len)
    switch_map = {k: v for k, v in zip(reversed(range_len), range_len)}
    for layer in connected_circuit_layers:
        for node in layer:
            node.layer_id = switch_map[node.layer_id]
            for next_node in node.next:
                next_node.layer_id = switch_map[next_node.layer_id]
    print("Time to switch layers", time.time() - start)
    idx = len(connected_circuit_layers[:-1]) - 1
    start = time.time()
    # Add dummy gates to the last layer if the number of elements is not a power of 2
    num_elements_current_layer = len(connected_circuit_layers[0])
    layer = connected_circuit_layers[0]
    corrected_num_elements_current_layer = 0
    if not _is_power_of_two(num_elements_current_layer):
        for i in range(31):
            if num_elements_current_layer <= powers_of_2[i + 1]:
                corrected_num_elements_current_layer = powers_of_2[i + 1]
                break
        if corrected_num_elements_current_layer == 0:
            raise ValueError("Number of elements in the next layer is too large")
    remaining_elements_current_layer = (
        corrected_num_elements_current_layer - num_elements_current_layer
    )
    if remaining_elements_current_layer > 0:
        for i in range(remaining_elements_current_layer):
            new_node = Graph(
                0,
                [Value(0), None],
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
            for i in range(31):
                if num_elements_current_layer > powers_of_2[i + 1]:
                    continue
                if num_elements_current_layer <= powers_of_2[i + 1]:
                    corrected_num_elements_current_layer = powers_of_2[i + 1]
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
                    0,
                    [Value(0), None],
                    "relay",
                    dummy_gate=True,
                )
                new_node.layer_id = idx
                new_node.left_child_idx = num_elements_current_layer + i
                layer.append(new_node)
    print("Time to add dummy gates", time.time() - start)
    return connected_circuit_layers, non_linearities


def compile_layered_circuit(
    output: "Value", Graph: TGRAPH, Value: TVALUE, integer=True, debug=False
):
    start = time.time()
    connected_circuit_layers, non_linearities = to_circuit(output, Graph, Value)
    print("Time to compile circuit relays", time.time() - start)
    start = time.time()
    circuit = LayeredCircuit()
    circuit.size = len(connected_circuit_layers)
    circuit.total_depth = len(connected_circuit_layers)
    circuit.circuit = []
    for idx, base_layer in enumerate(reversed(connected_circuit_layers)):
        layer_arr = []

        for node in base_layer:
            if idx == 0:
                layer_arr.append(
                    Gate(
                        GateType.Input,
                        0,
                        node.data if not integer else node.data_int,
                        0,
                        0,
                        False,
                    )
                )
            else:
                if len(node._prev) == 0:
                    continue
                if len(node._prev) <= 1:
                    raise ValueError("Node has only one child")
                right_child = node._prev[1]
                left_child_idx = node.left_child_idx
                right_child_idx = node.right_child_idx if right_child else 0
                gate_type = GateType.Mul
                if node._op == "relay":
                    gate_type = GateType.Relay
                    if left_child_idx is None:
                        if right_child_idx is None:
                            raise ValueError(
                                "Both left and right child indices are None"
                            )
                        left_child_idx = right_child_idx
                        right_child_idx = 0
                elif node._op == "+":
                    gate_type = GateType.Add
                if left_child_idx is None or right_child_idx is None:
                    raise ValueError(
                        f"Child indices are not defined for node at layer: {idx}"
                    )
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
        base_layer_len = len(base_layer)
        layer = Layer(gates=layer_arr[:])
        layer.bitLength = int(math.log2(base_layer_len)) if base_layer_len > 1 else 1
        layer.size = base_layer_len
        circuit.circuit.append(layer)
    print("Time to compile layered circuit", time.time() - start)
    if debug:
        return circuit, non_linearities, connected_circuit_layers
    return circuit, non_linearities


THRESHOLD = 2**32
HALF_THRESHOLD = 2**16
SCALE = 10


def float_to_natural(x, decimals=1, max_value=HALF_THRESHOLD):
    scale = 10**decimals
    return int(x + max_value) * scale


def natural_to_float(y, decimals=5, max_value=THRESHOLD):
    scale = 10**decimals
    return (y - max_value * scale) / scale


LayerList: List[List["Value"]] = []


class Value:
    """stores a single scalar value and its gradient"""

    def __init__(
        self,
        data,
        _children=(),
        _op="",
        nl_op="",
        dummy_gate=False,
        no_grad=False,
        integer=True,
        past_node_ids=[],
    ):
        self.data = data
        self.data_int = None
        self.grad = 0
        self.sign = None
        self.layer_id = None
        self.scaled = False
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = _children
        self._op = _op  # the op that produced this node, for graphviz / debugging / etc
        self.no_grad = no_grad
        self.nl_op = nl_op
        self.left_child_idx = None
        self.right_child_idx = None
        self.dummy_gate = dummy_gate
        self.id = uuid4().int
        self.integer = integer
        self.past_node_ids = past_node_ids
        self.next = []
        self.counter = 0
        self.new = False
        if self.integer:
            self.data_int = int(self.data * 10**5)
            self.data_int = self.data_int % curve_order

    def compute_layer_id(self, left, right, output):
        left_layer_id = left.layer_id
        right_layer_id = right.layer_id
        if left_layer_id is not None and right_layer_id is None:
            right.layer_id = left_layer_id
        elif right_layer_id is not None and left_layer_id is None:
            left.layer_id = right_layer_id
        elif left_layer_id is None and right_layer_id is None:
            len_layers = 1 if len(LayerList) > 0 else 0
            left.layer_id = len_layers
            right.layer_id = len_layers
        left_layer_id = left.layer_id
        right_layer_id = right.layer_id
        next_layer_id = max(left_layer_id, right_layer_id) + 1
        output.layer_id = next_layer_id
        self.set_layer_element(left_layer_id, left)
        self.set_layer_element(right_layer_id, right)
        self.set_layer_element(next_layer_id, output)
        left_layer_idx = [n.id for n in LayerList[left_layer_id]]
        right_layer_idx = [n.id for n in LayerList[right_layer_id]]
        left_node_idx = left_layer_idx.index(left.id)
        right_node_idx = right_layer_idx.index(right.id)
        output.left_child_idx = left_node_idx
        output.right_child_idx = right_node_idx

    def get_layers(self):
        return LayerList

    def set_layer_element(self, layer_id, element):
        diff = (layer_id + 1) - len(LayerList)
        if diff > 0:
            for _ in range(diff):
                LayerList.append([])
        layer_ids = [n.id for n in LayerList[layer_id] if n.id == element.id]
        if len(layer_ids):
            return
        LayerList[layer_id].append(element)

    def delete_layer_element(self, layer_id, element):
        layer_ids = [n.id for n in LayerList[layer_id] if n.id == element.id]
        if len(layer_id):
            element_idx = layer_ids.index(element.id)
            LayerList[layer_id].remove(element_idx)
        else:
            raise ValueError("Element not found in layer")

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(
            self.data + other.data,
            [self, other],
            "+",
            past_node_ids=self.past_node_ids,
        )
        self.compute_layer_id(self, other, out)
        other.next.append(out)
        self.next.append(out)

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward if not self.no_grad else lambda: None

        return out

    def __mul__(self, other):
        # TODO: Add the features here for all methods.
        if other is None:
            raise ValueError("Other value is None")
        other = other if isinstance(other, Value) else Value(other)

        out = Value(
            self.data * other.data,
            [self, other],
            "*",
            past_node_ids=self.past_node_ids,
        )
        self.compute_layer_id(self, other, out)
        other.next.append(out)
        self.next.append(out)

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward if not self.no_grad else lambda: None

        return out

    def __pow__(self, other):
        assert isinstance(
            other, (int, float)
        ), "only supporting int/float powers for now"
        t = self.data**other
        right: Value = Value(t / self.data)
        out = Value(t, [self, right], "*", nl_op="**", past_node_ids=self.past_node_ids)
        self.compute_layer_id(self, right, out)
        right.next.append(out)
        self.next.append(out)

        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad

        out._backward = _backward if not self.no_grad else lambda: None

        return out

    def tanh(self):
        x = self.data
        t = (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)
        if self.integer:
            t = round(t, 5)
        right: Value = t / self
        out = Value(
            t, [self, right], "*", nl_op="tanh", past_node_ids=self.past_node_ids
        )
        self.compute_layer_id(self, right, out)
        right.next.append(out)
        self.next.append(out)

        def _backward():
            self.grad += (1 - t**2) * out.grad

        out._backward = _backward if not self.no_grad else lambda: None
        return out

    def exp(self):
        x = self.data
        if self.integer:
            t = round(math.exp(x), 5)
        else:
            t = math.exp(x)

        right: Value = t / self
        out = Value(
            t, [self, right], "*", nl_op="exp", past_node_ids=self.past_node_ids
        )
        self.compute_layer_id(self, right, out)
        self.next.append(out)
        right.next.append(out)

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward if not self.no_grad else lambda: None
        return out

    def log(self):
        x = self.data
        if self.integer:
            t = round(math.log(x), 5)
        else:
            t = math.log(x)

        right: Value = t / self
        out = Value(
            t, [self, right], "*", nl_op="log", past_node_ids=self.past_node_ids
        )
        self.compute_layer_id(self, right, out)
        self.next.append(out)
        right.next.append(out)

        def _backward():
            self.grad += (1 / x) * out.grad

        out._backward = _backward if not self.no_grad else lambda: None
        return out

    def relu(self):
        t = 0 if self.data < 0 else self.data
        right: Value = t / self
        out = Value(t, [self, right], "*", nl_op="ReLU")
        self.compute_layer_id(self, right, out)
        self.next.append(out)
        right.next.append(out)

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward if not self.no_grad else lambda: None

        return out

    def backward(self):
        # topological order all of the children in the graph
        topo: List[Value] = []
        visited: Set[Value] = set()

        def build_topo(v: Value):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self):  # -self
        return self * -1

    def __radd__(self, other):  # other + self
        return self + other

    def __sub__(self, other):  # self - other
        return self + (-other)

    def __rsub__(self, other):  # other - self
        return other + (-self)

    def __rmul__(self, other):  # other * self
        return self * other

    def __truediv__(self, other):  # self / other
        return self * other**-1

    def __rtruediv__(self, other):  # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    @staticmethod
    def to_circuit(output: "Value", debug: bool = False):
        return to_circuit(output, Value, Value, debug=debug)

    @staticmethod
    def compile_layered_circuit(output: "Value", debug: bool = False):
        return compile_layered_circuit(output, Value, Value, debug=debug)

    @staticmethod
    def proprocess_circuit(output: "Value", debug: bool = False):
        return preprocess_circuit(output, Value, Value)
