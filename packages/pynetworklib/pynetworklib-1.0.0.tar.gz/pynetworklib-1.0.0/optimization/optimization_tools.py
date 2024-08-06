import itertools
from ..config.optimizer_config import OptimizerConfig
from ..config.network_config import NetworkConfig
from ..network.activation_functions import *
from ..network.dense import Dense
from ..network.layer import Layer
from ..network.mse import MeanSquaredError

def generate_struct(config: OptimizerConfig) -> list[list[Layer]]:

    # Generate all possible sizes for hidden layers

    min_layer_size, max_layer_size = config.hidden_range
    hidden_layer_sizes = list(range(min_layer_size, max_layer_size + 1, config.hidden_interval))
    # Generate all combinations of hidden layer sizes with length n_layers
    layer_combinations = list(itertools.product(hidden_layer_sizes, repeat=config.n_hidden))
    structures = []
    for combo in layer_combinations:
        structure = []
        prev_size = config.inputs
        # Create layers and add to structure
        for size in combo:
            structure.append(Dense(prev_size, size))
            structure.append(Sigmoid())
            prev_size = size
        # Add the output layer
        structure.append(Dense(prev_size, config.outputs))
        structure.append(Sigmoid())
        structures.append(structure)
    return structures

def create_params(config: OptimizerConfig) -> list[NetworkConfig]:
    param_list=[]
    for rate in config.learning_rates:
        for activ in config.activation_functions:
            for batch in config.batch_sizes:
                param_list.append(NetworkConfig(MeanSquaredError(), config.epoachs, batch, rate, activ, config.verbose))
    return param_list