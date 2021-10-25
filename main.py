# Marvin's Mystery Mansion

import json

room_data_list = []

room_json_file = open("1.json")
room_data_list.push(json.load(room_json_file))
room_json_file.close()

room_json_file = open("2.json")
room_data_list.push(json.load(room_json_file))
room_json_file.close()

room_json_file = open("3.json")
room_data_list.push(json.load(room_json_file))
room_json_file.close()

room_json_file = open("4.json")
room_data_list.push(json.load(room_json_file))
room_json_file.close()

room_json_file = open("5.json")
room_data_list.push(json.load(room_json_file))
room_json_file.close()

room_json_file = open("6.json")
room_data_list[5] = json.load(room_json_file)
room_json_file.close()

current_room_data = room_data_list[0]


def go(direction):
    if direction in current_room_data["exits"]:
        return room_data_list[ current_room_data["exits"][direction]-1]
    else:
        print("There is no exit " + direction)




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
    print("\nYou enter the " + current_room_data['roomName'] + ".")
    print(current_room_data['shortDesc'])
    print(current_room_data['longDesc'])

    player_input = input(">")

    if player_input == "go north":
        current_room_data = go("north")
    elif player_input == "go east":
        room_data = go("east")
    elif player_input == "go west":
        room_data = go("west")
    elif player_input == "go south":
        room_data = go("south")
