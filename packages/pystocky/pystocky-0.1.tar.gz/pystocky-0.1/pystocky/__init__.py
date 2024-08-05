"""
pystocky - a PyTorch based stock model training and prediction library

Usage:

**Training mode**

- Configure basic parameters through the config module

- Instantiate trainer based on config

- Start training

**Prediction mode**

- Provide model file (. pth)

- Instantiate predictor

- Starting prediction with given data
"""

from . import config, trainer

__all__ = [
    'config',
    'trainer',
]
