# Marvin's Mystery Mansion

import json
from regex_filter import filter_prep
from helper_functions import uncover_vase, harvey_chat, greg_chat, play_pc, smash_vase, load_projector, unlock_exit, locked_exit_output, unlock_combo
from helper_functions import take_ladder_room_revision, climbed_on_item_check, master_bedroom_key_take_check, ballroom_ladder_climb_event, master_bedroom_unlock_check
from helper_functions import game_intro, main_menu, new_game_screen, load_game_check

game_running = True
intro_needed = True

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

current_room = room_data_list[1]


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
    if "climbed_up_status" and "climbed_object" in current_room:
        print(f"\nYou have to climb down the {objects_list[current_room['climbed_object']]['name'][0]} first.")
        new_data = current_room
    elif argument in current_room["exits"] and current_room["exits"][argument][1] == 0:
        new_data = room_data_list[current_room["exits"][argument][0]]
        print("\nYou enter the " + new_data["roomName"] + ".")
        if new_data["firstEntry"]:
            print(new_data["longDesc"])
            new_data["firstEntry"] = False
        else:
            print(new_data["shortDesc"])
    elif argument in current_room["exits"] and current_room["exits"][argument][1] == 1:
        if master_bedroom_unlock_check(argument, current_room, room_data_list[0]["objects"]):  # Specific check to unlock room 11
            return go(argument)
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
        if item == "ladder":
            take_ladder_room_revision(current_room)
        if climbed_on_item_check(item, current_room):  # prevent taking item that is climbed on
            return current_room
        if master_bedroom_key_take_check(item, current_room, room_data_list[0]["objects"]):
            return current_room

        room_data_list[0]["objects"].append(item)
        current_room["objects"].remove(item)
        print("You take the " + objects_list[item]['name'][0])
        if item in ["house_manager_memo", "recipe_book", "film_reel", "cue_stick", "master_bedroom_key"]:
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
    print("Inventory:")
    for item in room_data_list[0]["objects"]:
        print(objects_list[item]['name'][0], end="   ")
    print()
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
            load_projector(current_room, room_data_list[6])
            room_data_list[0]["objects"].remove("film_reel")
        else:
            print("There is nothing to load the projector with")
    else:
        print("No object to load right now")
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


# Climbing up or down objects
def climb(item):
    if item == "down":
        if "climbed_up_status" in current_room:
            print(f"You climb down the {objects_list[current_room['climbed_object']]['name'][0]}.")
            current_room.pop("climbed_up_status")
            current_room.pop("climbed_object")
    else:
        item = item_convert(item)
        if obj_check(item, "climb", "room"):
            if "climbed_up_status" in current_room:
                print(f"You've already climbed up the {objects_list[item]['name'][0]}.")
            else:
                print("You climb up the " + objects_list[item]["name"][0])
                current_room["climbed_up_status"] = True
                current_room["climbed_object"] = item
                if current_room["roomName"] == "Ballroom" and item == "ladder":
                    ballroom_ladder_climb_event(current_room)

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
        saved_curr_room = save_data_list.pop()
        save_file.close()

        room_data_list.clear()
        for room in save_data_list:
            room_data_list.append(room)
        new_curr_room = room_data_list[saved_curr_room["room"]]

        print(f"\nYou are in the {new_curr_room['roomName']}")
        print(new_curr_room["longDesc"] + "\n")
        inventory()
    except FileNotFoundError:
        print("No saved game data")
        new_curr_room = current_room

    return new_curr_room


while game_running:
    looping = True
    if intro_needed:
        game_intro()
    main_menu()
    player_input = input(">").lower()
    
    if player_input == '0' or player_input == '1':
        if player_input == '0':
            new_game_screen(objects_list["will"]["read"], current_room['roomName'], current_room['longDesc'])
        else:
            if load_game_check():
                print("*** LOADING PREVIOUS GAME... ***\n")
                current_room = loadgame()
            else:
                print("No save file found.. Returning to main menu")
                looping = False
            
        while looping:
            player_input = input(">").lower()
            if player_input == "quit":
                looping = quit_game()
            else:
                current_room = parse(player_input)
                print()

    elif player_input == '2':
        print("Thanks for playing! Goodbye.")
        game_running = False
    else:
        print("I'm sorry, I do not understand that input. Let's try again.\n")
        intro_needed = False
