# Marvin's Mystery Mansion

import json
from regex_filter import filter_prep
from helper_functions import uncover_vase, harvey_chat, greg_chat, play_pc, smash_vase, load_projector, unlock_exit, locked_exit_output, unlock_combo

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

room_data_list = [inventory_list]

for num in range(1, 16):
    room_num = str(num)
    room_json_file = open(room_num + ".json")
    room_data = json.load(room_json_file)
    room_json_file.close()
    room_data_list.append(room_data)

current_room = room_data_list[6]


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
            if name == item_str and (key in current_room["objects"] or key in room_data_list[0]["objects"]):
                item = key
    return item


# checks the room for the item & ability to use verb on that item
# where specifies if item can only be in inventory, room, or both
def obj_check(item, verb, where):
    if item == '':
        print("Item not available - try again")
        return False
    if verb == "look_at" and (item in current_room["objects"] or item in room_data_list[0]["objects"]):
        return True
    if where == "both" and (item in current_room["objects"] or item in room_data_list[0]["objects"]) and verb in \
            objects_list[item]["actions"]:
        return True
    elif where == "inventory" and item in room_data_list[0]["objects"] and verb in objects_list[item]["actions"]:
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
    if argument in current_room["exits"] and current_room["exits"][argument][1] == 0:
        new_data = room_data_list[current_room["exits"][argument][0]]
        print("\nYou enter the " + new_data["roomName"] + ".")
        if new_data["firstEntry"]:
            print(new_data["longDesc"])
            new_data["firstEntry"] = False
        else:
            print(new_data["shortDesc"])
    elif argument in current_room["exits"] and current_room["exits"][argument][1] == 1:
        locked_exit_output(current_room["exits"][argument][0])
        new_data = current_room
    else:
        print("You cannot go there.")
        new_data = current_room
    return new_data


# Object removed from inventory, placed in room.
def put(item):
    item = item_convert(item)
    if obj_check(item, "put", "inventory"):
        current_room["objects"].append(item)
        room_data_list[0]["objects"].remove(item)
        print("You put down the " + objects_list[item]['name'][0])
    return current_room


# Object removed from room, placed in inventory.
def take(item):
    item = item_convert(item)
    if obj_check(item, "take", "room"):
        room_data_list[0]["objects"].append(item)
        current_room["objects"].remove(item)
        print("You take the " + objects_list[item]['name'][0])
        if item in ["house_manager_memo", "recipe_book", "film_reel"]:
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
    print("Inventory: " + str(room_data_list[0]["objects"]))
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
    if obj_check(item, "smash", "room") and item == "uncovered_vase":
        smash_vase(current_room)
        take("piano bench doodle")
        return current_room

    if obj_check(item, "smash", "inventory"):
        if item == "wine_1950":
            print("You smash the 1950 wine bottle open.")
            room_data_list[0]["objects"].remove(item)
            print("You find a large key of sorts was inside.")
            for object in objects_list:
                if object == "master_key":
                    room_data_list[0]["objects"].append(object)
    return current_room


# Unlock the album in the garage and obtain "Marvin's Manifesto"
# Reading the Manifesto ends the game.
def unlock(item):
    item = item_convert(item)
    if obj_check(item, "unlock", "room"):
        if item == "master_chest":
            if "master_key" in room_data_list[0]["objects"]:
                print(objects_list[item]["unlock"])
                for object in objects_list:
                    if object == "marvin_manifesto":
                        room_data_list[0]["objects"].append(object)
                        return current_room
            else:
                print("You can't unlock the album without a key.")
        elif obj_check(item, "unlock", "room") and item == "combo_lock":
            locked = unlock_combo()
            if not locked:
                current_room["objects"].remove("combo_lock")
                print(objects_list[item]["unlock"])
                return unlock_exit(current_room, 5)
    return current_room


def pull(item):
    item = item_convert(item)
    if obj_check(item, "pull", "room"):
        print(objects_list[item]["pull"])
        if item == "lion_hook" and "locked_foyer_chest" in current_room["objects"]:
            current_room["objects"].remove("locked_foyer_chest")
            current_room["objects"].append("unlocked_foyer_chest")
        elif item == "shag_rug" and (
                "house_manager_memo" in current_room["objects"] or "house_manager_memo" in room_data_list[0][
            "objects"]) == False:
            current_room["objects"].append("house_manager_memo")
    return current_room


# Press the button on piano bench
def press_button():
    if obj_check("piano_bench", "press_button", "room"):
        print("You press the button on the piano bench, and the cushioned top opens and swings up to reveal the storage space underneath inside the bench.")
        print("There is a film reel stored in the space.")
        current_room["objects"].remove("piano_bench")
        current_room["objects"].append("opened_piano_bench")
        current_room["objects"].append("film_reel")
    else:
        print("There's no button to press")
    return current_room


# Load object
def load_object(item):
    item = item_convert(item)
    if item == "empty_projector" and obj_check(item, "load_object", "room"):
        if "film_reel" in room_data_list[0]["objects"]:
            load_projector(current_room)
            room_data_list[0]["objects"].remove("film_reel")
        else:
            print("There is nothing to load the projector with")
    else:
        print("Nothing to load")
    return current_room


