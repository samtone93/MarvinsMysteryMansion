# Marvin's Mystery Mansion

import json

room_json_file = open("11.json")

room_data = json.load(room_json_file)
room_json_file.close()


def go(data, direction):
    if direction in data["exits"]:
        json_file = open(str(data["exits"][direction]) + ".json")
        new_data = json.load(json_file)
        json_file.close()
    else:
        print("There is no exit " + direction)
        new_data = data

    return new_data


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
    print("\nYou enter the " + room_data['roomName'] + ".")
    print(room_data['shortDesc'])
    print(room_data['longDesc'])

    player_input = input(">")

    if player_input == "go north":
        room_data = go(room_data, "north")
    elif player_input == "go east":
        room_data = go(room_data, "east")
    elif player_input == "go west":
        room_data = go(room_data, "west")
    elif player_input == "go south":
        room_data = go(room_data, "south")
