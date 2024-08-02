from typing import List, Any
from sympy import FiniteField
from dohko.commitments.mkzg.ecc import curve_order
import random
import math
from dohko.types.gate import GateType

DOMAIN = FiniteField(curve_order)


class Gate:
    def __init__(
        self, ty: GateType, l: int, u: int, v: int, c: FiniteField, is_assert_zero: bool
    ):
        """Initializes a new instance of the Gate class.

        Args:
            ty (GateType): The gate type
            l (int): index layer of the left side
            u (int): index of the left input layer at layer l
            v (int): index of the right input layer at layer l
            c (FiniteField): Element of a finite field
            is_assert_zero (bool): Whether the gate is an assertion gate
        """
        self.ty: GateType = ty
        self.l: int = l  # index layer of the left side
        self.u: int = u  # index of the left input layer at layer l
        self.v: int = v  # index of the right input layer at layer l
        self.lv: int = (
            0  # represent an alternative or secondary layer index for the second input v
        )
        self.c: FiniteField = c  # This should be an element of a finite field
        self.is_assert: bool = is_assert_zero


class Layer:
    def __init__(self, gates: List[Gate] = []):
        self.gates: List[Gate] = gates
        self.bitLength: int = 0
        self.size: int = 0
        self.dadId: List[List[int]] = []  # map from subset id to real id
        self.dadBitLength: List[int] = []  # subset bit length
        self.dadSize: List[int] = []  # subset size
        self.maxDadSize: int = 0  # max subset size
        self.maxDadBitLength: int = 0  # max subset bit length


