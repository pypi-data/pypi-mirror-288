"""
LSTM stock prediction model
Model structure:
LSTMModel(
  (lstm1): LSTM(_INPUT_SIZE, _HIDDEN_SIZE1, batch_first=True)
  (lstm2): LSTM(_HIDDEN_SIZE1, _HIDDEN_SIZE2, batch_first=True)
  (fc1): Linear(in_features=_HIDDEN_SIZE2, out_features=_FC1_SIZE, bias=True)
  (fc2): Linear(in_features=_FC1_SIZE, out_features=_FC2_SIZE, bias=True)
  (fc3): Linear(in_features=_FC2_SIZE, out_features=_OUTPUT_SIZE, bias=True)
)
"""

import torch.nn as nn

_INPUT_SIZE = 1  # Input layer size
_HIDDEN_SIZE1 = 128  # Hidden layer 1 size
_HIDDEN_SIZE2 = 128  # Hidden layer 2 size
_FC1_SIZE = 64  # Fully connected layer 1 size
_FC2_SIZE = 32  # Fully connected layer 2 size
_OUTPUT_SIZE = 1  # Output layer size


class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(_INPUT_SIZE, _HIDDEN_SIZE1, batch_first=True)
        self.lstm2 = nn.LSTM(_HIDDEN_SIZE1, _HIDDEN_SIZE2, batch_first=True)
        self.fc1 = nn.Linear(_HIDDEN_SIZE2, _FC1_SIZE)
        self.fc2 = nn.Linear(_FC1_SIZE, _FC2_SIZE)
        self.fc3 = nn.Linear(_FC2_SIZE, _OUTPUT_SIZE)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x = self.fc1(x[:, -1, :])
        x = self.fc2(x)
        x = self.fc3(x)
        return x
