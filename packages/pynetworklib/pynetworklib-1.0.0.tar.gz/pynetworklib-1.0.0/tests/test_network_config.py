import unittest
import tempfile
import os
from config.network_config import NetworkConfig
from network.activation_functions import Tanh, Relu, Sigmoid

class TestNetworkConfig(unittest.TestCase):

    def test_export_and_import_config(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        # Create a NetworkConfig instance
        config = NetworkConfig(
            loss="some_loss",
            epoachs=10,
            batch_size=32,
            learning_rate=0.001,
            activation=Tanh(),  # Use the activation instance directly
            verbose=True,
            one_hot=True,
            export_path=temp_path
        )

        try:
            # Export the config
            config.export_config()

            # Ensure the file was created
            self.assertTrue(os.path.exists(temp_path))

            # Import the config back
            imported_config = NetworkConfig.import_config(temp_path)

            # Ensure the imported configuration matches the original
            self.assertEqual(config.loss, imported_config.loss)
            self.assertEqual(config.epoachs, imported_config.epoachs)
            self.assertEqual(config.batch_size, imported_config.batch_size)
            self.assertEqual(config.learning_rate, imported_config.learning_rate)
            self.assertEqual(config.verbose, imported_config.verbose)
            self.assertEqual(config.one_hot, imported_config.one_hot)
            self.assertEqual(config.export_path, imported_config.export_path)
            # Compare the activation function instances
            self.assertEqual(config.activation.__class__.__name__, imported_config.activation.__class__.__name__)
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
