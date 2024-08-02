def one_hot_encode(label, num_classes):
    """One-hot encodes a single label."""
    return [1 if i == label else 0 for i in range(num_classes)]


def one_hot_encode_iris(labels, num_classes):
    """One-hot encodes a single label."""
