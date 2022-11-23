import random
import json
import argparse
from utils import *
import re 
import os
from collections import OrderedDict
import pdb

parser = argparse.ArgumentParser()
# add parser for experiment name
parser.add_argument('--exp_name', type=str, default='experiment')
parser.add_argument('--num_datapoints', type=int, default=10, help='number of data to generate')
parser.add_argument('--num_colors', type=int, default=4, help='max number of distinct colors to keep per container')
parser.add_argument('--max_repeat_color', type=int, default=3, help='maximum number of times a color can be repeated in each container of the initial world state')
args = parser.parse_args()

# define vocab of world state
operations = ['add', 'pour', 'unmix', 'filter', 'extract', 'remove', 'destroy', 'double', 'transfer', 'shift']
grounded_objects_container = ['jar', 'beaker', 'bottle', 'mug', 'thermos', 'glass', 'cup', 'flask', 'burette', 'pitcher', 'jug', 'urn', 'decanter', 'flagon', 'canister', 'vessel']
grounded_objects_color = ['orange', 'blue', 'green', 'yellow', 'red', 'purple', 'magenta', 'violet', 'aqua', 'cabernet', 'daffodil', 'emberiae', 'fuchsia', 'harlequin']
char_to_color = {}
for col in grounded_objects_color:
    if col[0] in char_to_color:
        print("Multiple colors with same initial!")
        pdb.set_trace()
    char_to_color[col[0]] = col

def generate_initial_world_state(num_containers):
    # function to generate initial world state
    initial_world_state = OrderedDict()
    # counter for each keys of grounded_objects_container
    counter = {}
    for container in grounded_objects_container:
        counter[container] = 0
    for _ in range(num_containers):
        num_colors = random.randint(1, args.num_colors)
        grounded_objects_color_with_prob = grounded_objects_color* args.max_repeat_color
        colors = random.sample(grounded_objects_color_with_prob, num_colors)
        container_name = random.choice(grounded_objects_container)        
        color_name = ''.join([color[0] for color in colors])
        container_state = ''.join(color_name)
        initial_world_state[container_name+str(counter[container_name])] = container_state
        counter[container_name] += 1

    return initial_world_state, counter

def build_command_state(initial_world_state):
    # function to build command state
    # generate initial world state command
    operation = random.choice(operations)
    container1 = random.choice(list(initial_world_state.keys()))
    colors_c1_str = initial_world_state[container1]
    colors_c1_dict = {}
    total_c1 = len(colors_c1_str)
    for c in colors_c1_str:
        if c in colors_c1_dict:
            colors_c1_dict[c] += 1
        else:
            colors_c1_dict[c] = 1
    # make sure container1 and container2 are different
    container2 = random.choice(list(initial_world_state.keys()))
    while container1 == container2:
        container2 = random.choice(list(initial_world_state.keys()))
    into_out_of_to = random.choice(['into', 'to'])
    
    if operation == 'add':
        # example command: add three pink to jar
        color = random.choice(grounded_objects_color)
        quantity_color = random.choice(['one', 'two', 'three', 'four', 'five', 'six'])
        command = operation + ' ' + quantity_color + ' ' + color + ' ' + into_out_of_to + ' ' + container1
    elif operation == 'pour':
        # randomly select the [into, out of, to]
        command = operation + ' ' + container1 + " " + into_out_of_to + " " + container2
    elif operation == 'unmix':
        command = operation + ' ' + container1 
    elif operation == 'filter':
        command = operation + ' ' + container1
    elif operation == 'extract':
        color = random.choice(list(colors_c1_dict.keys()))
        quantity_color = mapping_num_to_words(random.randint(1, colors_c1_dict[color]))
        command = operation + ' ' + quantity_color + ' ' + char_to_color[color] + ' from ' + container1
    elif operation == 'remove':
        color = random.choice(list(colors_c1_dict.keys()))
        quantity_color = mapping_num_to_words(random.randint(1, total_c1))
        command = operation + ' ' + quantity_color + ' from ' + container1
    elif operation == 'destroy':
        command = operation + ' ' + container1
    elif operation == 'double':
        command = operation + ' ' + container1
    elif operation == 'transfer':
        # example command: transfer two pink from jar to beaker
        color = random.choice(list(colors_c1_dict.keys()))
        quantity_color = mapping_num_to_words(random.randint(1, colors_c1_dict[color]))
        command = operation + ' ' + quantity_color + ' ' + char_to_color[color] + ' from ' + container1 + ' ' + into_out_of_to + ' ' + container2
    elif operation == 'shift':
        # example command: shift jar after/before beaker
        ch = random.uniform(0, 1)
        if ch > 0.5:
            command = operation + ' ' +  container1 + ' after ' + container2
        else:
            command = operation + ' ' +  container1 + ' before ' + container2
    return command

