# Marvin's Mystery Mansion

import json

room = open("11.json")

data = json.load(room)


def go(curr_room, direction):
    if curr_room["exits"][direction]:
        return str(curr_room["exits"][direction]) + ".json"

print()
print("While you were going about your day, you were abducted and dropped off at an unknown location.")
print("You feel the car stop and the driver leaves you with a letter before driving off in the distance.")
print("It reads: “Hello <Player>, I hope this letter finds you well.")
print("As my last remaining kin, I have left you the entirety of my fortune, which includes the mansion you currently stand at.")
print("Inside, I hope you’ll find, decipher, and solve the clues I’ve left behind, to which will truly determine whether or not you are worthy of the Lehane family legacy.")
print("Prevail, and you shall inherit it all; fail, and you will return to what you once were.")
print()

while True:

    print("You enter the " + data['roomName'] + ".")
    print(data['shortDesc'])
    print(data['longDesc'])
    
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
