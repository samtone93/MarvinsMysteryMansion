# Helper functions that have specific uses or functions outside of main verbs

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
