import os

import numpy as np
import pandas as pd

import torch
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt

from ..data.dataset.torch_overlap import NBAPlayerDataset
from ..machine_learning.use_models import use_model

from ..utils import filename_grabber
from ..utils.config import settings
from ..utils.logger import get_logger


# Create logger
logger = get_logger(__name__)

FILTER_AMT = settings.dataset.FILTER_AMT

# set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the dataset from the tensor file
df = pd.read_csv(filename_grabber.get_data_file("gold",
                                                settings.dataset.gold.DATA_FILE_CONTINUOUS_FIRST))

# Load the numpy array with proper numeric types
np_overlap = np.loadtxt(filename_grabber.get_data_file("gold",
                                                       settings.dataset.gold.DATA_FILE_CONTINUOUS_OVERLAP), delimiter=",")

# Reshape the 2D numpy array to its original shape
np_overlap = np_overlap.reshape(np_overlap.shape[0], FILTER_AMT, -1)

# Load the dictionary with proper numeric types
df_dict = pd.read_json(filename_grabber.get_data_file("gold",
                                                      settings.dataset.gold.DATA_FILE_CONTINUOUS_FIRST_JSON),
                       typ='series').to_dict()

# Instantiate the dataset
nba_dataset = NBAPlayerDataset(np_overlap)

# Create a DataLoader
data_loader = DataLoader(nba_dataset, batch_size=32, shuffle=False)


# Perform analytics on the dataset

# Get shape of the dataset
def get_input_shape(index=0):
    X, y = nba_dataset[index]
    print(f"X: {X.shape}, y: {y.shape}")

    return X, y


# Get the mean and standard deviation of the dataset
def get_mean_std():
    X = np.array([nba_dataset[i][0] for i in range(len(nba_dataset))])
    y = np.array([nba_dataset[i][1] for i in range(len(nba_dataset))])

    X_mean, X_std = np.mean(X), np.std(X)
    y_mean, y_std = np.mean(y), np.std(y)

    return X_mean, X_std, y_mean, y_std


# Get the min and max values of the dataset
def get_min_max():
    X = np.array([nba_dataset[i][0] for i in range(len(nba_dataset))])
    y = np.array([nba_dataset[i][1] for i in range(len(nba_dataset))])

    X_min, X_max = np.min(X), np.max(X)
    y_min, y_max = np.min(y), np.max(y)

    return X_min, X_max, y_min, y_max


# Get the number of features in the dataset
def get_num_features():
    X, y = nba_dataset[0]
    num_features = X.shape[1]

    return num_features


# Get the number of samples in the dataset
def get_num_samples():
    num_samples = len(nba_dataset)

    return num_samples


    # Create a line graph showing:
    #   1. the average 5 year projections of someone's career,
    #   2. the 5 year projects of piston players for all predictions.