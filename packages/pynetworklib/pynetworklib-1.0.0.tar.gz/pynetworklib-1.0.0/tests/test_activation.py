import unittest
import numpy as np
from network.activation import Activation

class TestActivation(Activation):
    def __init__(self, activation, activation_prime):
        super().__init__(activation, activation_prime)

class TestActivationClass(unittest.TestCase):
    
    def setUp(self):
        # Define the ReLU activation function and its derivative
        def relu(x):
            return np.maximum(0, x)
        
        def relu_prime(x):
            return (x > 0)
        
        # Create an instance of the Activation class using the ReLU functions
        self.activation_layer = TestActivation(relu, relu_prime)
        
        # Define sample input and gradient for testing
        self.x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
        self.output_gradient = np.array([1.0, 1.0, 1.0, 1.0, 1.0]).astype(float)
        self.learning_rate = 0.01  # Example learning rate (not used in calculations)
        
        # Expected values
        self.expected_forward = np.maximum(0, self.x)
        self.expected_backward = self.output_gradient * (self.x > 0)
    
    def test_forward_and_backward(self):
        
        # Test the forward pass
        result = self.activation_layer.forward(self.x)
        np.testing.assert_array_equal(result, self.expected_forward, err_msg="Forward pass failed.")

        # Test the backward pass
        result = self.activation_layer.backward(self.output_gradient, self.learning_rate)
        np.testing.assert_array_equal(result, self.expected_backward, err_msg="Backward pass failed.")

    
if __name__ == '__main__':
    unittest.main()