class LayeredCircuit:
    def __init__(self, domain: FiniteField = DOMAIN):
        self.circuit: List[Layer] = []
        self.size: int = 0
        self.domain = domain
        self.zero = domain.zero
        self.total_depth = 0
        self.prime = domain.characteristic()

    def _generate_random_point(self):
        return random.randint(1, self.prime - 1) % self.prime

    def readFromStream(stream: Any) -> "LayeredCircuit":
        # TODO: Implement reading from a stream (file, network, etc.)
        # This is a placeholder and needs to be implemented based on your specific input format
        raise NotImplementedError("readFromStream method is not implemented yet.")

    def randomize(self, layer_num: int, each_layer: int) -> "LayeredCircuit":
        c = LayeredCircuit(domain=self.domain)
        gate_size = 1 << each_layer
        c.circuit = [Layer() for _ in range(layer_num)]
        c.size = layer_num
        c.circuit[0].bitLength = each_layer
        c.circuit[0].size = gate_size
        c.circuit[0].gates = [
            Gate(
                GateType.Input,
                0,
                self.domain(self._generate_random_point()),
                0,
                self.zero,
                False,
            )
            for _ in range(gate_size)
        ]

        for i in range(1, layer_num):
            c.circuit[i].bitLength = each_layer
            c.circuit[i].size = gate_size
            c.circuit[i].gates = [
                Gate(
                    GateType.Add if gs % 2 == 0 else GateType.Mul,
                    self._generate_random_point() % i,
                    self._generate_random_point() % gate_size,
                    self._generate_random_point() % gate_size,
                    self.zero,
                    False,
                )
                for gs in range(gate_size)
            ]

        return c

    def subsetInit(self):
        # Initialize the necessary attributes for each layer
        self.total_depth = self.size
        for i in range(self.size):
            self.circuit[i].dadBitLength = [-1] * i
            self.circuit[i].dadSize = [0] * i
            self.circuit[i].dadId = [[] for _ in range(i)]
            self.circuit[i].maxDadBitLength = -1
            self.circuit[i].maxDadSize = 0

        # Initialize visited and subset indices
        visited_idx = [[0 for _ in range(layer.size)] for layer in self.circuit]
        subset_idx = [[0 for _ in range(layer.size)] for layer in self.circuit]

        # Iterate over the layers in reverse order
        for i in reversed(range(1, self.size)):
            for j in reversed(range(self.circuit[i].size)):
                g = self.circuit[i].gates[j]
                l = g.l
                v = g.v
                if l == -1:  # Continue if l is -1
                    continue
                if visited_idx[l][v] != i:
                    visited_idx[l][v] = i
                    subset_idx[l][v] = self.circuit[i].dadSize[l]
                    self.circuit[i].dadId[l].append(v)
                    self.circuit[i].dadSize[l] += 1
                g.lv = subset_idx[l][v]

            # Update dadBitLength and max values
            for j in range(i):
                self.circuit[i].dadBitLength[j] = math.ceil(
                    math.log2(self.circuit[i].dadSize[j])
                    if self.circuit[i].dadSize[j] > 0
                    else 0
                )
                if (1 << self.circuit[i].dadBitLength[j]) < self.circuit[i].dadSize[j]:
                    self.circuit[i].dadBitLength[j] += 1
                self.circuit[i].maxDadSize = max(
                    self.circuit[i].dadSize[j], self.circuit[i].maxDadSize
                )
                self.circuit[i].maxDadBitLength = max(
                    self.circuit[i].dadBitLength[j], self.circuit[i].maxDadBitLength
                )

    def test(self, layer_num) -> "LayeredCircuit":
        each_layer_size = (
            2**layer_num
        )  # Initial number of gates, could be set to a power of 2 for simplicity
        c = LayeredCircuit(domain=self.domain)
        c.circuit = [Layer() for _ in range(layer_num)]
        c.size = layer_num
        c.total_depth = layer_num
        # Initialize the first layer as input layer
        c.circuit[0].bitLength = int(
            math.log2(each_layer_size)
        )  # Calculate bit length as log base 2 of number of gates
        c.circuit[0].size = each_layer_size
        c.circuit[0].gates = [
            Gate(
                GateType.Input,
                0,
                self.domain(self._generate_random_point()),
                0,
                self.zero,
                False,
            )
            for _ in range(each_layer_size)
        ]

        # Initialize subsequent layers with half the gates of the previous layer
        for i in range(1, layer_num):
            current_layer_size = each_layer_size // (2**i)
            c.circuit[i].bitLength = int(math.log2(current_layer_size))
            c.circuit[i].size = current_layer_size
            c.circuit[i].gates = [
                Gate(
                    (
                        GateType.Add if j % 2 == 0 else GateType.Mul
                    ),  # Use Copy for a simple connection
                    i - 1,  # Connect to the previous layer
                    self._generate_random_point()
                    % c.circuit[
                        i - 1
                    ].size,  # Ensure connections wrap around if fewer gates
                    self._generate_random_point() % c.circuit[i - 1].size,
                    self.zero,
                    False,
                )
                for j in range(current_layer_size)
            ]
            last_gate = c.circuit[i].gates[-1]
            c.circuit[i].gates[-1] = Gate(
                GateType.Relay, last_gate.l, last_gate.u, 0, self.zero, False
            )

        return c

    def subsetInitTest(self):
        # Initialize the necessary attributes for each layer
        self.total_depth = self.size
        for i in range(self.size):
            self.circuit[i].dadBitLength = [-1] * i
            self.circuit[i].dadSize = [0] * i
            self.circuit[i].dadId = [[] for _ in range(i)]
            self.circuit[i].maxDadBitLength = -1
            self.circuit[i].maxDadSize = 0

        # Initialize visited and subset indices
        visited_idx = [[0 for _ in range(layer.size)] for layer in self.circuit]
        subset_idx = [[0 for _ in range(layer.size)] for layer in self.circuit]

        # Iterate over the layers in reverse order
        for i in reversed(range(1, self.size)):
            for j in reversed(range(self.circuit[i].size)):
                g = self.circuit[i].gates[j]
                l = g.l
                v = g.v
                if l == -1:  # Continue if l is -1
                    continue
                if visited_idx[l][v] != i:
                    visited_idx[l][v] = i
                    subset_idx[l][v] = self.circuit[i].dadSize[l]
                    self.circuit[i].dadId[l].append(v)
                    self.circuit[i].dadSize[l] += 1
                g.lv = subset_idx[l][v]

            # Update dadBitLength and max values
            for j in range(i):
                if self.circuit[i].dadSize[j] > 0:
                    self.circuit[i].dadBitLength[j] = math.ceil(
                        math.log2(self.circuit[i].dadSize[j])
                    )
                else:
                    self.circuit[i].dadBitLength[
                        j
                    ] = 0  # Set to 0 or an appropriate default when no connections

                # Update maximum dadBitLength and dadSize
                self.circuit[i].maxDadSize = max(
                    self.circuit[i].dadSize[j], self.circuit[i].maxDadSize
                )
                self.circuit[i].maxDadBitLength = max(
                    self.circuit[i].dadBitLength[j], self.circuit[i].maxDadBitLength
                )
