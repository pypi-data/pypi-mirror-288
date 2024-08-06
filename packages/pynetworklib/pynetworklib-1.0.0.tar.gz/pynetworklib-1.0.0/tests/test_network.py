import unittest
import numpy as np
from network.dense import Dense
from network.activation import Activation
from network.mse import MeanSquaredError
from network.activation_functions import Tanh
from network.layer import Layer
from network.network import Network

class TestNetwork(unittest.TestCase):
    
    def setUp(self):
        np.random.seed(0)  # Set the seed for reproducibility
        self.dense_layer = Dense(3, 2)
        self.activation_layer = Tanh()
        self.network_layers = [self.dense_layer, self.activation_layer]
        self.inputs = 3
        self.outputs = 2
        self.network = Network(self.network_layers, self.inputs, self.outputs)
        self.loss = MeanSquaredError()

        # Sample training data
        self.x_train = [np.random.rand(self.inputs) for _ in range(10)]
        self.y_train = [np.random.rand(self.outputs) for _ in range(10)]

    
    def test_network_initialization_with_valid_arguments(self):
        try:
            network = Network(self.network_layers, self.inputs, self.outputs)
        except TypeError:
            self.fail("Network initialization failed with valid arguments")

    def test_network_initialization_with_invalid_network(self):
        with self.assertRaises(TypeError):
            Network("invalid_network", self.inputs, self.outputs)
    
    def test_network_initialization_with_invalid_inputs(self):
        with self.assertRaises(TypeError):
            Network(self.network_layers, "invalid_inputs", self.outputs)
    
    def test_network_initialization_with_invalid_outputs(self):
        with self.assertRaises(TypeError):
            Network(self.network_layers, self.inputs, "invalid_outputs")
    
    def test_predict(self):
        network = Network(self.network_layers, self.inputs, self.outputs)
        sample_input = np.array([1.0, 2.0, 3.0])
        try:
            network.predict(sample_input)
        except Exception as e:
            self.fail(f"Network predict method raised an exception: {e}")
    def test_fit_method(self):
        epochs = 10
        batch_size = 2
        learning_rate = 0.01
        verbose = False
        one_hot = False

        # Before training, save the initial weights and biases
        initial_weights = [layer.weights.copy() for layer in self.network.network if isinstance(layer, Dense)]
        initial_biases = [layer.bias.copy() for layer in self.network.network if isinstance(layer, Dense)]

        errors = self.network._fit(self.loss, self.x_train, self.y_train, epochs, batch_size, learning_rate, one_hot, verbose)

        # Check if errors list is of the correct length
        self.assertEqual(len(errors), epochs, "Length of errors list should be equal to number of epochs")

        # Check if the weights and biases have been updated
        updated_weights = [layer.weights for layer in self.network.network if isinstance(layer, Dense)]
        updated_biases = [layer.bias for layer in self.network.network if isinstance(layer, Dense)]

        for initial, updated in zip(initial_weights, updated_weights):
            self.assertFalse(np.array_equal(initial, updated), "Weights should have been updated after training")

        for initial, updated in zip(initial_biases, updated_biases):
            self.assertFalse(np.array_equal(initial, updated), "Biases should have been updated after training")

    def test_fit_method_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.network._fit(self.loss, [], self.y_train)  # Empty x_train
        
        with self.assertRaises(ValueError):
            self.network._fit(self.loss, self.x_train, [])  # Empty y_train
        
        with self.assertRaises(ValueError):
            self.network._fit(self.loss, self.x_train, self.y_train, epoachs=-1)  # Invalid epochs
        
        with self.assertRaises(ValueError):
            self.network._fit(self.loss, self.x_train, self.y_train, batch_size=0)  # Invalid batch_size

if __name__ == '__main__':
    unittest.main()
