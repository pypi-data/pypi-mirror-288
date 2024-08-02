from typing import List, Union
from dohko.zkgrad.zkgrad.engine import Value


class CrossEntropyLoss:
    def __init__(self):
        pass

    def softmax(self, logits: List[Value]) -> List[Value]:
        # Exponentiate and normalize logits to get probabilities
        exp_logits = [x.exp() for x in logits]
        total = sum(exp_logits)
        probabilities = [x / total for x in exp_logits]
        return probabilities

    def __call__(self, logits: List[Value], target: Union[List[Value], List[int]]):
        # logits: list of Value objects from the last layer of the network
        # target: index of the correct class (assuming it's a single number)
        if len(target) and isinstance(target[0], Value):
            target = [t.data for t in target]
        # Apply softmax to logits
        probs = self.softmax(logits)

        # Calculate the cross-entropy loss
        loss = -probs[target.index(1)].log()
        return loss
