import random

# Helper functions that have specific uses or functions outside of main verbs
harvey_chats = [
    "You: Hello! \nHarvey: Oh hello there! Marvin's told me so much about you & we're excited to have you at the mansion. \nHarvey: My name is Harvey, I was Marvin's great friend and house manager. \nHarvey: Please let me know if you have questions as you explore and discover new things in the mansion!",
    "You: Do you know what this recipe book is? \nHarvey: Where on earth did you find this!? \nHarvey: Marvin was such an incredible cook and taught me most of what I know about cooking - he kept this custom recipe book to share his most prized recipes. \nHarvey: His favorite recipe of them all was for Chicken Pot Pie. I've got it cooking in the oven for the remaining staff right now!",
    "You: Excuse me - but who is the family in this photo? \nHarvey: Oh how sweet. This is an old picture of Marvin & his beloved parents, Julie and John, in front of this very mansion. \nHarvey: This is from the very day they bought this mansion when Marvin was only about 7 years old. \nHarvey: I never got to meet his folks, but he always spoke so fondly of them.",
    "You: Excuse me - Do you know who this couple is in this wedding photo? \nHarvey: Oh you don't recognize him! That's Marvin himself with his beautiful bride, Melinda. \nHarvey: She passed just after they had your mother. The family doesn't speak of her often, as Marvin spent years heart broken after losing her.",
    "You: Excuse me - I couldn't help put notice this beautiful mountain picture. Could you tell me more? \nHarvey: Oh yes. This is the last vacation Marvin took before passing. It's from the Alps. \nHarvey: I believe this is where he met his beloved Melinda while studying abroad. He always spoke of getting back there before he himself passed.",
    "You: Thanks for chatting! \nHarvey: Goodbye! Let me know if you need anything!"
]


greg_chats = [
    "You: Hello! \nGreg: Welcome! You must be Marvin's grandchild. Harvey mentioned you'd be poking around. \nGreg: I'm Greg, and I've helped Marvin tend the garden for years. He was a curious old man, but so kind to all of us on staff. \nGreg: I'm quite busy cleaning up around the greenhouse, but let me know if you need anything, okay?",
    "You: Excuse me, but did you drop this over by the plants? \nGreg: Hmm. That looks like Marvin's handwriting. He was always making to-do lists and also always forgetting them places ironcially. \nGreg: We always had to plant things by the half dozen. That's why the entire list calls for 6 of everything. Not sure why, but Marvin liked it that way",
    "You: Thanks for chatting! \nGreg: Come grab me if you need anything. I'll be working here in the greenhouse!"
]


def uncover_vase(room):
    """Uncover the vase in the Art Gallery"""
    if "blue_sheet_covering_vase" in room["objects"]:
        room["objects"].remove("blue_sheet_covering_vase")
        room["objects"].append("blue_sheet")
        room["objects"].append("vase")
        room["longDesc"] = "You see a long rectangular room with maroon colored walls. Framed paintings and portraits line the walls. You notice a majority feature lions in various art styles.\nThere is a tall white vase in the corner. There is a long dimly lit hallway leading to the north. On the south wall are huge double brass doors with polished long golden handles."


def smash_vase(room):
    """Smash the vase in the Art Gallery"""
    if "vase" in room["objects"]:
        room["objects"].remove("vase")
        room["objects"].append("piano_bench_doodle")
        print("You smash the vase by tipping it over forcefully. It shatters completely, revealing a piece of paper from inside the vase.")
        print("It was a hand drawn doodle of a piano bench. What could it mean? And where could you have seen it?")
        room["longDesc"] = "You see a long rectangular room with maroon colored walls. Framed paintings and portraits line the walls. You notice a majority feature lions in various art styles.\nThe remains of a shattered vase can be seen in the corner. There is a long dimly lit hallway leading to the north. On the south wall are huge double brass doors with polished long golden handles."

def harvey_chat(curr_inventory):
    talking = True
    while talking:
        option = 0
        option_list = [0]
        # creates list of all options for user to talk about
        print("\nWhat would you like to talk to Harvey about?")
        print("Type '" + str(option) + "': Say hello")
        option = option + 1
        item_ct = 1
        # specifically checks for added talking points if certain items are in the inventory
        for item in ["recipe_book","family_photo","wedding_photo","mountain_photo"]:
            if item in curr_inventory:
                option_list.append(item_ct)
                print("Type '" + str(option) + "': Ask about " + item.replace("_", " "))
                option = option + 1
            item_ct = item_ct + 1
        print("Type '" + str(option) + "': Say goodbye")
        option_list.append(5)
        # takes the user input & tests it
        player_input = input(">").lower()
        if player_input.isnumeric() and int(player_input) <= option:
            print(harvey_chats[option_list[int(player_input)]])
            if option_list[int(player_input)] == 5:
                talking = False
        else:
            print("Sorry - that's not a valid input between 0 and " + str(option) + ". Please try again!")


def greg_chat(curr_inventory):
    talking = True
    while talking:
        option = 0
        option_list = [0]
        # creates list of all options for user to talk about
        print("\nWhat would you like to talk to Greg about?")
        print("Type '" + str(option) + "': Say hello")
        option = option + 1
        item_ct = 1
        # specifically checks for added talking points if certain items are in the inventory
        for item in ["todo_list"]:
            if item in curr_inventory:
                option_list.append(item_ct)
                print("Type '" + str(option) + "': Ask about " + item.replace("_", " "))
                option = option + 1
            item_ct = item_ct + 1
        print("Type '" + str(option) + "': Say goodbye")
        option_list.append(2)
        # takes the user input & tests it
        player_input = input(">").lower()
        if player_input.isnumeric() and int(player_input) <= option:
            print(greg_chats[option_list[int(player_input)]])
            if option_list[int(player_input)] == 2:
                talking = False
        else:
            print("Sorry - that's not a valid input between 0 and " + str(option) + ". Please try again!")


def play_pc():
    while True:
        print("\nEnter the correct code to continue: ")
        print("There are three numbers to the code, each ranging from 1 to 5.\n")

        code_a = random.randint(1, 5)
        code_b = random.randint(1, 5)
        code_c = random.randint(1, 5)
        code_sum = code_a + code_b + code_c
        code_prod = code_a * code_b * code_c

        print("The sum of the numbers is " + str(code_sum))
        print("The product of the numbers is " + str(code_prod) + "\n")
        print("Type \'exit\' to give up.")
        print("Please enter three numbers separated by spaces.")
        code_input = input(">").lower().split()

        if code_input[0] == 'exit':
            print("You've given up for now.")
            break
        # Check for three valid integers
        if len(code_input) == 3 and code_input[0].isnumeric() and code_input[1].isnumeric() and code_input[2].isnumeric():
            guess_a = int(code_input[0])
            guess_b = int(code_input[1])
            guess_c = int(code_input[2])

            guess_sum = guess_a + guess_b + guess_c
            guess_prod = guess_a * guess_b * guess_c

            if guess_sum == code_sum and guess_prod == code_prod:
                print("Correct! For your quick wit, you are awarded with the number 1950.")
                print("The program exits.\n")
                break
            else:
                print("Wrong! The code has changed.\n")
        else:
            print("Invalid input - you didn't enter 3 numbers! The code has changed.\n")
