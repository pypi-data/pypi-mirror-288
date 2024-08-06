from config.config import Config
from network.activation_functions import Tanh, Relu, Sigmoid
from network.activation import Activation

class OptimizerConfig(Config):
    
    def __init__(
                self, 
                inputs: int,
                outputs: int,
                n_hidden: int, 
                hidden_range: tuple[int, int],
                hidden_interval: int,
                batch_sizes: list[int],
                learning_rates: list[float],
                activation_functions: list[Activation],
                epoachs: int,
                n_random: int,
                verbose=False,
                export_path=None
                ):
        """
        This class represents the configuration for an optimizer used in a neural network.

        Parameters:
            inputs (int): The number of inputs in the dataset.
            outputs (int): The number of outputs in the dataset.
            n_hidden (int): The number of hidden layers in the neural network.
            hidden_range (tuple[int, int]): A tuple representing the range of possible number of neurons in each hidden layer.
            hidden_interval (int): The interval between sizes in the hidden range.
            batch_sizes (list[int]): A list of possible batch sizes for training the neural network.
            learning_rates (list[float]): A list of possible learning rates for the optimizer.
            activation_functions (list[Activation]): A list of activation functions to be used in the neural network.
            epoachs (int): The number of epochs to train the neural network.
            n_random (int): The number of random configurations to generate.
            verbose (bool, optional): A boolean flag indicating whether to print training progress. Defaults to False.
            export_path (str, optional): The path to export the configuration to a file. Defaults to None.

        Returns:
            None: This method does not return any value. It initializes the OptimizerConfig object with the provided parameters.
        """
        self.inputs = inputs
        self.outputs = outputs
        self.n_hidden = n_hidden
        self.hidden_range = hidden_range
        self.hidden_interval = hidden_interval
        self.batch_sizes = batch_sizes
        self.learning_rates = learning_rates
        self.activation_functions = activation_functions
        self.epoachs = epoachs
        self.n_random = n_random
        self.verbose = verbose
        self.export_path = export_path

    def __getstate__(self):
        """
        Prepare the state dictionary for serialization.

        This method is used to serialize the object's state into a dictionary. The dictionary contains all the necessary information to reconstruct the object's state later.

        Parameters:
            None

        Returns:
            state (dict): A dictionary containing the serialized state of the object.
        """
        state = {
            'inputs': self.inputs,
            'outputs': self.outputs,
            'n_hidden': self.n_hidden,
            'hidden_range': self.hidden_range,
            'hidden_interval': self.hidden_interval,
            'batch_sizes': self.batch_sizes,
            'learning_rates': self.learning_rates,
            'activation_functions': [func.__class__.__name__ for func in self.activation_functions],  # Store class names
            'epoachs': self.epoachs,
            'n_random': self.n_random,
            'verbose': self.verbose,
            'export_path': self.export_path
        }
        return state

    def __setstate__(self, state):
        """
        Restore the object's state from the dictionary.

        This method is used to serialize the object's state into a dictionary. The dictionary contains all the necessary information to reconstruct the object's state later.

        Parameters:
            state (dict): A dictionary containing the serialized state of the object.

        Attributes restored:
            inputs (int): The number of inputs in the dataset.
            outputs (int): The number of outputs in the dataset.
            n_hidden (int): The number of hidden layers in the neural network.
            hidden_range (tuple[int, int]): A tuple representing the range of possible number of neurons in each hidden layer.
            hidden_interval (int): The interval between sizes in the hidden range.
            batch_sizes (list[int]): A list of possible batch sizes for training the neural network.
            learning_rates (list[float]): A list of possible learning rates for the optimizer.
            activation_functions (list[Activation]): A list of activation functions to be used in the neural network.
            epoachs (int): The number of epochs to train the neural network.
            n_random (int): The number of random configurations to generate.
            verbose (bool, optional): A boolean flag indicating whether to print training progress. Defaults to False.
            export_path (str, optional): The path to export the configuration to a file. Defaults to None.

        Returns:
            None: This method does not return any value. It initializes the OptimizerConfig object with the provided parameters.
        """
        self.inputs = state['inputs']
        self.outputs = state['outputs']
        self.n_hidden = state['n_hidden']
        self.hidden_range = state['hidden_range']
        self.hidden_interval = state['hidden_interval']
        self.batch_sizes = state['batch_sizes']
        self.learning_rates = state['learning_rates']
        activation_class_names = state['activation_functions']
        self.epoachs = state['epoachs']
        self.n_random = state['n_random']
        self.verbose = state['verbose']
        self.export_path = state['export_path']

        # Map class names to actual classes
        activation_classes = {
            'Tanh': Tanh,
            'Relu': Relu,
            'Sigmoid': Sigmoid
        }

        # Instantiate the activation function classes
        self.activation_functions = []
        for class_name in activation_class_names:
            if class_name in activation_classes:
                self.activation_functions.append(activation_classes[class_name]())
            else:
                raise ValueError(f"Unknown activation class: {class_name}")

    def export_config(self):
        """
        Export the configuration to a file specified by the 'export_path' attribute.

        Parameters:
            None

        Returns:
            None: This method does not return any value. It exports the configuration to a file.

        Raises:
            ValueError: If the 'export_path' attribute is not provided, a ValueError is raised with a message indicating that the export path is not provided.

        Note:
            This method uses the 'export_config' method of the parent class (Config) to perform the actual export operation. If the 'export_path' attribute is not provided, a message is printed indicating that the export path is not provided, and the configuration is not exported.
        """
        if self.export_path:
            super().export_config(self, self.export_path)
        else:
            print("Export path not provided, config not exported.")

    @staticmethod
    def import_config(path: str):
        """
        Import a configuration from a file specified by the 'path' parameter.

        Parameters:
            path (str): The path to the file containing the configuration.

        Returns:
            config (OptimizerConfig): An instance of the OptimizerConfig class containing the imported configuration.

        Raises:
            ValueError: If the imported configuration is not of type OptimizerConfig, a ValueError is raised with a message indicating that the imported configuration is not of the expected type.

        Note:
            This method uses the 'import_config' method of the parent class (Config) to perform the actual import operation. If the imported configuration is not of type OptimizerConfig, a ValueError is raised.
        """
        config = Config.import_config(path)
        if isinstance(config, OptimizerConfig):
            return config
        else:
            raise ValueError("Imported configuration is not of type OptimizerConfig")

