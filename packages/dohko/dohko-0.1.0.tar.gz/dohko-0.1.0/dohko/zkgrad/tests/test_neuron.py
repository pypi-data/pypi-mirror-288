from sklearn.datasets import load_iris, load_digits
from dohko.zkgrad.zkgrad.engine import Value
from dohko.zkgrad.zkgrad.examples.mlp import MLP
from dohko.zkgrad.zkgrad.layers.dense import DenseLayer
from dohko.zkgrad.zkgrad.layers.neuron import Neuron
from dohko.zkgrad.zkgrad.loss.cross_entropy import CrossEntropyLoss
from dohko.zkgrad.zkgrad.utils.hot_encode import one_hot_encode
from dohko.zkgrad.zkgrad.utils.visualize import draw_dot
from dohko.prover.prover import ZkProver
from dohko.zkgrad.zkgrad.utils.visualize import draw_dot

DIGITS_DATASET = load_digits()

IRIS_DATASET = load_iris()


def test_neuron_fires():
    n = Neuron(2)
    x = [Value(1), Value(2)]
    y = n(x)
    assert abs(y.data) > 0
    assert y.grad == 0
    y.backward()
    assert y.grad != 0
    for w in n.weights:
        assert w.grad != 0
    assert n.bias.grad != 0


def test_layer_activation():
    l = DenseLayer(2, 3)
    x = [Value(1), Value(2)]
    y = l(x)
    assert len(y) == 3
    for y_ in y:
        assert abs(y_.data) > 0
        assert y_.grad == 0
    [y_.backward() for y_ in y]
    for y_ in y:
        assert y_.grad != 0
    for n in l.neurons:
        for w in n.weights:
            assert w.grad != 0
        assert n.bias.grad != 0


def test_mlp_activation():
    mlp = MLP(3, [3, 4, 1])
    x = [Value(1), Value(2), Value(3)]
    y = mlp(x)
    assert len(y) == 1
    for y_ in y:
        assert abs(y_.data) > 0
        assert y_.grad == 0
    [y_.backward() for y_ in y]
    for y_ in y:
        assert y_.grad != 0
    for layer in mlp.layers:
        for n in layer.neurons:
            for w in n.weights:
                assert w.grad != 0
            assert n.bias.grad != 0


def load_iris_dataset_classification():
    X = IRIS_DATASET.data
    y = IRIS_DATASET.target
    return X, y


def test_iris_dataset_classification():
    dataset = load_iris_dataset_classification()
    X, y = dataset
    num_classes = len(set(y))
    y = list(map(lambda x: one_hot_encode(x, num_classes), y))
    mlp_hidden_dim = 50
    model = MLP(X.shape[1], [mlp_hidden_dim, num_classes])
    # learning_rate = 0.01
    # loss_function = CrossEntropyLoss()
    # for epoch in range(1):
    #     total_loss = 0
    #     for i in range(0, len(X)):
    #         x = X[i]
    #         y_true = y[i]
    #         y_pred = model(x)
    #         loss = loss_function(y_pred, y_true)
    #         total_loss += loss.data
    #         for p in model.parameters():
    #             p.grad = 0
    #         loss.backward()
    #         for param in model.parameters():
    #             param.data -= learning_rate * param.grad
    #     if epoch % 2 == 0:
    #         print(f"Epoch {epoch}, Loss: {total_loss}")
    y_pred = model(X[0])
    # draw_dot(y_pred[0]).render(
    #     filename="dohko/zkgrad/tests/assets/iris_mlp_dag", format="png", cleanup=True
    # )
    # draw_dot(loss).render(
    #     filename="dohko/zkgrad/tests/assets/iris_mlp_backpropagation_dag",
    #     format="png",
    #     cleanup=True,
    # )
    output = y_pred[0]
    for o in y_pred[1:]:
        output = output + o
    draw_dot(output).render(
        filename="dohko/zkgrad/tests/assets/iris_mlp_dag", format="png", cleanup=True
    )
    circuit, _, value_circuit = Value.compile_layered_circuit(output, True)
    # vc = value_circuit  # [0:10]
    # for i in vc[5]:
    #     i._prev = []
    print(circuit)
    assert ZkProver(circuit).prove()


def prepare_data(X, y, num_classes):
    X_prepared = [[[Value(pixel) for pixel in row] for row in image] for image in X]
    y_prepared = [one_hot_encode(label, num_classes=num_classes) for label in y]
    return X_prepared, y_prepared
