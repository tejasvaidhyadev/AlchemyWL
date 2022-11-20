import random
import json
import argparse
from utils import *

parser = argparse.ArgumentParser()
# add parser for experiment name
parser.add_argument('--exp_name', type=str, default='experiment')
parser.add_argument('--num_datapoints', type=int, default=10, help='number of data to generate')
parser.add_argument('--max_repeat_color', type=int, default=3, help='maximum number of times a color can be repeated in each container of the initial world state')
args = parser.parse_args()

# define vocab of world state
operations = ['add', 'pour', 'unmix']
grounded_objects_container = ['jar', 'Beaker', 'bottle']
grounded_objects_color = ['orange', 'blue', 'green', 'yellow', 'red', 'purple']

# ToDo: post processing module for adding grounded_references to the data
grounded_references = ['Second', 'Third', 'Fourth', 'Fifth', 'last', 'last first', 'last second', 'last third', 'last fourth']

def generate_initial_world_state(num_containers):
    # function to generate initial world state
    initial_world_state = {}
    # counter for each keys of grounded_objects_container
    counter = {}
    for container in grounded_objects_container:
        counter[container] = 0
    for _ in range(num_containers):
        num_colors = random.randint(1, len(grounded_objects_color))
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
    # make sure container1 and container2 are different
    container2 = random.choice(list(initial_world_state.keys()))
    while container1 == container2:
        container2 = random.choice(list(initial_world_state.keys()))
    into_out_of_to = random.choice(['into', 'to'])
    
    if operation == 'add':
        # example command: add pink to jar
        color = random.choice(grounded_objects_color)
        quantity_color = random.choice(['one', 'two', 'three', 'four', 'five', 'six'])
        command = operation + ' ' + quantity_color + ' ' + color + ' ' + into_out_of_to + ' ' + container1
        
    elif operation == 'pour':
        # randomly select the [into, out of, to]
        command = operation + ' ' + container1 + " " +into_out_of_to+" " + container2
    elif operation == 'unmix':
        command = operation + ' ' + container1 
    return command

def generate_data(num_data, exp_dir):
    initial_world_states_list = []
    initial_world_state_commands = []
    update_world_states = []
    for _ in range(num_data):
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
        

def mapping_words_to_num(word):
    # using dictionary to map words to numbers
    mapping_words_to_num = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
    return mapping_words_to_num[word]

def preprocessing_command(command, counter_container_type):
    # Example command: "add six pink to jar1", to "add six pint to first jar"
    command = command.split()
    # find word with with part from grounded_objects_container
    # example: jar1 -> first jar
    for i, word in enumerate(command):
        if word[:-1] in grounded_objects_container:
            num = random.randint(0, 1)
            if num == 0 and counter_container_type[word[:-1]] < 4:
                command[i] = last_num_to_grond_ref(int(word[-1]), counter_container_type[word[:-1]]) + word[:-1]
            else: 
                command[i] = num_to_grond_ref(int(word[-1]))+ " " + word[:-1]
    return ' '.join(command)

def update_world_state(world_state, command):
    command = command.split()
    if 'pour'== command[0] or 'unmix' == command[0]:
        operation = command[0]
        container1 = command[1]
        if operation != 'unmix':
            container2 = command[3] 
        else:
            container2 = None
        
    if 'add' == command[0]:
        operation = command[0]
        quantity_color = command[1]
        color = command[2]
        container1 = command[4]
        container2 = None
    container1_state = world_state[container1]

    if container2:
        container2_state = world_state[container2]
    if operation == 'add':
        # for example: add pink to jar. intial state: jar1 = 'b', jar2 = 'r', jar3 = 'g' 
        # command: add pink to jar1 updated state: jar1 = 'bp', jar2 = 'r', jar3 = 'g'
        world_state[container1] = container1_state + color[0]*int(mapping_words_to_num(quantity_color))       
    elif operation == 'pour':
        container2_state = container1_state + container2_state
        world_state[container1] = ''
        world_state[container2] = container2_state
    elif operation == 'unmix':
        num_colors = len(set(container1_state))
        if num_colors == 1:
            return world_state
        elif num_colors > 1:
            new_world_state = {}
            for i in range(num_colors):
                new_world_state[container1+str(i)] = ''
                # add the same colors into the same container
                # for example, if the container1_state is 'rrbbc', then the container1_0 will be 'rr', 
                # container1_1 will be 'bb', and container1_2 will be 'c'
                for color in container1_state:
                    if color == container1_state[i]:
                        new_world_state[container1+str(i)] += color

            # delete the original container with new_world_state_container
            final_dict={}
            for keys in world_state.keys():
                final_dict[keys] = world_state[keys]
                if keys == container1:
                    final_dict.update(new_world_state)
            del final_dict[container1]
            world_state = final_dict
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
