import pickle

class Config:
    def __init__(self):
        pass

    @staticmethod
    def import_config(path: str):
        """
        Import a previously saved configuration from a pickle file.

        Parameters:
        path (str): The path to the pickle file containing the configuration.

        Returns:
        Config: The imported configuration object.
        """
        with open(path, "rb") as file:
            config = pickle.load(file)
        return config
    
    def export(self, path: str):
        """
        Export the current configuration to a pickle file.

        Parameters:
        path (str): The path to the pickle file where the configuration will be saved.

        Returns:
        None. The function saves the configuration to the specified file.
        """
        with open(path, "wb") as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)
    @staticmethod
    def export_config(config, path: str):
        """
        Export the given configuration object to a pickle file.

        Parameters:
        config (Config): The configuration object to be saved.
        path (str): The path to the pickle file where the configuration will be saved.

        Returns:
        None. The function saves the configuration to the specified file.
        """
        with open(path, "wb") as file:
            pickle.dump(config, file, protocol=pickle.HIGHEST_PROTOCOL)   
