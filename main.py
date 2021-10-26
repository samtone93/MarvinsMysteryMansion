# Marvin's Mystery Mansion

import json

action_json_file = open("actions.json")
action_list = json.load(action_json_file)
action_json_file.close()

objects_json_file = open("objects.json")
objects_list = json.load(objects_json_file)
objects_json_file.close()

inventory_json_file = open("inventory.json")
inventory = json.load(inventory_json_file)
inventory_json_file.close()

room_json_file = open("1.json")
room_data_1 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("2.json")
room_data_2 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("3.json")
room_data_3 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("4.json")
room_data_4 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("5.json")
room_data_5 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("6.json")
room_data_6 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("7.json")
room_data_7 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("8.json")
room_data_8 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("9.json")
room_data_9 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("10.json")
room_data_10 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("11.json")
room_data_11 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("12.json")
room_data_12 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("13.json")
room_data_13 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("14.json")
room_data_14 = json.load(room_json_file)
room_json_file.close()

room_json_file = open("15.json")
room_data_15 = json.load(room_json_file)
room_json_file.close()

room_data_list = [
    inventory,
    room_data_1,
    room_data_2,
    room_data_3,
    room_data_4,
    room_data_5,
    room_data_6,
    room_data_7,
    room_data_8,
    room_data_9,
    room_data_10,
    room_data_11,
    room_data_12,
    room_data_13,
    room_data_14,
    room_data_15
]

current_room = room_data_1


def parse(input_command):
    # literal single word function name
    # need to account for destinations / directions

    if len(input_command.split()) == 1:
        if input_command in ('north', 'east', 'south', 'west'):
            return go(input_command)
        return eval(input_command + "()")

    # if one word case
    # > do word (verb)
    # else if
    # Two-word Case
    verb, argument = input_command.split()
    for action in action_list:
        for pair in action_list[action]:
            if verb == pair:
                # evaluating "go" returns room_data; room_data updated after parsed
                return eval(action + "(\"" + argument + "\")")

    #for object in objects_list:
    #    for alias in objects_list[object]["name"]:
    #        if alias in input_command:

    # longer sentence ->
    # remove prepositions (up/down/the... junk words)
    # check first word, compare to actions.json -> continue as normal
    # remove verb, left-over string is either room or object


def go(direction):
    if direction in current_room["exits"]:
        new_data = room_data_list[current_room["exits"][direction][0]]
    else:
        print("There is no exit " + direction)
        new_data = current_room
    return new_data

# assume it's legal
# inventory -> room
def put(item):
    current_room["objects"].append(item)
    inventory["objects"].remove(item)
    return current_room


# room -> inventory
def take(item):
    inventory["objects"].append(item)
    current_room["objects"].remove(item)
    return current_room

# no arg -> room smell
# 1 arg -> smell object..?


# Describes the smell of the current room.
def smell():
    print(current_room["smell"])
    return current_room


# Describes the sound of the current room.
def listen():
    print(current_room["sound"])
    return current_room


# Long description of the current room.
def look():
    print(current_room["longDesc"])
    return current_room

def look_at(object):
    print(object["longDesc"])


print()
print("While you were going about your day, you were abducted and dropped off at an unknown location.")
print("You feel the car stop and the driver leaves you with a letter before driving off in the distance.")
print("It reads: “Hello <Player>, I hope this letter finds you well.")
print(
    "As my last remaining kin, I have left you the entirety of my fortune, which includes the mansion you currently stand at.")
print(
    "Inside, I hope you’ll find, decipher, and solve the clues I’ve left behind, to which will truly determine whether or not you are worthy of the Lehane family legacy.")
print("Prevail, and you shall inherit it all; fail, and you will return to what you once were.")
print()

while True:
    print("\nYou enter the " + current_room['roomName'] + ".")
    print(current_room['shortDesc'])
    print(current_room['longDesc'])
    print("Room items: " + str(current_room['objects']))
    print("Inventory: " + str(inventory['objects']))


    player_input = input(">").lower()
    current_room = parse(player_input)

