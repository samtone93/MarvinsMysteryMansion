# Marvin's Mystery Mansion

import json
from regex_filter import filter_prep

looping = True

action_json_file = open("actions.json")
action_list = json.load(action_json_file)
action_json_file.close()

prep_json_file = open("prep.json")
prep_list = json.load(prep_json_file)
prep_json_file.close()

objects_json_file = open("objects.json")
objects_list = json.load(objects_json_file)
objects_json_file.close()

inventory_json_file = open("inventory.json")
inventory_list = json.load(inventory_json_file)
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
    inventory_list,
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


# Quit game
def quit_game():
    print("Goodbye!")
    return False


def parse(input_command):
    # split input
    input_list = input_command.split()
    
    # get verb]
    verb = ""
    for action in action_list:
        for alias in action_list[action]:
            if alias in input_list[0]:
                verb = action
    
    # remove verb from input
    if verb == "":
        verb = "go"
    else:
        input_list.remove(input_list[0])
    
    # remove prepositions
    for prep in prep_list["prepositions"]:
        if prep in input_list:
            input_list.remove(prep)
    
    if verb == "look" and len(input_list) > 0:
        verb = "look_at"
    
    # create argument
    argument = ""
    while len(input_list) > 0:
        argument = argument + input_list[0]
        input_list.remove(input_list[0])
        if len(input_list) > 0:
            argument = argument + " "
    
    if argument == "":
        return eval(verb + "()")
    else:
        return eval(verb + "(\"" + argument + "\")")
    
    
# Converts item to be usable
def item_convert(item_str):
    item = ""
    for key in objects_list:
        for name in objects_list[key]["name"]:
            if name == item_str and (key in current_room["objects"] or key in inventory_list["objects"]):
                item = key
    return item


# Handles both directions & entryways
# Edit room files to include aliases for entryways under "exits"
def go(argument):
    if argument in current_room["exits"]:
        new_data = room_data_list[current_room["exits"][argument][0]]
        print("\nYou enter the " + new_data["roomName"] + ".")
        print(new_data["shortDesc"])
    else:
        print("You cannot go there.")
        new_data = current_room
    return new_data


# Object removed from inventory, placed in room.
def put(item):
    item = item_convert(item)
    if item in inventory_list["objects"]:
        current_room["objects"].append(item)
        inventory_list["objects"].remove(item)
        print(f"You put down the {objects_list[item]['name'][0]}")
    else:
        print("No item to put.")
    return current_room


# Object removed from room, placed in inventory.
def take(item):
    item = item_convert(item)
    if item in current_room["objects"]:
        inventory_list["objects"].append(item)
        current_room["objects"].remove(item)
        print(f"You take the {objects_list[item]['name'][0]}")
    else:
        print("No item to take.")
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


# Prints out the current items in the inventory.
def inventory():
    print("Inventory: " + str(inventory_list["objects"]))
    return current_room


# Description of the object.
def look_at(item):
    item = item_convert(item)
    print(objects_list[item]["desc"])
    return current_room


print()
print("While you were going about your day, you were abducted and dropped off at an unknown location.")
print("You feel the car stop and the driver leaves you with a letter before driving off in the distance.")
print("It reads: “Hello Player, I hope this letter finds you well.")
print(
    "As my last remaining kin, I have left you the entirety of my fortune, which includes the mansion you currently stand at.")
print(
    "Inside, I hope you’ll find, decipher, and solve the clues I’ve left behind, to which will truly determine whether or not you are worthy of the Lehane family legacy.")
print("Prevail, and you shall inherit it all; fail, and you will return to what you once were.")
print()

print("\nYou enter the " + current_room['roomName'] + ".")
print(current_room['shortDesc'])
while looping:

    # print(current_room['longDesc'])
    # print("Room items: " + str(current_room['objects']))

    player_input = input(">").lower()
    if player_input == "quit":
        looping = quit_game()
    else:
        current_room = parse(player_input)
