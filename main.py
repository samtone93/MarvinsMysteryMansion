# Marvin's Mystery Mansion

import json
from regex_filter import filter_prep
from helper_functions import uncover_vase, harvey_chat, greg_chat, play_pc

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
    # remove prepositions, filter input string, and split into list
    input_list = filter_prep(input_command, current_room["exits"])

    # get verb
    verb = ""
    for action in action_list:
        for alias in action_list[action]["aliases"]:
            if alias in input_list[0]:
                verb = action

    # remove verb from input
    if verb == "":
        print("That is an unrecognized command. Sorry, try again")
        return current_room
    else:
        input_list.remove(input_list[0])

    # create argument
    argument = ""
    while len(input_list) > 0:
        argument = argument + input_list[0]
        input_list.remove(input_list[0])
        if len(input_list) > 0:
            argument = argument + " "

    if argument == "" and not action_list[verb]["takes_arg"]:
        return eval(verb + "()")
    elif argument != "" and action_list[verb]["takes_arg"]:
        return eval(verb + "(\"" + argument + "\")")
    else:
        print("Command not understood. Try again")
        return current_room


# Converts item to be usable
def item_convert(item_str):
    item = ""
    for key in objects_list:
        for name in objects_list[key]["name"]:
            if name == item_str and (key in current_room["objects"] or key in inventory_list["objects"]):
                item = key
    return item


# checks the room for the item & ability to use verb on that item
# where specifies if item can only be in inventory, room, or both
def obj_check(item, verb, where):
    if item == '':
        print("Item not available - try again")
        return False
    if verb == "look_at" and (item in current_room["objects"] or item in inventory_list["objects"]):
        return True
    if where == "both" and (item in current_room["objects"] or item in inventory_list["objects"]) and verb in objects_list[item]["actions"]:
        return True
    elif where == "inventory" and item in inventory_list["objects"] and verb in objects_list[item]["actions"]:
        return True
    elif where == "room" and item in current_room["objects"] and verb in objects_list[item]["actions"]:
        return True
    elif verb in objects_list[item]["actions"]:
        if where == "both":
            where = "room or inventory"
        print(objects_list[item]["name"][0] + " is not present in " + where + " - " + verb + " cannot be performed")
        return False
    else:
        print(verb + " is not a valid action for " + objects_list[item]["name"][0] + " - try again")
        return False


# Handles both directions & entryways
# Edit room files to include aliases for entryways under "exits"
def go(argument):
    if argument in current_room["exits"]:
        new_data = room_data_list[current_room["exits"][argument][0]]
        print("\nYou enter the " + new_data["roomName"] + ".")
        if new_data["firstEntry"]:
            print(new_data["longDesc"])
            new_data["firstEntry"] = False
        else:
            print(new_data["shortDesc"])
    else:
        print("You cannot go there.")
        new_data = current_room
    return new_data


# Object removed from inventory, placed in room.
def put(item):
    item = item_convert(item)
    if obj_check(item, "put", "inventory"):
        current_room["objects"].append(item)
        inventory_list["objects"].remove(item)
        print("You put down the " + objects_list[item]['name'][0])
    return current_room


# Object removed from room, placed in inventory.
def take(item):
    item = item_convert(item)
    if obj_check(item, "take", "room"):
        inventory_list["objects"].append(item)
        current_room["objects"].remove(item)
        print("You take the "+ objects_list[item]['name'][0])
        if item in ["house_manager_memo","recipe_book"]:
            if objects_list[item]["take"] in current_room["objects"]:
                current_room["objects"].remove(objects_list[item]["take"])
                current_room["objects"].append(("empty_" + objects_list[item]["take"]))
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
    if obj_check(item, "look_at", "both"):
        print(objects_list[item]["desc"])
    return current_room


# Play the game on the PC
def play(item):
    item = item_convert(item)
    if obj_check(item, "play", "room"):
        if item == "pc":
            play_pc()
    return current_room


# Smash the 1950 wine bottle in the wine cellar for the album key
def smash(item):
    item = item_convert(item)
    if obj_check(item, "smash", "inventory"):
        if item == "wine_1950":
            print("You smash the 1950 wine bottle open.")
            inventory_list["objects"].remove(item)
            print("You find a large key of sorts was inside.")
            for object in objects_list:
                if object == "master_key":
                    inventory_list["objects"].append(object)
    return current_room


