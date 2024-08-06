from network.network import Network
from config.network_config import NetworkConfig
from config.optimizer_config import OptimizerConfig
from optimization.optimizer import Optimizer
from optimization.optimization_tools import generate_struct
from optimization.optimization_tools import create_params
import numpy as np

class GridOptimizer(Optimizer):
    def __init__(self, config: OptimizerConfig):
        """
        Initialize the GridOptimizer object with the provided OptimizerConfig.

        Args:
        config (OptimizerConfig): A configuration object containing all the necessary parameters for the optimizer.

        Returns:
        None
        """
        self.super.__init__(config)
    
    def optimize(self, x_train: list[np.ndarray], y_train: list[np.ndarray]) -> tuple[Network, NetworkConfig]:
        """
        Optimizes the structure and parameters of a neural network using a grid search approach.

        Args:
        x_train (list[np.ndarray]): A list of input training data, where each element is a numpy array.
        y_train (list[np.ndarray]): A list of output training data, where each element is a numpy array.

        Returns:
        tuple[Network, NetworkConfig]: A tuple containing the optimized structure and parameters of the neural network as a Network object and a NetworkConfig object respectively.
        """
        structs = generate_struct(self.config)
        params = create_params(self.config)

        optimal_structure = structs[-1]
        optimal_parameters = params[-1]

        lowest_error = 1000

        for struct in structs:

            network = Network(struct, self.config.inputs, self.config.outputs)
            params, error = GridOptimizer.grid_optimizer(network, x_train, y_train, params, self.config.n_random)

            if error < lowest_error:
                lowest_error = error
                optimal_structure = network
                optimal_parameters = params
        return optimal_structure, optimal_parameters

    @staticmethod
    def grid_optimizer(network: Network, x_train: list[np.ndarray], y_train: list[np.ndarray], params: list[NetworkConfig], n_random_checks: int):
        """
        This function performs a grid search optimization of the neural network's parameters.

        Args:
        network (Network): A neural network object with a defined structure and parameters.
        x_train (list[np.ndarray]): A list of input training data, where each element is a numpy array.
        y_train (list[np.ndarray]): A list of output training data, where each element is a numpy array.
        params (list[NetworkConfig]): A list of possible parameter configurations for the neural network.
        n_random_checks (int): The number of random parameter configurations to check during the optimization process.

        Returns:
        tuple[dict, float]: A tuple containing the optimized parameters and the corresponding minimum error achieved during the optimization process.
        """
        lowest_error = 10000
        optimal_parameters = {}

        for param in params:
            error = network.train_from_config(param, x_train, y_train)[-1]

            if error < lowest_error:
                lowest_error = error
                optimal_parameters = param

        return optimal_parameters, lowest_error

