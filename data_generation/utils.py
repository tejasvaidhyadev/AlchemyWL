import logging
import json
import re
import pandas as pd
import pdb

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
    mapping_num_to_grond_ref = {0: 'first', 1: 'second', 2: 'third', 3: 'fourth', 4: 'fifth'}
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

def transform_ws(ws):
    # pdb.set_trace()
    f_str = ""
    for key in ws:
        f_str = f_str + key + " : " + " ".join(list(ws[key])) + " ; "
    f_str = re.sub(r'\d+', '', f_str)
    return f_str.strip()

def post_processing_data(exp_dir):
    with open(exp_dir +'/data.json', 'r') as f:
        data = json.load(f)
    initial_world_states_list = data['initial_world_states_list']
    initial_world_state_commands = data['initial_world_state_commands']
    update_world_states = data['update_world_states']
    input_ls = []
    output_ls = []
    # post processing
    for i, command in enumerate(initial_world_state_commands):
        # template start and end token
        initial_world_state_commands[i] = command
    for i, world_state in enumerate(initial_world_states_list):
        input_ls.append(transform_ws(world_state) + " SEPARATE " + initial_world_state_commands[i])
        world_state = str(world_state)
        # replace the numerical value with ""
        world_state = re.sub(r'\d+', '', world_state)
        initial_world_states_list[i] = world_state

    for i, world_state in enumerate(update_world_states):
        output_ls.append(transform_ws(world_state))
        world_state = str(world_state)
        world_state = re.sub(r'\d+', '', world_state)
        update_world_states[i] = str(world_state)

    df_dict = {"Input": input_ls, "Output": output_ls}
    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv(exp_dir +'/full' + '.tsv', sep="\t", index=None)

    train_df = df.sample(frac=0.8).reset_index(drop=True)
    df_all = df.merge(train_df.drop_duplicates(), on=['Input', 'Output'], how='left', indicator=True)
    test_df = df_all[df_all['_merge'] == 'left_only'][['Input', 'Output']].reset_index(drop=True)

    train_df.to_csv(exp_dir +'/train' + '.tsv', sep="\t", index=None)
    test_df.to_csv(exp_dir +'/dev' + '.tsv', sep="\t", index=None)

    with open(exp_dir +'/post_data.json', 'w') as f:
        # with proper indentation
        json.dump({'initial_world_states_list': initial_world_states_list, 'initial_world_state_commands': initial_world_state_commands, 'update_world_states': update_world_states}, f, indent=4)

def publish_data(exp_dir, initial_world_states_list, initial_world_state_commands, update_world_states):
    input_ls = []
    output_ls = []
    # post processing
    for i, world_state in enumerate(initial_world_states_list):
        input_ls.append(transform_ws(world_state) + " SEPARATE " + initial_world_state_commands[i])
        world_state = str(world_state)
        # replace the numerical value with ""
        world_state = re.sub(r'\d+', '', world_state)
        initial_world_states_list[i] = world_state

    for i, world_state in enumerate(update_world_states):
        output_ls.append(transform_ws(world_state))
        world_state = str(world_state)
        world_state = re.sub(r'\d+', '', world_state)
        update_world_states[i] = str(world_state)

    df_dict = {"Input": input_ls, "Output": output_ls}
    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv(exp_dir +'/full' + '.tsv', sep="\t", index=None)

    train_df = df.sample(frac=0.8).reset_index(drop=True)
    df_all = df.merge(train_df.drop_duplicates(), on=['Input', 'Output'], how='left', indicator=True)
    test_df = df_all[df_all['_merge'] == 'left_only'][['Input', 'Output']].reset_index(drop=True)

    train_df.to_csv(exp_dir +'/train' + '.tsv', sep="\t", index=None)
    test_df.to_csv(exp_dir +'/gen' + '.tsv', sep="\t", index=None)

    # with open(exp_dir +'/post_data.json', 'w') as f:
    #     # with proper indentation
    #     json.dump({'initial_world_states_list': initial_world_states_list, 'initial_world_state_commands': initial_world_state_commands, 'update_world_states': update_world_states}, f, indent=4)