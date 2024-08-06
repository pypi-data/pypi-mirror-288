from network.loss import Loss
import numpy as np

class MeanSquaredError(Loss):
    """
    Mean Squared Error (MSE) loss function.

    This class implements the Mean Squared Error loss function, which is commonly used in regression tasks.

    Args:
    y_true (numpy.ndarray): The true or target values.
    y_pred (numpy.ndarray): The predicted values.

    Returns:
    float: The mean squared error between the true and predicted values.

    Example:
    >>> from network.loss import MeanSquaredError
    >>> y_true = np.array([1, 2, 3])
    >>> y_pred = np.array([0.5, 1.5, 2.5])
    >>> mse = MeanSquaredError.loss(y_true, y_pred)
    >>> print(mse)
    0.375
    """

    @staticmethod
    def loss(y_true, y_pred):
        """
        Calculate the Mean Squared Error loss.

        Args:
        y_true (numpy.ndarray): The true or target values.
        y_pred (numpy.ndarray): The predicted values.

        Returns:
        float: The mean squared error between the true and predicted values.
        """
        return np.mean(np.power(y_true-y_pred, 2))
    @staticmethod

    def loss_prime(y_true, y_pred):
        """
        Compute the derivative of the Mean Squared Error loss function with respect to the predicted values.

        Args:
        y_true (numpy.ndarray): The true or target values.
        y_pred (numpy.ndarray): The predicted values.

        Returns:
        numpy.ndarray: The derivative of the Mean Squared Error loss function with respect to the predicted values.

        This function computes the derivative of the Mean Squared Error loss function with respect to the predicted values. The derivative is used in gradient-based optimization algorithms to update the model parameters. The derivative is given by the formula:

        derivative = 2 * (y_pred - y_true) / np.size(y_true)

        Example:
        >>> from network.loss import MeanSquaredError
        >>> y_true = np.array([1, 2, 3])
        >>> y_pred = np.array([0.5, 1.5, 2.5])
        >>> loss_prime = MeanSquaredError.loss_prime(y_true, y_pred)
        >>> print(loss_prime)
        [ 1.5  1.5  1.5]
        """
        return 2 * (y_pred - y_true) / np.size(y_true)
