class Layer:
    """
    A base class for layers in a neural network.

    Attributes:
        input (Tensor): The input tensor for the layer.
        output (Tensor): The output tensor for the layer.

    Methods:
        forward(input): Forward pass through the layer.
        backward(output_gradient, learning_rate): Backward pass through the layer.

    """

    def __init__(self):
        """
        Initialize a new layer.

        Args:
            None

        Returns:
            None

        """
        self.input = None
        self.output = None
    def forward(self, input):
        """
        Perform the forward pass through the layer.

        Args:
            input (Tensor): The input tensor for the layer.

        Returns:
            Tensor: The output tensor for the layer after the forward pass.

        Raises:
            ValueError: If the input tensor is not provided.

        """
        if input is None:
            raise ValueError("Input tensor must be provided for the forward pass.")
        # Perform the forward pass through the layer using the input tensor.
        # Update the output tensor based on the forward pass.
        # Return the output tensor.
    def backward(self, output_gradient, learning_rate):
        """
        Perform the backward pass through the layer.

        Args:
            output_gradient (Tensor): The gradient of the output tensor with respect to the layer's output.
            learning_rate (float): The learning rate for updating the layer's weights.

        Returns:
            None: The backward pass updates the layer's weights and does not return a value.

        Raises:
            ValueError: If the output gradient tensor is not provided.

        """
        if output_gradient is None:
            raise ValueError("Output gradient tensor must be provided for the backward pass.")
        # Perform the backward pass through the layer using the output gradient tensor.
        # Update the layer's weights based on the backward pass.
        # The backward pass does not return a value, but updates the layer's weights.