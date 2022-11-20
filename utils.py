import os 
import logging
import json
def set_logger(log_path):
    """Set the logger to log info in terminal and file `log_path`."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)

        # Logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

class Params():
    """
    Class that loads hyperparameters from a pretty json file.
    """

    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by `params.dict['learning_rate']"""
        return self.__dict__

def num_to_grond_ref(num):
    # function to map number to grounded reference
    # example: 1 -> second
    if num == 0:
        return 'first'
    mapping_num_to_grond_ref = {1: 'second', 2: 'third', 3: 'fourth', 4: 'fifth'}
    return mapping_num_to_grond_ref[num]

def last_num_to_grond_ref(position, tot_len):
    # function to map last number to grounded reference
    # example: 1 -> second
    if position < 1:
        return ''
    elif position == tot_len - 1:
        return 'last '
    mapping_num_to_grond_ref = {1: 'last second', 2: 'last third', 3: 'last fourth'}
    return mapping_num_to_grond_ref[tot_len -1 - position] + ' '
