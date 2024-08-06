import unittest
import numpy as np
from network.layer import Layer
from network.dense import Dense

class TestDenseLayer(unittest.TestCase):

    def setUp(self):
        # Initialize the Dense layer with known weights and biases for testing
        self.input_size = 3
        self.output_size = 2
        self.dense_layer = Dense(self.input_size, self.output_size)
        
        # Manually set the weights and biases for predictable behavior
        self.dense_layer.weights = np.array([[0.2, 0.4, 0.6], [0.1, 0.3, 0.5]])
        self.dense_layer.bias = np.array([[0.5], [0.2]])
        
        # Define sample input and output gradient for testing
        self.input = np.array([[1.0], [2.0], [3.0]])
        self.output_gradient = np.array([[1.0], [1.0]])
        self.learning_rate = 0.01
        
        # Expected forward output
        self.expected_forward_output = np.dot(self.dense_layer.weights, self.input) + self.dense_layer.bias
        
        # Expected backward output
        self.expected_weights_gradient = np.dot(self.output_gradient, self.input.T)
        self.expected_input_gradient = np.dot(self.dense_layer.weights.T, self.output_gradient)

    def test_forward(self):
        # Test the forward pass
        forward_output = self.dense_layer.forward(self.input)
        np.testing.assert_array_almost_equal(forward_output, self.expected_forward_output, decimal=1, err_msg="Forward pass failed.")
    
    def test_backward(self):
        # Test the backward pass
        self.dense_layer.forward(self.input)  # Ensure input is set
        
        # Check weights update
        expected_updated_weights = self.dense_layer.weights - self.learning_rate * self.expected_weights_gradient
        backward_output = self.dense_layer.backward(self.output_gradient, self.learning_rate)
        np.testing.assert_array_almost_equal(self.dense_layer.weights, expected_updated_weights, decimal=2, err_msg="Weights update failed.")
        
        # Check biases update
        expected_updated_bias = self.dense_layer.bias - self.learning_rate * self.output_gradient
        np.testing.assert_array_almost_equal(self.dense_layer.bias, expected_updated_bias, decimal=2, err_msg="Bias update failed.")
        
        # Check backward output
        np.testing.assert_array_almost_equal(backward_output, self.expected_input_gradient, decimal=2, err_msg="Backward pass failed.")
    
if __name__ == '__main__':
    unittest.main()