def generate_data(num_data, exp_dir):
    # pdb.set_trace()
    initial_world_states_list = []
    initial_world_state_commands = []
    update_world_states = []
    for z in range(num_data):
        # generate initial world state
        ## sampling number of containers in each world state from 2 to 5
        num_containers = random.randint(2, 5)

        # generate initial world state
        initial_world_state, counter_container_type = generate_initial_world_state(num_containers)
        initial_world_states_list.append(initial_world_state)

        # generate initial world state command
        command = build_command_state(initial_world_state)
        update_world = update_world_state(initial_world_state.copy(), command)

        # preprocessing command
        command = preprocessing_command(command, counter_container_type)
        initial_world_state_commands.append(command)
        update_world_states.append(update_world)
        # save the initial world state, command, and updated world state to a file
        # save json fiel in the experiment directory

        with open(exp_dir +'/data.json', 'w') as f:
            # with proper indentation
            json.dump({'initial_world_states_list': initial_world_states_list, 'initial_world_state_commands': initial_world_state_commands, 'update_world_states': update_world_states}, f, indent=4)
        post_processing_data(exp_dir)
        print("Completed {} / {}...".format(z+1, num_data), end = '\r', flush = True)

def mapping_words_to_num(word):
    # using dictionary to map words to numbers
    mapping_words_to_num = {
        'one': 1, 
        'two': 2, 
        'three': 3, 
        'four': 4, 
        'five': 5, 
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10
    }
    return mapping_words_to_num[word]

def mapping_num_to_words(num):
    num_to_str = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten"
    }
    return num_to_str[num]

def preprocessing_command(command, counter_container_type):
    # Example command: "add six pink to jar1", to "add six pink to first jar"
    command = command.split()
    # find word with with part from grounded_objects_container
    # example: jar1 -> first jar
    for i, word in enumerate(command):
        if word[:-1] in grounded_objects_container:
            # num = random.randint(0, 1)
            if counter_container_type[word[:-1]] > 1:
                if int(word[-1]) == counter_container_type[word[:-1]]-1:
                    ch = random.uniform(0, 1)
                    if ch < 0.3:
                        command[i] = num_to_grond_ref(int(word[-1]))+ " " + word[:-1]
                    else:
                        command[i] = 'last ' + word[:-1]
                        # command[i] = last_num_to_grond_ref(int(word[-1]), counter_container_type[word[:-1]]) + word[:-1]
                else:
                    command[i] = num_to_grond_ref(int(word[-1]))+ " " + word[:-1]
            else:
                command[i] = word[:-1]
    return ' '.join(command)

