from generate_data import  generate_initial_world_state, grounded_objects_color, grounded_objects_container, operations, args, update_world_state 
from collections import OrderedDict
def test_command_structure():
    # check the structure of the command   
    command = 'add two green to jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1] in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    assert command[2] in grounded_objects_color
    assert command[3] == 'to'
    assert command[4][:-1] in grounded_objects_container

    command = 'pour jar0 to jar1'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container
    assert command[2] == 'to'
    assert command[3][:-1] in grounded_objects_container
    
    command = 'unmix jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container

    command = 'filter jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container

    command = 'extract three from jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1] in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    assert command[2] == 'from'
    assert command[3][:-1] in grounded_objects_container


    command = 'remove two from jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1] in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    assert command[2] == 'from'
    assert command[3][:-1] in grounded_objects_container

    command = 'destroy jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container

    command = 'double jar0'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container

    command = 'transfer two red from jar0 to jar1'
    command = command.split()
    assert command[0] in operations
    assert command[1] in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    assert command[2] in grounded_objects_color
    assert command[3] == 'from'
    assert command[4][:-1] in grounded_objects_container
    assert command[5] == 'to'
    assert command[6][:-1] in grounded_objects_container

    command = 'shift jar0 after jar1'
    command = command.split()
    assert command[0] in operations
    assert command[1][:-1] in grounded_objects_container
    assert command[2] in ['after', 'before']
    assert command[3][:-1] in grounded_objects_container

# Test to see if grounded ojects have colors with unique first letters
def test_unique_colors():
    colors = []
    for color in grounded_objects_color:
        colors.append(color[0])
    assert len(set(colors)) == len(colors) #"Colors do not have unique first letters"

# test intial world state
def test_generate_initial_world_state():
    initial_world_state, counter_container_type = generate_initial_world_state(3)
    assert len(initial_world_state) == 3
    assert len(counter_container_type) == len(grounded_objects_container)
    for container in grounded_objects_container:
        assert container in counter_container_type
    for container in initial_world_state:
        assert len(initial_world_state[container]) > 0
        # assert len(initial_world_state[container]) <= args.num_colors 
        for color in initial_world_state[container]:
            assert color not in grounded_objects_color

def test_command_on_world_state():
    # test command add
    initial_world_state = {'jar0': 'r', 'jar1': 'b', 'jar2': 'g'}
    command = 'add two green to jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'rgg', 'jar1': 'b', 'jar2': 'g'}

    # test command pour
    initial_world_state = {'jar0': 'r', 'jar1': 'b', 'jar2': 'g'}
    command = 'pour jar0 to jar1'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': '', 'jar1': 'br', 'jar2': 'g'}

    # test command unmix
    initial_world_state = {'jar0': 'rrb', 'jar1': 'bb', 'jar2': 'gg'}
    command = 'unmix jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar00': 'rr', 'jar01': 'b', 'jar1': 'bb', 'jar2': 'gg'}

    # test command filter
    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'filter jar1'

    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'rbr', 'jar1': 'bbr', 'jar2': 'gg'}

    command = 'extract two red from jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'b', 'jar1': 'brb', 'jar2': 'gg'}

    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'remove one from jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'rb', 'jar1': 'brb', 'jar2': 'gg'}

    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'destroy jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar1': 'brb', 'jar2': 'gg'}


    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'double jar0'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'rbrrbr', 'jar1': 'brb', 'jar2': 'gg'}

    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'transfer two red from jar0 to jar1'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'b', 'jar1': 'brbrr', 'jar2': 'gg'}

    initial_world_state = {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}
    command = 'shift jar0 after jar1'
    initial_world_state = OrderedDict(initial_world_state)
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar1': 'brb', 'jar0': 'rbr', 'jar2': 'gg'}
    
    command = 'shift jar0 before jar1'
    update_world = update_world_state(initial_world_state.copy(), command)
    assert update_world == {'jar0': 'rbr', 'jar1': 'brb', 'jar2': 'gg'}