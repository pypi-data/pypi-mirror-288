import unittest
import tempfile
import os
from config.optimizer_config import OptimizerConfig
from network.activation_functions import Tanh, Relu, Sigmoid

class TestOptimizerConfig(unittest.TestCase):
    def setUp(self):
        # Create sample data for the test
        self.inputs = 10
        self.outputs = 5
        self.n_hidden = 2
        self.hidden_range = (10, 100)
        self.hidden_interval = 10
        self.batch_sizes = [32, 64, 128]
        self.learning_rates = [0.01, 0.001]
        self.activation_functions = [Tanh(), Relu()]
        self.epoachs = 20
        self.n_random = 5
        self.export_path = tempfile.mktemp()  # Use a temporary file for exporting

        self.config = OptimizerConfig(
            inputs=self.inputs,
            outputs=self.outputs,
            n_hidden=self.n_hidden,
            hidden_range=self.hidden_range,
            hidden_interval=self.hidden_interval,
            batch_sizes=self.batch_sizes,
            learning_rates=self.learning_rates,
            activation_functions=self.activation_functions,
            epoachs=self.epoachs,
            n_random=self.n_random,
            export_path=self.export_path
        )

    def test_export_config(self):
        # Export the configuration
        self.config.export_config()
        self.assertTrue(os.path.exists(self.export_path), "Export file does not exist.")

    def test_import_config(self):
        # Export and then import the configuration
        self.config.export_config()
        
        # Import the configuration
        imported_config = OptimizerConfig.import_config(self.export_path)
        
        # Check that the imported config is an instance of OptimizerConfig
        self.assertIsInstance(imported_config, OptimizerConfig)

        # Verify that the imported configuration matches the original
        self.assertEqual(imported_config.inputs, self.inputs)
        self.assertEqual(imported_config.outputs, self.outputs)
        self.assertEqual(imported_config.n_hidden, self.n_hidden)
        self.assertEqual(imported_config.hidden_range, self.hidden_range)
        self.assertEqual(imported_config.hidden_interval, self.hidden_interval)
        self.assertEqual(imported_config.batch_sizes, self.batch_sizes)
        self.assertEqual(imported_config.learning_rates, self.learning_rates)
        self.assertEqual(imported_config.epoachs, self.epoachs)
        self.assertEqual(imported_config.n_random, self.n_random)
        
        # Check activation functions
        for original_func, imported_func in zip(self.config.activation_functions, imported_config.activation_functions):
            self.assertIsInstance(imported_func, original_func.__class__)

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.export_path):
            os.remove(self.export_path)

if __name__ == '__main__':
    unittest.main()
