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

prep_json_file = open("prep.json")
prep_list = json.load(prep_json_file)
prep_json_file.close()

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

current_room = room_data_12


def parse(input_command):
    # In case the player forgets to specify the item/argument of the verb

    if input_command in ("go", "put", "take", "look at"):
        print("That is not a legal command - be specific!.")
        return current_room

    # For singular verbs <put> <take> <smell> <listen> <look>
    if len(input_command.split()) == 1 and input_command in action_list:
        return eval(input_command + "()")

    # For movement via <direction> or <location>
    if input_command in (("north", "east", "south", "west") or current_room["exits"]):
        return go(input_command)

    # Remove prepositions the user may use (to, the, )
    # "  " kept as last entry in prepositions to remove any extra spaces
    for prep in prep_list["prepositions"]:
        if prep in input_command:
            input_command = input_command.replace(prep, '')

    # For movement via <go> <location>
    if "go" in input_command and input_command[3:] in current_room["exits"]:
        return go(input_command[3:])

    # For illegal movement; skipping or teleporting rooms
    if "go" in input_command and input_command[3:] not in current_room["exits"]:
        print("You can't go there from this room.")
        return current_room

    # Create default values to determine if they get changed
    verb, argument = "test", "test"

    # If an action or its alias is detected in user input
    for action in action_list:
        for alias in action_list[action]:
            if alias in input_command:
                verb = action

    # If an object or its alias is detected in user input and can be interacted with
    for key in objects_list:
        for name in objects_list[key]["name"]:
            if name in input_command and (name in current_room["objects"] or name in inventory["objects"]):
                argument = name

    # If not default values, eval the two
    if verb != "test" and argument != "test":
        return eval(verb + "(\"" + argument + "\")")
    # If default values, prompt user for another command.
    else:
        print("You can't do that. Try something else.")
        return current_room


# Handles both directions & entryways
# Edit room files to include aliases for entryways under "exits"
def go(argument):
    if argument in current_room["exits"]:
        new_data = room_data_list[current_room["exits"][argument][0]]
    else:
        print("You cannot go there.")
        new_data = current_room
    return new_data


# Object removed from inventory, placed in room.
def put(item):
    current_room["objects"].append(item)
    inventory["objects"].remove(item)
    return current_room


# Object removed from room, placed in inventory.
def take(item):
    inventory["objects"].append(item)
    current_room["objects"].remove(item)
    return current_room


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


# Description of the object.
def look_at(input):
    for item in objects_list:
        for name in objects_list[item]["name"]:
            if input == name and (item in current_room["objects"] or item in inventory["objects"]):
                print(objects_list[item]["desc"])
                return current_room
    print("There is no such thing to look at. Try again.")
    return current_room



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
