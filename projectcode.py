#this is the text-based form of "Fire Emblem: Let's Get This Bread"
class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color, weapon, color):
        self.name = name
        self.appearance = appearance
        if self.appearance == "male":
            self.he = "he"
            self.his = "his"
            self.him = "him"
        if self.appearance == "female":
            self.he = "she"
            self.his = "her"
            self.him = "her"
        if self.appearance == "nonbinary":
            self.he = "they"
            self.his = "their"
            self.him = "them"
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.weapon = weapon
        self.color = color
#change base stats later
        self.hp = 10 #health
        self.a = 8 #attack
        self.d = 3 #defense
        self.res = 2 #resistance
        self.spd = 5 #speed

class Foe:
    """The class for the enemies."""
    def __init__(self, name, weapon, color, hp, a, d, res, spd):
        self.name = name
        self.weapon = weapon
        self.color = color
        self.hp = hp
        self.a = a
        self.d = d
        self.res = res
        self.spd = spd
roll_imp = Foe("Roll Imp", "lance", "blue", 13, 5, 4, 2, 5) #balance later

#opening
print("Welcome to Fire Emblem: Let's Get This Bread.")
input("Press ENTER to begin.")

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
weapon = input("Do you use a sword, lance, axe, tome, dragon stone, bow, or dagger? ")
weapon_list = ["sword", "lance", "axe", "bow", "dagger", "dragon stone", "tome"]
while True:
    if weapon not in weapon_list:
        weapon = input("Please pick one of the options. Do you use a sword, lance, axe, tome, dragon stone, bow, or dagger? ")
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
elif weapon == "bow" or weapon == "dagger" or weapon == "dragon stone":
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

#tutorial scene
input(f"ANNA: Good morning, {mc.name}!")
input("ANNA: Are you ready to start fighting the forces of Brioche? ")
input("ANNA: That's the spirit. Let's get started.")
print("")
input("ANNA: That's a Roll Imp.") #insert arrow pointing at Roll Imp

#print("ANNA: Alright! Let's get this bread!")