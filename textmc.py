"""This is the terminal-based customization code.
It relies on classes used in projectcode.py, so it can't run on its own, but it's more convenient to store it here."""

#opening
print("Welcome to Fire Emblem: Let's Get This Bread.")
input("Press ENTER to begin.")
print("")

#character customization
name = input("What is your name? ")
while True:
    if name == "":
        name = input("Please enter a name. What is your name? ")
    else:
        break
appearance = input("Do you identify as male, female, or nonbinary? ")
appearance_list = ["male", "female", "nonbinary"]
while True:
    if appearance not in appearance_list:
        appearance = input("Please pick one of the options. Do you identify as male, female, or nonbinary? ")
    else:
        break
eye_color = input("Are your eyes brown, green, blue, or red? ")
eye_color_list = ["brown", "green", "blue", "red"]
while True:
    if eye_color not in eye_color_list:
        eye_color = input("Please pick one of the options. Are your eyes brown, green, blue, or red? ")
    else:
        break
hair_color = input("Is your hair brown, green, blue, red, black, or white? ")
hair_color_list = ["brown", "green", "blue", "red", "black", "white"]
while True:
    if hair_color not in hair_color_list:
        hair_color = input("Please pick one of the options. Is your hair brown, green, blue, red, black, or white? ")
    else:
        break
weapon = input("Do you use a sword, lance, axe, tome, dragonstone, bow, or dagger? ")
weapon_list = ["sword", "lance", "axe", "bow", "dagger", "dragonstone", "tome"]
while True:
    if weapon not in weapon_list:
        weapon = input("Please pick one of the options. Do you use a sword, lance, axe, tome, dragonstone, bow, or dagger? ")
    else:
        break
if weapon == "sword":
    print("A sword is a RED weapon.")
    color = "red"
elif weapon == "lance":
    print("A lance is a BLUE weapon.")
    color = "blue"
elif weapon == "axe":
    print("An axe is a GREEN weapon.")
    color = "green"
elif weapon == "bow" or weapon == "dagger" or weapon == "dragonstone":
    color = input(f"A {weapon} can be colorless, red, blue, or green. What color is your {weapon}? ")
    color_list = ["red", "blue", "green", "colorless"]
    while True:
        if color not in color_list:
            color = input(f"Please pick one of the options. Is your {weapon} colorless, red, blue, or green? ")
        else:
            break
elif weapon == "tome":
    color = input("A tome can be red, blue, or green. What color is your tome? ")
    color_list = ["red", "blue", "green"]
    while True:
        if color not in color_list:
            color = input("Please pick one of the options. Is your tome red, blue, or green? ")
        else:
            break
mc = Player(name, appearance, eye_color, hair_color, weapon, color)
#equip weapons
if weapon == "sword" or weapon == "lance" or weapon == "axe":
    input(f"You received an Iron {mc.weapon.title()}.")
    if weapon == "sword":
        iron_sword.equip()
    elif weapon == "lance":
        iron_lance.equip()
    elif weapon == "axe":
        iron_axe.equip()
elif weapon == "bow":
    input("You received an Iron Bow.")
    iron_bow.equip()
elif weapon == "dagger":
    input("You received an Iron Dagger.")
    iron_dagger.equip()
elif weapon == "dragonstone":
    input(f"You received a {mc.color} dragonstone. It allows you to use Fire Breath.")
    fire_breath.equip()
elif weapon == "tome":
    print(f"You received a {mc.color} tome.")
    if color == "red":
        input("It can cast a Fire spell.")
        fire_tome.equip()
    elif color == "blue":
        input("It can cast a Light spell.")
        light_tome.equip()
    elif color == "green":
        input("It can cast a Wind spell.")
        wind_tome.equip()
print("")

#tutorial scene
input(f"ANNA: Good morning, {mc.name}!")
input("ANNA: Are you ready to start fighting the forces of Brioche? ")
input("ANNA: That's the spirit. Let's get started.")
print("")
input("ANNA: That's a Roll Imp.") #insert arrow pointing at Roll Imp
input("ANNA: The Roll Imp has a lance, which is a BLUE weapon. Keep the weapon-triangle advantages in mind when you attack enemies.")
input("ANNA: BLUE weapons are effective against RED weapons, which are effective against GREEN weapons, which are in turn effective against BLUE weapons.")

#print("ANNA: Alright! Let's get this bread!")