from network.layer import Layer
import numpy as np

class Softmax(Layer):
    def forward(self, input):
        """
        This function applies the softmax activation function to the input array.

        Parameters:
        input (np.ndarray): A 1D numpy array of real numbers representing the input to the softmax function.

        Returns:
        np.ndarray: A 1D numpy array of real numbers between 0 and 1, representing the output of the softmax function.
        """
        tmp = np.exp(input)
        self.output = tmp / np.sum(tmp)
        return self.output
    def backward(self, output_gradient, learning_rate):
        """
        This function computes the gradient of the softmax layer's loss with respect to the input.
    
        Parameters:
        output_gradient (np.ndarray): A 1D numpy array of real numbers representing the gradient of the loss with respect to the output of the softmax layer.
        learning_rate (float): A scalar value representing the learning rate for the gradient descent optimization algorithm.
    
        Returns:
        np.ndarray: A 1D numpy array of real numbers representing the gradient of the loss with respect to the input of the softmax layer.
        """
        n = np.size(self.output)
        return np.dot((np.identity(n) - self.output.T) * self.output, output_gradient)
