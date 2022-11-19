import random
import json

operations = ['add', 'pour', 'unmix']
grounded_objects_container = ['jar', 'Beaker', 'bottle']
grounded_objects_color = ['pink', 'blue', 'green', 'yellow', 'red', 'purple']
grounded_references = ['Second', 'Third', 'Fourth', 'Fifth', 'all', 'last', 'last first', 'last second', 'last third', 'last fourth']

def generate_initial_world_state():
    initial_world_state = {}
    for i in range(5):
        num_colors = random.randint(1, 6)
        colors = random.sample(grounded_objects_color, num_colors)
        container_name = random.choice(grounded_objects_container)        
        color_name = ''.join([color[0] for color in colors])
        container_state = ''.join(color_name)
        initial_world_state[container_name+str(i)] = container_state
    return initial_world_state
    

def generate_data(num_data=100):
    initial_world_states_list = []
    initial_world_state_commands = []
    update_world_states = []
    for _ in range(num_data):
        # generate initial world state
        initial_world_state = generate_initial_world_state()
        initial_world_states_list.append(initial_world_state)
        operations = ['add', 'pour', 'unmix']
        operation = random.choice(operations)
        container1 = random.choice(list(initial_world_state.keys()))
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
        
            
        # generate commands

        initial_world_state_commands.append(command)
        update_world = update_world_state(initial_world_state.copy(), command)

        # update the world state
        update_world_states.append(update_world)
        # save the initial world state, command, and updated world state to a file
        with open('data.json', 'w') as f:
            # with proper indentation
            json.dump({'initial_world_states_list': initial_world_states_list, 'initial_world_state_commands': initial_world_state_commands, 'update_world_states': update_world_states}, f, indent=4)
        
def mapping_words_to_num(word):
    if word == 'one':
        return 1
    elif word == 'two':
        return 2
    elif word == 'three':
        return 3
    elif word == 'four':
        return 4
    elif word == 'five':
        return 5
    else:
        return 6

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
        # for example: add pink to jar. intial state: jar1 = 'b', jar2 = 'r', jar3 = 'g' command: add pink to jar1 updated state: jar1 = 'bp', jar2 = 'r', jar3 = 'g'
        world_state[container1] = container1_state + color[0]*int(mapping_words_to_num(quantity_color))       
    elif operation == 'pour':
        container2_state = container1_state + container2_state
        world_state[container1] = ''
        world_state[container2] = container2_state
    elif operation == 'unmix':
        # number of different colors in the container
        num_colors = len(set(container1_state))
        # if the number of colors is 1, then the container is already unmix
        if num_colors == 1:
            return world_state
        # if the number of colors is 2, then the container will be divided into two containers
        elif num_colors > 1:
            # divide the container into different containers corresponding to the number of different colors
            for i in range(num_colors):
                world_state[container1+str(i)] = ''
                # add the same colors into the same container
                # for example, if the container1_state is 'rrbbc', then the container1_0 will be 'rr', container1_1 will be 'bb', and container1_2 will be 'c'
                for color in container1_state:
                    if color == container1_state[i]:
                        world_state[container1+str(i)] += color

            # delete the original container
    return world_state
            

def main():
    num = 10
    generate_data(num)
    
# init main call
if __name__ == '__main__':
    main()
