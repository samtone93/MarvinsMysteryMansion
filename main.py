# Marvin's Mystery Mansion

import json

room = open("1.json")

data = json.load(room)


def go(curr_room, direction):
    if curr_room["exits"][direction]:
        return str(curr_room["exits"][direction]) + ".json"


print("Welcome")

while True:

    player_input = input(">")

    if player_input == "go north":
        room = open(go(data, "north"))
    elif player_input == "go east":
        room = open(go(data, "east"))
    elif player_input == "go west":
        room = open(go(data, "west"))
    elif player_input == "go south":
        room = open(go(data, "south"))

    data = json.load(room)
    room.close()
    print(data['roomName'])