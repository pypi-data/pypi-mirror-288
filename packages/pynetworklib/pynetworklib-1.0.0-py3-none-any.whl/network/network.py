import numpy as np
import pickle

from network.dense import Dense
from network.activation import Activation
from network.activation_functions import *
from network.softmax import Softmax
from network.loss import Loss
from network.layer import Layer
from config.network_config import NetworkConfig

class Network:
    def __init__(self, network: list[Layer], inputs:int, outputs:int):
        if not isinstance(network, list):
            raise TypeError("network must be a list of layers")
        if not isinstance(inputs, int):
            raise TypeError("inputs must be an integer")
        if not isinstance(outputs, int):
            raise TypeError("outputs must be an integer")
        self.network = network
        self.inputs = inputs
        self.outputs = outputs

    def predict(self, input: np.ndarray):
        output = input
        output = np.reshape(output  , (self.inputs, 1))
        for layer in self.network:
            output = layer.forward(output)
        return output

    def fit(self, loss: Loss, x_train: list, y_train: list, epoachs = 100, batch_size = 10, learning_rate = 0.01, one_hot = False, verbose = False):
        if not isinstance(loss, Loss):
            raise TypeError("loss must be an instance of Loss")
        if not isinstance(x_train, list):
            raise TypeError("x_train must be a list")
        if not isinstance(y_train, list):
            raise TypeError("y_train must be a list")
        if not isinstance(epoachs, int) or epoachs <= 0:
            raise ValueError("epoachs must be a positive integer")
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not isinstance(learning_rate, (int, float)) or learning_rate <= 0:
            raise ValueError("learning_rate must be a positive number")
        if not isinstance(one_hot, bool):
            raise TypeError("one_hot must be a boolean")
        if not isinstance(verbose, bool):
            raise TypeError("verbose must be a boolean")
        
        if not x_train or not y_train:
            raise ValueError("Both x_train and y_train must be non-empty lists")

            
        n_samples = len(x_train)
        n_batches = int(n_samples/batch_size)
        errors= []
        
        for e in range(epoachs):
            error = 0 

            for i in range(n_batches):

                grad = np.zeros((self.outputs, 1))

                batch_start_index = i * batch_size
                batch_end_index = batch_start_index + batch_size

                for x,y in zip(x_train[batch_start_index: batch_end_index],
                                y_train[batch_start_index: batch_end_index]):

                    output = self.predict(x)
                    error += loss.loss(y, output)

                    grad += loss.loss_prime(y, output.T).T

                for layer in reversed(self.network):
                    grad = layer.backward(grad, learning_rate)

            error /= len(x_train)
            errors.append(error)

            if verbose:
                print(f"epoachs:{e+1}, error={error}")

        return errors


    @staticmethod
    def import_network(path: str):

        struct = []

        with open(path, "rb") as file:
            in_network = pickle.load(file)

        inputs, outputs = in_network[0][0], in_network[0][1]

        for layer in in_network:
            if isinstance(layer, Dense):
                struct.append(layer)
            if layer == "sigmoid":
                struct.append(Sigmoid())
            if layer == "softmax":
                struct.append(Softmax())
            if layer == "tanh":
                struct.append(Tanh())
            if layer == "relu":
                struct.append(Relu())

        return Network(struct, inputs, outputs)

    @staticmethod
    def export_network(network, path: str):

        struct = network.network

        out_network = [[network.inputs, network.outputs]]

        for layer in struct:
            if isinstance(layer, Dense):
                out_network.append(layer)
            if isinstance(layer, Sigmoid):
                out_network.append("sigmoid")
            if isinstance(layer, Softmax):
                out_network.append("softmax")
            if isinstance(layer, Tanh):
                out_network.append("tanh")
            if isinstance(layer, Relu):
                out_network.append("relu")

        with open(path, "wb") as file:
            pickle.dump(out_network, file)
    

    def train_from_config(self, config: NetworkConfig, xtrain: list, ytrain: list):

        loss = config.loss

        epochs = config.epoachs
        batch_size = config.batch_size

        learning_rate = config.learning_rate
        
        verbose = config.verbose
        one_hot = config.one_hot
        self.change_network_activations(config.activation)

        errors = self.fit(loss, xtrain, ytrain, epochs, batch_size, learning_rate, verbose=verbose, one_hot= one_hot)
        return errors
    
    def change_network_activations(self, activation: Activation):

        for i, layer in enumerate(self.network):

            if isinstance(layer, Activation):
                self.network[i] = activation