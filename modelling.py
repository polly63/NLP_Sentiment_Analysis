import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import math

# Network Hyperparameters:

create_ngram = False  # Create N-Grams to start
batch_size = 1
n_gram_size = 1
hidden_layers = 1
hidden_size = 1
learning_rate = 0.01
epochs = 1
vocab_size = 1
embedding_dimension = 1
dropout = 0


# Embedding

embed = torch.nn.Embedding(vocab_size, embedding_dim)

# Model input

model_input = embed(data) # Should be (ngram size x batch size x embedding dimension)


def check_input_size(input):
    """
    Throws an error if the input is wrong size
    :param input: data for model input
    :return: Nothing
    """
    if input.shape[0] != n_gram_size:
        print("given input shape:", input.shape[0], "expected:", n_gram_size)
        raise RuntimeError("The input is not the correct n-gram")
    elif input.shape[1] != batch_size:
        print("given input shape:", input.shape[1], "expected:", batch_size)
        raise RuntimeError("The input is not the correct batch-size")
    elif input.shape[2] != embedding_dimension:
        print("given input shape:", input.shape[2], "expected:", embedding_dimension)
        raise RuntimeError("The input is not the correct embedding dimension")


class Model1(nn.Module):
    def __init__(self):
        super(Model1, self).__init__()

        self.RNN1 = nn.Sequential(
            nn.RNN(input_size=embedding_dimension, hidden_size=hidden_size, num_layers=hidden_layers, dropout=dropout),
            nn.MaxPool1d(),
            nn.SELU()
        )

        self.FC1 = nn.Sequential(
            nn.Linear(),
            nn.MaxPool1d(),
            nn.SELU()
        )

        self.RNN2 = nn.Sequential(
            nn.RNN(input_size=embedding_dimension, hidden_size=hidden_size, num_layers=hidden_layers, dropout=dropout),
            nn.MaxPool1d(),
            nn.Tanh()
        )

    def forward(self, x):
        self.out1 = self.RNN1(x),
        self.out2 = self.RNN2(self.out1)
        return self.out2


def initial_weights():
    h0 = torch.randn(hidden_layers, batch_size, hidden_size)
    c0 = torch.randn(hidden_layers, batch_size, hidden_size)
    return h0, c0
