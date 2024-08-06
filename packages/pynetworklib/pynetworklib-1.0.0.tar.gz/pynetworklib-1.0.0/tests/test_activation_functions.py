import unittest
import numpy as np
from network.activation_functions import Tanh, Relu, Sigmoid

class TestActivationFunctions(unittest.TestCase):
    
    def test_tanh(self):
        tanh = Tanh()
        x = np.array([-2, -1, 0, 1, 2])
        
        # Test forward pass
        expected_output = np.tanh(x)
        np.testing.assert_array_almost_equal(tanh.forward(x), expected_output)
        
        # Test backward pass
        output_gradient = np.ones_like(x)
        expected_prime_output = output_gradient * (1 - np.tanh(x) ** 2)
        np.testing.assert_array_almost_equal(tanh.backward(output_gradient, None), expected_prime_output)

    def test_relu(self):
        relu = Relu()
        x = np.array([-2, -1, 0, 1, 2])
        
        # Test forward pass
        expected_output = np.maximum(0, x)
        np.testing.assert_array_equal(relu.forward(x), expected_output)
        
        # Test backward pass
        output_gradient = np.ones_like(x)
        expected_prime_output = output_gradient * (x > 0).astype(int)
        np.testing.assert_array_equal(relu.backward(output_gradient, None), expected_prime_output)

    def test_sigmoid(self):
        sigmoid = Sigmoid()
        x = np.array([-2, -1, 0, 1, 2])
        
        # Test forward pass
        expected_output = 1 / (1 + np.exp(-x))
        np.testing.assert_array_almost_equal(sigmoid.forward(x), expected_output)
        
        # Test backward pass
        output_gradient = np.ones_like(x)
        s = 1 / (1 + np.exp(-x))
        expected_prime_output = output_gradient * (s * (1 - s))
        np.testing.assert_array_almost_equal(sigmoid.backward(output_gradient, None), expected_prime_output)

if __name__ == '__main__':
    unittest.main()