# Uncover an item
def uncover(item):
    item = item_convert(item)
    if obj_check(item, "uncover", "room"):
        new_item = "un" + item
        current_room["objects"].remove(item)
        current_room["objects"].append(new_item)
        if new_item == "uncovered_vase":
            uncover_vase(current_room)
        else:
            print("You've revealed a new item:")
            print(objects_list[new_item]["desc"])
    return current_room


def pry(item):
    item = item_convert(item)
    if obj_check(item, "pry", "room"):
        if "crowbar" in room_data_list[0]["objects"]:
            print(objects_list[item]["pry"])
            if item == "nailed_boards":
                current_room["objects"].remove(item)
                return unlock_exit(current_room, 6)
        else:
            print("You try prying the " + objects_list[item]["name"][0] + " with your hands and fail")
            print("Hmm... Perhaps you should find a tool, such as a crowbar, to pry this item")
    return current_room


def open_object(item):
    item = item_convert(item)
    if obj_check(item, "open_object", "room"):
        print(objects_list[item]["open"])
        if item == "unlocked_foyer_chest" and (
                "recipe_book" in current_room["objects"] or "recipe_book" in room_data_list[0]["objects"]) == False:
            current_room["objects"].append("recipe_book")
    return current_room


def talk(item):
    item = item_convert(item)
    if obj_check(item, "talk", "room"):
        if item == "house_manager":
            harvey_chat(room_data_list[0]["objects"])
        elif item == "groundskeeper":
            greg_chat(room_data_list[0]["objects"])
    return current_room


def read_object(item):
    item = item_convert(item)
    if obj_check(item, "read", "both"):
        print(objects_list[item]["read"])
        if item == "gardening_book":
            current_room["objects"].append("family_letter")
            if item in current_room["objects"]:
                current_room["objects"].remove(item)
                current_room["objects"].append("empty_gardening_book")
            elif item in room_data_list[0]["objects"]:
                room_data_list[0]["objects"].remove(item)
                room_data_list[0]["objects"].append("empty_gardening_book")
        # Read Marvin's Manifesto; print out game ending, ask player to continue or quit
        if item == "marvin_manifesto":
            #  quit the game after reading
            quit_game()
    return current_room


# Help shows the user all the actions in the game & a short description of what they do
def help():
    for verb in action_list:
        print(verb + ": (other inputs: " + str(action_list[verb]["aliases"]) + ")")
        print("  " + action_list[verb]["description"])
    return current_room


def savegame():
    data_list = room_data_list
    data_list.append(current_room)
    save_data_json = json.dumps(data_list)
    save_file = open("saved_data_file.json", "w")
    save_file.write(save_data_json)
    save_file.close()

    print("Game saved")
    return current_room


def loadgame():
    try:
        save_file = open("saved_data_file.json")
        save_data_list = json.load(save_file)

        new_curr_room = save_data_list.pop()
        room_data_list.clear()
        for room in save_data_list:
            room_data_list.append(room)

        # print("Loaded data:")
        # print(f"current room: #{new_curr_room}")
        # for i in room_data_list:
        #     print(i)

        print(f"\nYou are in the {new_curr_room['roomName']}")
        print(new_curr_room["longDesc"])
        print(f"\nYour inventory: {room_data_list[0]['objects']}")
    except FileNotFoundError:
        print("No saved game data")
        new_curr_room = current_room

    return new_curr_room


print("""
  __  __                  _       _       __  __           _                    __  __                 _             
 |  \/  |                (_)     ( )     |  \/  |         | |                  |  \/  |               (_)            
 | \  / | __ _ _ ____   ___ _ __ |/ ___  | \  / |_   _ ___| |_ ___ _ __ _   _  | \  / | __ _ _ __  ___ _  ___  _ __  
 | |\/| |/ _` | '__\ \ / / | '_ \  / __| | |\/| | | | / __| __/ _ \ '__| | | | | |\/| |/ _` | '_ \/ __| |/ _ \| '_ \ 
 | |  | | (_| | |   \ V /| | | | | \__ \ | |  | | |_| \__ \ ||  __/ |  | |_| | | |  | | (_| | | | \__ \ | (_) | | | |
 |_|  |_|\__,_|_|    \_/ |_|_| |_| |___/ |_|  |_|\__, |___/\__\___|_|   \__, | |_|  |_|\__,_|_| |_|___/_|\___/|_| |_|
                                                  __/ |                  __/ |                                       
                                                 |___/                  |___/                              
""")

print("\nWhile you were going about your day, you were abducted and dropped off at an unknown location.")
print("You feel the car stop and the driver leaves you with a letter before driving off in the distance.")
print("It reads:\n")
print(objects_list["will"]["read"])
print()

print("\nYou enter the " + current_room['roomName'] + ".")
print(current_room['longDesc'])
print()
while looping:

    # print(current_room['longDesc'])
    # print("Room items: " + str(current_room['objects']))

    player_input = input(">").lower()
    if player_input == "quit":
        looping = quit_game()
    else:
        current_room = parse(player_input)
        print("***FOR DEBUGGING***\nRoom Objects:", current_room["objects"])
        print()