# Unlock the album in the garage and obtain "Marvin's Manifesto"
# Reading the Manifesto ends the game.
def unlock(item):
    item = item_convert(item)
    if obj_check(item, "unlock", "room"):
        if item == "master_chest":
            if "master_key" in inventory_list["objects"]:
                print(objects_list[item]["unlock"])
                for object in objects_list:
                    if object == "marvin_manifesto":
                        inventory_list["objects"].append(object)
                        return current_room
            else:
                print("You can't unlock the album without a key.")
        elif obj_check(item, "unlock", "room") and item == "combo_lock":
            locked = True
            print("You look at the combo lock and begin to decode it:")
            # while locked == True -> while locked:
            while locked:
                print("Type 3 numbers from 0-39 with spaces (i.e. '1 2 3') to attempt unlocking or 'leave' to exit")
                player_input = input(">").lower()
                if player_input == 'leave':
                    print("You've given up & headed back to the Greenhouse")
                    break
                input_list = player_input.split()
                if len(input_list) != 3:
                    print("Invalid input - you didn't enter 3 numbers")
                else:
                    num_list = []
                    for num in input_list:
                        # combined two and statements; 0<=num and num>= 39 -> 0 <= num <= 39
                        if num.isnumeric() and (0 <= int(num) <= 39):
                            num_list.append(int(num))
                        else:
                            print("Invalid number: " + num + " is not in the range 0-39")
                            num_list.append(40)
                    if num_list[0] == 32 and num_list[1] == 17 and num_list[2] == 6:
                        locked = False
                        current_room["objects"].remove("combo_lock")
                        print(objects_list[item]["unlock"])
                    else:
                        print("Wrong combination - please try again")
    return current_room
    
    
def pull(item):
    item = item_convert(item)
    if obj_check(item, "pull", "room"):
        print(objects_list[item]["pull"])
        if item == "lion_hook" and "locked_foyer_chest" in current_room["objects"]:
            current_room["objects"].remove("locked_foyer_chest")
            current_room["objects"].append("unlocked_foyer_chest")
        elif item == "shag_rug" and ("house_manager_memo" in current_room["objects"] or "house_manager_memo" in inventory_list["objects"]) == False:
            current_room["objects"].append("house_manager_memo")
    return current_room


def uncover(item):
    item = item_convert(item)
    if obj_check(item, "uncover", "room"):
        new_item = "un" + item
        current_room["objects"].remove(item)
        current_room["objects"].append(new_item)
        print("You've revealed a new item:")
        print(objects_list[new_item]["desc"])
    return current_room


def pry(item):
    item = item_convert(item)
    if obj_check(item, "pry", "room"):
        if "crowbar" in inventory_list["objects"]:
            print(objects_list[item]["pry"])
            if item == "nailed_boards":
                current_room["objects"].remove(item)
        else:
            print("You try prying the " + objects_list[item]["name"][0] + " with your hands and fail")
            print("Hmm... Perhaps you should find a tool, such as a crowbar, to pry this item")
    return current_room


def open(item):
    item = item_convert(item)
    if obj_check(item, "open", "room"):
        print(objects_list[item]["open"])
        if item == "unlocked_foyer_chest" and ("recipe_book" in current_room["objects"] or "recipe_book" in inventory_list["objects"]) == False:
            current_room["objects"].append("recipe_book")
    return current_room


def talk(item):
    item = item_convert(item)
    if obj_check(item, "talk", "room"):
        if item == "house_manager":
            harvey_chat(inventory_list["objects"])
        elif item == "groundskeeper":
            greg_chat(inventory_list["objects"])
    return current_room
    
    
# Help shows the user all the actions in the game & a short description of what they do
def help():
    for verb in action_list:
        print(verb + ": (other inputs: " + str(action_list[verb]["aliases"]) + ")")
        print("  " + action_list[verb]["description"])
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
print(current_room['longDesc'])
while looping:

    # print(current_room['longDesc'])
    # print("Room items: " + str(current_room['objects']))

    player_input = input(">").lower()
    if player_input == "quit":
        looping = quit_game()
    else:
        current_room = parse(player_input)
