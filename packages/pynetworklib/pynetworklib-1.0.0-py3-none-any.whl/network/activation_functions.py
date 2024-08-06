from network.activation import Activation
import numpy as np

class Tanh(Activation):

    def __init__(self):
        """
        Initialize the Tanh activation function.

        Parameters:
        No parameters are required for initialization.

        Returns:
        This function does not return any value explicitly. It initializes the activation function for use in the neural network.

        The Tanh activation function is defined as:
            tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))

        The derivative (or the prime function) of the Tanh activation function is:
            tanh_prime(x) = 1 - tanh(x) ** 2

        This function is used to apply the Tanh activation function to the input values during the forward propagation phase in a neural network.
        """
        def tanh(x):
            return np.tanh(x)
        def tanh_prime(x):
            return 1-np.tanh(x) ** 2

        super().__init__(tanh, tanh_prime)

class Relu(Activation):

    def __init__(self):
        """
        Initialize the ReLU activation function.

        Parameters:
        No parameters are required for initialization.

        Returns:
        This function does not return any value explicitly. It initializes the activation function for use in the neural network.

        The ReLU activation function is defined as:
            relu(x) = max(0, x)

        The derivative (or the prime function) of the ReLU activation function is:
            relu_prime(x) = 1 if x > 0 else 0

        This function is used to apply the ReLU activation function to the input values during the forward propagation phase in a neural network.
        """
        def relu(x):
            return np.maximum(0, x)

        def relu_prime(x):
            return (x > 0) * 1

        super().__init__(relu, relu_prime)

class Sigmoid(Activation):

    def __init__(self):
        """
        Initialize the Sigmoid activation function.
    
        Parameters:
        No parameters are required for initialization.
    
        Returns:
        This function does not return any value explicitly. It initializes the activation function for use in the neural network.
    
        The Sigmoid activation function is defined as:
            sigmoid(x) = 1 / (1 + e^(-x))
    
        The derivative (or the prime function) of the Sigmoid activation function is:
            sigmoid_prime(x) = sigmoid(x) * (1 - sigmoid(x))
    
        This function is used to apply the Sigmoid activation function to the input values during the forward propagation phase in a neural network.
        """
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))
        
        def sigmoid_prime(x):
            s = sigmoid(x)
            return s * (1 - s)
        
        super().__init__(sigmoid, sigmoid_prime)