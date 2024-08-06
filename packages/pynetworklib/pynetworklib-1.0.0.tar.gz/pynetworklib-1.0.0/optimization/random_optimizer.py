from network.network import Network
from config.network_config import NetworkConfig
from config.optimizer_config import OptimizerConfig
from optimization.optimizer import Optimizer
from optimization.optimization_tools import generate_struct
from optimization.optimization_tools import create_params
from random import randint
import numpy as np


class RandomOptimizer(Optimizer):
    def __init__(self, config: OptimizerConfig):
        """
        Initializes the RandomOptimizer object with the provided OptimizerConfig.

        Args:
        config (OptimizerConfig): A configuration object containing all the necessary parameters for the optimizer.

        Returns:
        None
        """
        super().__init__(config)    
    def optimize(self, x_train: list[np.ndarray], y_train: list[np.ndarray]) -> tuple[Network, NetworkConfig]:
        """
        Optimizes the neural network structure and parameters using a random search approach.

        Args:
        x_train (list[np.ndarray]): List of input training data.
        y_train (list[np.ndarray]): List of output training data.

        Returns:
        tuple[Network, NetworkConfig]: A tuple containing the optimized neural network structure and its corresponding configuration.
        """
        structs = generate_struct(self.config)
        params = create_params(self.config)

        optimal_structure = structs[-1]
        optimal_parameters = params[-1]

        lowest_error = 1000

        for struct in structs:

            network = Network(struct, self.config.inputs, self.config.outputs)
            params, error = RandomOptimizer.random_optimizer(network, x_train, y_train, params, self.config.n_random)

            if error < lowest_error:
                lowest_error = error
                optimal_structure = network
                optimal_parameters = params
        return optimal_structure, optimal_parameters

    @staticmethod
    def random_optimizer(network: Network, x_train: list, y_train: list, params: list[NetworkConfig], n_random_checks: int):
        """
        This function performs a random search for the optimal parameters of a neural network.

        Args:
        network (Network): A neural network object with a defined structure and configuration.
        x_train (list): A list of input training data.
        y_train (list): A list of output training data.
        params (list[NetworkConfig]): A list of candidate parameter configurations for the neural network.
        n_random_checks (int): The number of random parameter configurations to evaluate.

        Returns:
        tuple[float, list[NetworkConfig]]: A tuple containing the lowest error achieved during the random search and the optimal parameter configuration that resulted in this error.
        """
        lowest_error = 10000
        for n in range(0, n_random_checks):

            n_param = len(params)
            param = params.pop(randint(0, n_param-1))

            error = network.train_from_config(param, x_train, y_train)[-1]

            if error < lowest_error:
                lowest_error = error
                optimal_parameters = param

        return optimal_parameters[1], lowest_error