def update_world_state(world_state, command):
    command = command.split()
    operation = command[0]

    if operation == 'add':
        # for example: add pink to jar. intial state: jar1 = 'b', jar2 = 'r', jar3 = 'g' 
        # command: add pink to jar1 updated state: jar1 = 'bp', jar2 = 'r', jar3 = 'g'
        quantity_color = command[1]
        color = command[2]
        container1 = command[4]
        container1_state = world_state[container1]
        world_state[container1] = container1_state + color[0]*int(mapping_words_to_num(quantity_color))       
    elif operation == 'pour':
        container1 = command[1]
        container2 = command[3]
        container1_state = world_state[container1]
        container2_state = world_state[container2]
        container2_state = container2_state + container1_state
        world_state[container1] = ''
        world_state[container2] = container2_state
    elif operation == 'unmix':
        container1 = command[1]
        container1_state = world_state[container1]
        unique_colors = list(sorted(set(container1_state), key=container1_state.index))
        num_colors = len(unique_colors)

        if num_colors == 1:
            return world_state
        elif num_colors > 1:
            new_world_state = OrderedDict()
            for i in range(num_colors):
                new_world_state[container1+str(i)] = ''
                # add the same colors into the same container
                # for example, if the container1_state is 'rrbbc', then the container1_0 will be 'rr', 
                # container1_1 will be 'bb', and container1_2 will be 'c'
                for color in container1_state:
                    if color == unique_colors[i]:
                        new_world_state[container1+str(i)] += color
                # remove the container1[i] from the container1_state
                
            # delete the original container with new_world_state_container
            final_dict=OrderedDict()
            for keys in world_state.keys():
                final_dict[keys] = world_state[keys]
                if keys == container1:
                    final_dict.update(new_world_state)
            del final_dict[container1]
            world_state = final_dict
    elif operation == 'filter':
        container1 = command[1]
        container1_state = world_state[container1]
        col_dict = OrderedDict()
        for c in container1_state:
            if c in col_dict:
                col_dict[c] += 1
            else:
                col_dict[c] = 1
        new_str = ""
        for c in col_dict:
            new_str = new_str + "".join([c for i in range(col_dict[c])])
        world_state[container1] = new_str
    elif operation == 'extract':
        container1 = command[-1]
        container1_state = world_state[container1]
        quantity_color = mapping_words_to_num(command[1])
        color = command[2][0]
        new_ls = []
        for c in range(len(container1_state)-1, 0, -1):
            if quantity_color > 0:
                if container1_state[c]!=color:
                    new_ls.append(container1_state[c])
                    quantity_color -= 1
            else:
                new_ls.append(container1_state[c])
        new_str = ""
        for e in range(len(new_ls)-1, 0, -1):
            new_str = new_str + new_ls[e]
        world_state[container1] = new_str
    elif operation == 'remove':
        container1 = command[-1]
        quantity_color = mapping_words_to_num(command[1])
        world_state[container1] = world_state[container1][:len(world_state[container1])-quantity_color]
    elif operation == 'destroy':
        container1 = command[1]
        del world_state[container1]
    elif operation == 'double':
        container1 = command[1]
        world_state[container1] = world_state[container1] + world_state[container1]
    elif operation == 'transfer':
        container1 = command[4]
        container2 = command[-1]
        container1_state = world_state[container1]
        container2_state = world_state[container2]
        quantity_color = mapping_words_to_num(command[1])
        temp_qty = quantity_color
        color = command[2][0]
        new_ls = []
        for c in range(len(container1_state)-1, 0, -1):
            if quantity_color > 0:
                if container1_state[c]!=color:
                    new_ls.append(container1_state[c])
                    quantity_color -= 1
            else:
                new_ls.append(container1_state[c])
        new_str = ""
        for e in range(len(new_ls)-1, 0, -1):
            new_str = new_str + new_ls[e]
        world_state[container1] = new_str
        world_state[container2] = world_state[container2] + "".join([color for i in range(temp_qty)])
    elif operation == "shift":
        container1 = command[1]
        container2 = command[-1]
        connector = command[2]
        cur_order = list(world_state.keys())
        cur_order.remove(container1)
        new_ls = []
        try:
            idx = cur_order.index(container2)
        except:
            pdb.set_trace()
        if connector == "before":
            if idx == 0:
                new_ls = [container1] + cur_order
            else:
                new_ls = cur_order[:idx] + [container1] + cur_order[idx:]
        else:
            if idx == len(cur_order)-1:
                new_ls = cur_order + [container1]
            else:
                new_ls = cur_order[:idx+1] + [container1] + cur_order[idx+1:]
        for k in new_ls:
            world_state.move_to_end(k)

    return world_state
            
def main(exp_dir):
    generate_data(args.num_datapoints, exp_dir)
    
# init main call
if __name__ == '__main__':
    # create directory if not exists
    if not os.path.exists('data'):
        os.makedirs('data')
    # create folder with name args.exp_name
    if not os.path.exists('data/'+args.exp_name):
        os.makedirs('data/'+args.exp_name)
    exp_dir = 'data/'+args.exp_name
    set_logger(os.path.join(exp_dir, 'log.txt'))
    logging.info('Experiment directory: %s', exp_dir)
    logging.info('Arguments: %s', args)
    logging.info("Generating ")
    main(exp_dir)
    logging.info("Done")
