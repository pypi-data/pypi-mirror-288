from network.layer import Layer
import numpy as np

class Dense(Layer):
    def __init__(
        self,
        input_size: int,  # The number of input features for the dense layer.
        output_size: int  # The number of output features for the dense layer.
    ):
        """
        Initialize a dense layer with given input and output sizes.

        Args:
        input_size (int): The number of input features for the dense layer.
        output_size (int): The number of output features for the dense layer.

        Attributes:
        inputs (int): The number of input features for the dense layer.
        outputs (int): The number of output features for the dense layer.
        weights (numpy.ndarray): A 2D array of random weights initialized for the dense layer.
        bias (numpy.ndarray): A 2D array of random biases initialized for the dense layer.
        """
        super().__init__()
        self.inputs = input_size
        self.outputs = output_size
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)
    def forward(self, input: np.ndarray) -> np.ndarray:
        """
        Perform a forward pass through the dense layer.

        Args:
        input (np.ndarray): A 2D array of input features for the dense layer.

        Returns:
        np.ndarray: A 2D array of output features obtained after applying the dense layer's weights and biases.
        """
        self.input = input
        return np.dot(self.weights, self.input) + self.bias
    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """
        Perform a backward pass through the dense layer to compute the gradients.
    
        Args:
        output_gradient (np.ndarray): A 2D array of gradients of the loss function with respect to the output features.
        learning_rate (float): The learning rate for updating the weights and biases.
    
        Returns:
        np.ndarray: A 2D array of gradients of the loss function with respect to the input features.
    
        The function computes the gradients of the loss function with respect to the input features by applying the chain rule of differentiation. It first calculates the gradients of the loss function with respect to the weights and biases using the provided output_gradient. Then, it updates the weights and biases using the learning_rate and the computed gradients. Finally, it computes the gradients of the loss function with respect to the input features using the chain rule.
        """
        weights_gradient = np.dot(output_gradient, self.input.T)
        input_gradients = np.dot(self.weights.T, output_gradient)
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return input_gradients
    