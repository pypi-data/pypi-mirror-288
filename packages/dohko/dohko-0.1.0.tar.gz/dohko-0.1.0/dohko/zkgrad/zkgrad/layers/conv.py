import random
from dohko.zkgrad.zkgrad.engine import Value


class Convolutional2DLayer:
    def __init__(self, num_filters, filter_size, input_depth):
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.filters = [
            [
                Value(random.uniform(-1, 1))
                for _ in range(filter_size * filter_size * input_depth)
            ]
            for _ in range(num_filters)
        ]

    def __call__(self, input_volume):
        input_height, input_width = len(input_volume), len(input_volume[0])

        output_height = input_height - self.filter_size + 1
        output_width = input_width - self.filter_size + 1

        # Initialize the output volume with zeros
        output_volume = [
            [Value(0) for _ in range(output_width)] for _ in range(output_height)
        ]

        # Apply each filter to the input_volume
        for i in range(output_height):
            for j in range(output_width):
                # Extract the region of the input volume that the current filter will be applied to
                region = [
                    input_volume[i + di][j + dj]
                    for di in range(self.filter_size)
                    for dj in range(self.filter_size)
                ]

                # Apply the filter
                for f in range(self.num_filters):
                    filter_values = self.filters[f]
                    output_volume[i][j] += sum(
                        rv * fv for rv, fv in zip(region, filter_values)
                    )

        return output_volume

    def parameters(self):
        # Flatten the filters for the optimizer
        return [p for filter in self.filters for p in filter]
