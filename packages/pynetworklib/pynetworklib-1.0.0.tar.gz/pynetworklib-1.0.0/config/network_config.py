from network.activation_functions import Tanh, Relu, Sigmoid
from network.activation import Activation
from config.config import Config

class NetworkConfig(Config):
    def __init__(
                self,
                loss: str,
                epoachs: int,
                batch_size: int,
                learning_rate: float,
                activation: Activation,
                verbose=False,
                one_hot=False,
                export_path=None
                ):
        """
        Initialize the NetworkConfig object with the specified parameters.

        Args:
        - loss (str): The loss function to be used during training.
        - epoachs (int): The number of epochs to train for.
        - batch_size (int): The size of the mini-batches used during training.
        - learning_rate (float): The learning rate for the training.
        - activation (Activation): The activation function to be used in the network.
        - verbose (bool, optional): Whether to print training progress. Defaults to False.
        - one_hot (bool, optional): Whether to use one-hot encoding for the target variable. Defaults to False.
        - export_path (str, optional): The path to export the trained model. Defaults to None.

        Returns:
        None
        """
        self.loss = loss
        self.epoachs = epoachs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.activation = activation
        self.verbose = verbose
        self.one_hot = one_hot
        self.export_path = export_path

    def __getstate__(self):
        """
        Return a dictionary of the object's state.
    
        This method is used to serialize the object's state for pickling or other serialization purposes.
    
        Args:
        No arguments are required.
    
        Returns:
        A dictionary containing the state of the object. The dictionary includes the following keys:
            - 'loss': The loss function used during training.
            - 'epoachs': The number of epochs to train for.
            - 'batch_size': The size of the mini-batches used during training.
            - 'learning_rate': The learning rate for the training.
            - 'activation': The class name of the activation function used in the network.
            - 'verbose': A boolean indicating whether to print training progress.
            - 'one_hot': A boolean indicating whether to use one-hot encoding for the target variable.
            - 'export_path': The path to export the trained model.
        """
        state = {
            'loss': self.loss,
            'epoachs': self.epoachs,
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate,
            'activation': self.activation.__class__.__name__,  # Store class name
            'verbose': self.verbose,
            'one_hot': self.one_hot,
            'export_path': self.export_path
        }
        return state

    def __setstate__(self, state):
        # Restore the object's state from the dictionary
        self.loss = state['loss']
        self.epoachs = state['epoachs']
        self.batch_size = state['batch_size']
        self.learning_rate = state['learning_rate']
        activation_class_name = state['activation']
        self.verbose = state['verbose']
        self.one_hot = state['one_hot']
        self.export_path = state['export_path']

        # Map class names to actual classes
        activation_classes = {
            'Tanh': Tanh,
            'Relu': Relu,
            'Sigmoid': Sigmoid
        }
        if activation_class_name in activation_classes:
            self.activation = activation_classes[activation_class_name]()
        else:
            raise ValueError(f"Unknown activation class: {activation_class_name}")

    def export_config(self):
        if self.export_path:
            super().export_config(self, self.export_path)
        else:
            print("Export path not provided, config not exported.")


    @staticmethod
    def import_config(path):
        config = Config.import_config(path)
        if isinstance(config, NetworkConfig):
            return config
        else:
            raise ValueError("Imported configuration is not of type NetworkConfig")
