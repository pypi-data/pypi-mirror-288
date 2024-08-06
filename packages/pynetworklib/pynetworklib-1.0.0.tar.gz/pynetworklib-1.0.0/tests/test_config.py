import unittest
import tempfile
import os
import pickle
from config.config import Config

class TestConfig(unittest.TestCase):

    def test_export_and_import_config(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        # Define a sample config to export
        sample_config = {'learning_rate': 0.01, 'batch_size': 32}

        try:
            # Test export_config
            Config.export_config(sample_config, temp_path)
            
            # Ensure the file was created
            self.assertTrue(os.path.exists(temp_path))

            # Test import_config
            imported_config = Config.import_config(temp_path)

            # Ensure the imported config matches the original
            self.assertEqual(sample_config, imported_config)
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
