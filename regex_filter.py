# RUN regex_filter.py. It will loop asking for input, and print out filtered string result. Type exit to end loop

import re


# looping = True


def filter_prep(pi, exits):
    """pi stands for player input"""
    # if there is look at, replace with look_at so not to filter out
    pi = re.sub("look at", "look_at", pi)

    # same for press_button
    pi = re.sub("press button", "press_button", pi)
    pi = re.sub("push button", "press_button", pi)

    # and climb up and down
    if re.match("climb down", pi):
        pi = "climb down"
    pi = re.sub("climb up", "climb", pi)

    # find and sub out articles/prepositions
    # filters out: a, an, at, by, for, from, in, of, off, on, out, that, the, to, toward, towards, with
    pi = re.sub(
        r"\bthe\b|\bin\b|\bto\b|\baway\b|\ba\b|\ban\b|\bby\b|\bfor\b|\bon\b|\bfrom\b|\bof\b|\bout\b|\bwith\b|\bat\b|"
        r"\btoward\b|\btowards\b|\bthat\b|\boff\b",
        "",
        pi)

    # convert double or more spaces to single space
    pi = re.sub(r"\s\s+", " ", pi)

    # If string starts with a space, remove it
    whitespace_search = re.search("\s", pi)
    if whitespace_search:
        if whitespace_search.start() == 0:
            pi = re.sub("\s", "", pi, 1)

        # Remove trailing space ending a string
        reversed_pi = pi[::-1]
        reversed_search = re.search("\s", reversed_pi)
        if reversed_search:
            if reversed_search.start() == 0:
                pi = re.sub("\s", "", reversed_pi, 1)

    if pi in exits or pi in ["north", "south", "east", "west"]:
        pi = "go " + pi

    return pi.split()

# while looping:
#     player_input = input(">").lower()
#     filtered_str = filter_prep(player_input)
#     print(filtered_str)
#     if player_input == "exit":
#         looping = False
