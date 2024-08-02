from dohko.zkgrad.zkgrad.examples.mlp import MLP
from dohko.zkgrad.zkgrad.layers.conv import Convolutional2DLayer


class ConvMLP:
    def __init__(
        self,
        input_depth,
        num_classes,
        mlp_hidden_dim,
        conv_num_filters,
        conv_filter_size=3,
    ):
        self.conv_layer = Convolutional2DLayer(
            conv_num_filters, conv_filter_size, input_depth
        )
        self.mlp = MLP(mlp_hidden_dim, [num_classes])

    def __call__(self, input_volume):
        conv_output = self.conv_layer(input_volume)
        flattened_conv_output = [x for row in conv_output for x in row]
        return self.mlp(flattened_conv_output)

    def parameters(self):
        return self.mlp.parameters() + self.conv_layer.parameters()
