import unittest
import numpy as np
from network.mse import MeanSquaredError

class TestMeanSquaredError(unittest.TestCase):

    def setUp(self):
        # Define sample true and predicted values
        self.y_true = np.array([1, 2, 3])
        self.y_pred = np.array([0.5, 1.5, 2.5])
        
        # Expected values
        self.expected_loss = 0.375
        self.expected_loss_prime = np.array([-0.33333333, -0.33333333, -0.33333333])

    def test_loss(self):
        # Test the Mean Squared Error loss calculation
        mse_loss = MeanSquaredError.loss(self.y_true, self.y_pred)
        self.assertAlmostEqual(mse_loss, self.expected_loss, places=6, msg="Mean Squared Error loss calculation failed.")

    def test_loss_prime(self):
        # Test the derivative of the Mean Squared Error loss function
        mse_loss_prime = MeanSquaredError.loss_prime(self.y_true, self.y_pred)
        np.testing.assert_array_almost_equal(mse_loss_prime, self.expected_loss_prime, decimal=6, err_msg="Derivative of Mean Squared Error loss function calculation failed.")

    def test_high_loss_with_significant_difference():
        # Arrange
        y_true = np.array([1, 2, 3])
        y_pred = np.array([4, 5, 6])

        # Act
        loss = MeanSquaredError.loss(y_true, y_pred)

        # Assert
        assert loss > 3.5, "Loss should be high when predicted values are significantly different from true values"

    def test_loss_low_value_when_predicted_values_closely_match_true_values():
        # Create true and predicted values arrays with closely matching values
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.1, 3.1])

        # Calculate the loss using the selected code
        loss = MeanSquaredError.loss(y_true, y_pred)

        # Assert that the loss is low
        assert loss < 1.0, f"Expected a low loss value, but got {loss}"

if __name__ == '__main__':
    unittest.main()
