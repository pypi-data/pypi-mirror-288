# zkGrad: A Simple Neural Network Framework with Autograd

## Introduction

zkGrad is a minimalist neural network framework designed for educational purposes. It focuses on the core concepts of automatic differentiation (autograd) and backpropagation, making it an excellent tool for learning and experimentation. zkGrad is particularly suitable for those looking to understand the internals of neural network operations and autograd mechanisms.

## Features

Automatic Differentiation (Autograd): At the heart of zkGrad is an autograd system that automatically computes gradients for node operations. This feature simplifies the implementation of backpropagation, allowing users to focus on designing and training neural networks without worrying about the complex underlying calculus.

- Dense Layers: zkGrad comes with fully implemented dense layers (also known as fully connected layers). These layers are fundamental building blocks of many neural networks, suitable for a wide range of applications from simple regression to complex classification tasks.

- Convolutional 2D Layers: In addition to dense layers, zkGrad offers 2D convolutional layers out of the box. These layers are crucial for tasks involving spatial data, such as image and video recognition, making zkGrad suitable for experimenting with convolutional neural networks (CNNs).

## Getting Started

### Prerequisites

- Python 3.10

## Basic Usage

Here's a quick example of how to use zkGrad to create a simple neural network:

```python
from dohko.zkgrad.zkgrad.engine import Value
from dohko.zkgrad.zkgrad.layers import DenseLayer, ConvolutionalLayer
from dohko.zkgrad.zkgrad.model import NeuralNetwork

from sklearn.datasets import load_iris
from dohko.zkgrad.zkgrad.examples.mlp import MLP
from dohko.zkgrad.zkgrad.loss.cross_entropy import CrossEntropyLoss

from dohko.zkgrad.zkgrad.utils.hot_encode import one_hot_encode


IRIS_DATASET = load_iris()


def load_iris_dataset_classification():
    X = IRIS_DATASET.data
    y = IRIS_DATASET.target
    return X, y


dataset = load_iris_dataset_classification()

X, y = dataset
num_classes = len(set(y))
y = list(map(lambda x: one_hot_encode(x, num_classes), y))
mlp_hidden_dim = 50
model = MLP(X.shape[1], [mlp_hidden_dim, num_classes])
learning_rate = 0.01
loss_function = CrossEntropyLoss()
for epoch in range(10):
    total_loss = 0
    for i in range(0, len(X)):
        x = X[i]
        y_true = y[i]
        y_pred = model(x)
        loss = loss_function(y_pred, y_true)
        total_loss += loss.data
        for p in model.parameters():
            p.grad = 0
        loss.backward()
        for param in model.parameters():
            param.data -= learning_rate * param.grad
    if epoch % 2 == 0:
        print(f"Epoch {epoch}, Loss: {total_loss}")

```

## Contributing

Contributions to zkGrad are welcome! Whether it's improving the documentation, adding new features, or reporting issues, all contributions are appreciated.

## License

zkGrad is open source and is available under the MIT License.
