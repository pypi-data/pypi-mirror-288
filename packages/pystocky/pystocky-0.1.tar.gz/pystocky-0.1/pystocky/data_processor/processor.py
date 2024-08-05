"""
Internal module
Preprocess data (from. csv file)
"""

from copy import deepcopy

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler

from pystocky.data_processor import dataset


class DataProcessor:
    @classmethod
    def prepare_for_lstm(cls, data, lookback):
        """
        Process the dataset to make it suitable for LSTM models
        :param data: raw data
        :param lookback: Input data volume for prediction
        :return: processed data
        """
        d = deepcopy(data)
        d['date'] = pd.to_datetime(d['date'])
        d.set_index('date', inplace=True)

        for i in range(1, lookback + 1):
            d[f'close(t-{i})'] = d['close'].shift(i)

        d.dropna(inplace=True)
        return d

    @classmethod
    def get_dataset_for_lstm(cls, fn: str, lookback: int, train_set_ratio: float, target: str) \
            -> (MinMaxScaler, dataset.TimeSeriesDatasetForLSTM, dataset.TimeSeriesDatasetForLSTM):
        """
        Normalize data, partition training and testing sets
        :param fn: .csv file name
        :param lookback: Input data volume for prediction
        :param train_set_ratio: The proportion of the training dataset to the total dataset
        :param target: The targeted stock price data (such as 'close')
        :return: scaler, Dataset, Dataset
        """
        data = pd.read_csv(fn)[['date', target]]

        scaler = MinMaxScaler(feature_range=(-1, 1))
        normalized = scaler.fit_transform(cls.prepare_for_lstm(data, lookback))

        x = normalized[:, 1:]
        y = normalized[:, 0]

        x = np.flip(x, axis=1)

        split_index = int(len(x) * train_set_ratio)

        x_train = torch.tensor(x[:split_index].reshape((-1, lookback, 1)).copy(),
                               dtype=torch.float32)
        x_test = torch.tensor(x[split_index:].reshape((-1, lookback, 1)).copy(),
                              dtype=torch.float32)

        y_train = torch.tensor(y[:split_index].reshape((-1, 1)),
                               dtype=torch.float32)
        y_test = torch.tensor(y[split_index:].reshape((-1, 1)),
                              dtype=torch.float32)

        return (
            scaler,
            dataset.TimeSeriesDatasetForLSTM(x_train, y_train),
            dataset.TimeSeriesDatasetForLSTM(x_test, y_test)
        )
