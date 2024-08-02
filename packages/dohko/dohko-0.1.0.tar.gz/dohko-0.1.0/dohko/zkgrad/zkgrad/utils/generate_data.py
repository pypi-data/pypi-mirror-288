import random
from dohko.zkgrad.zkgrad.engine import Value


def generate_synthetic_data(grid_size, depth, num_samples, num_classes):
    xs = []
    ys = []

    for _ in range(num_samples):
        # Generate a random grid of specified size and depth
        x = [
            [
                [Value(random.normalvariate(0, 10)) for _ in range(depth)]
                for _ in range(grid_size)
            ]
            for _ in range(grid_size)
        ]
        xs.append(x)

        # Simple relationship: y is the sum of all values in x
        y_true = random.randint(0, num_classes - 1)
        y = [Value(1) if i == y_true else Value(0) for i in range(num_classes)]
        ys.append(y)

    return xs, ys
