"""
Set global configuration
===========================
Set by init_from_ series functions

The config parameters and instructions are as follows:

- Basic parameters

**data** - Source data path

**output** - List of trained model parameter outputs

**train_set_ratio** - The proportion of the training set to the dataset (default value: 0.9)

**look_back** - The amount of data used for prediction (default value: 30)

**device** - Device used for training and evaluation (default value: cpu) **(Could only be `cpu` or `cuda`)**

-Machine learning hyperparameters

**epochs** - number of training iterations (default value: 100)

**lr** - Initial learning rate (default value: 4e-3)

"""

from configparser import ConfigParser


def init_from_dict(d: dict) -> dict:
    """
    Read parameters from the dictionary
    If a parameter is not provided, use the default value if possible

    :param d: Input dictionary
    :return: None
    """
    stock_config = {
        'data': '',
        'output': '',
        'train_set_ratio': 0.9,

        'epochs': 100,
        'lr': 4e-3,

        'look_back': 30,

        'device': 'cpu'
    }

    try:
        stock_config['data'] = d['data']
        stock_config['output'] = d['output']
    except KeyError:
        raise KeyError('You must provide two parameters, data and output,'
                       'and at least one of them is missing from the given ones')
    if 'train_set_ratio' in d:
        stock_config['train_set_ratio'] = d['train_set_ratio']
    if 'epochs' in d:
        stock_config['epochs'] = d['epochs']
    if 'lr' in d:
        stock_config['lr'] = d['lr']
    if 'look_back' in d:
        stock_config['look_back'] = d['look_back']
    if 'device' in d:
        if (device := d['device']) not in ['cpu', 'cuda']:
            raise RuntimeError('Device could only be `cpu` or `cuda`')
        else:
            stock_config['device'] = device

    return stock_config


def init_from_ini(fn: str) -> dict:
    """
    Read configuration based on .ini configuration file
    :param fn: .ini file name
    :return: None
    """
    stock_config = {
        'data': '',
        'output': '',
        'train_set_ratio': -1,

        'epochs': 100,
        'lr': 4e-3,

        'look_back': 30,

        'device': 'cpu'
    }
    parser = ConfigParser()
    parser.read(fn)
    if parser.has_section('settings'):
        if parser.has_option('settings', 'data'):
            stock_config['data'] = parser.get('settings', 'data')
        else:
            raise KeyError('You must provide `data`')
        if parser.has_option('settings', 'output'):
            stock_config['output'] = parser.get('settings', 'output')
        else:
            raise KeyError('You must provide `output`')
        if parser.has_option('settings', 'train_set_ratio'):
            stock_config['train_set_ratio'] = parser.getint('settings', 'train_set_ratio')
        if parser.has_option('settings', 'epochs'):
            stock_config['epochs'] = parser.getint('settings', 'epochs')
        if parser.has_option('settings', 'lr'):
            stock_config['lr'] = parser.getfloat('settings', 'lr')
        if parser.has_option('settings', 'look_back'):
            stock_config['look_back'] = parser.getint('settings', 'look_back')
        if parser.has_option('settings', 'device'):
            if (device := parser.get('settings', 'device')) not in ['cpu', 'cuda']:
                raise RuntimeError('Device could only be `cpu` or `cuda`')
            else:
                stock_config['device'] = device
    else:
        raise KeyError('Configuration should be provided in section `settings`')

    return stock_config


__all__ = [
    'init_from_ini',
    'init_from_dict',
]
