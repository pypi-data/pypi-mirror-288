import numpy as np
from network.network import *
from config.network_config import NetworkConfig
from config.optimizer_config import OptimizerConfig

class Optimizer:
    def __init__(self,config: OptimizerConfig):
        """
        Initialize the Optimizer object with the provided configuration.

        Args:
            config (OptimizerConfig): A configuration object containing details about the optimizer to be used.

        Attributes:
            config (OptimizerConfig): The configuration object used to initialize the optimizer.
        """
        self.config = config
    
    def optimize(self, x_train: list[np.ndarray], y_train: list[np.ndarray]) -> tuple[Network, NetworkConfig]:
        """
        Optimize the provided neural network using the specified optimizer configuration.
    
        Args:
            x_train (list[np.ndarray]): A list of input training data, where each element is a numpy array representing the input data for a single training example.
            y_train (list[np.ndarray]): A list of output training data, where each element is a numpy array representing the output data for a single training example.
    
        Returns:
            tuple[Network, NetworkConfig]: A tuple containing the optimized neural network and its corresponding configuration.
        """
        pass


