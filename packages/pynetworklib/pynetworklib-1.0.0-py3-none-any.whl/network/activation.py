from network.layer import Layer
import numpy as np

class Activation(Layer):
    """
    This class represents an activation layer in a neural network.

    Parameters:
    - activation (function): The activation function to be applied to the input.
    - activation_prime (function): The derivative of the activation function.

    Attributes:
    - activation (function): The activation function.
    - activation_prime (function): The derivative of the activation function.

    Methods:
    - forward(input): Applies the activation function to the input and returns the result.
    - backward(output_gradient, learning_rate): Computes the gradient of the loss function with respect to the input and returns it.
    """

    def __init__(self, activation, activation_prime):
        """
        Initializes an instance of the Activation class.

        Parameters:
        - activation (function): The activation function to be applied to the input.
        - activation_prime (function): The derivative of the activation function.

        Attributes:
        - activation (function): The activation function.
        - activation_prime (function): The derivative of the activation function.
        """
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input):
        """
        Applies the activation function to the input and returns the result.

        Parameters:
        - input (numpy.ndarray): The input data to be processed by the activation layer.

        Returns:
        - output (numpy.ndarray): The result of applying the activation function to the input data.
        """
        self.input = input
        return self.activation(self.input)

    def backward(self, output_gradient, learning_rate):
        """
        Computes the gradient of the loss function with respect to the input and returns it.
    
        Parameters:
        - output_gradient (numpy.ndarray): The gradient of the loss function with respect to the output of the activation layer.
        - learning_rate (float): The learning rate used for updating the weights in the neural network.
    
        Returns:
        - input_gradient (numpy.ndarray): The gradient of the loss function with respect to the input of the activation layer.
        """
        return np.multiply(output_gradient, self.activation_prime(self.input))