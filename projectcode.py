class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color):
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

name = input("What is your name?")
if name == "":
    name = input("Please enter a name. What is your name?")
appearance = input("Do you identify as male, female, or nonbinary?")
appearance_list = ["male", "female", "nonbinary"]
if appearance not in appearance_list:
    appearance = input("Please pick one of the options. Do you identify as male, female, or nonbinary?")
eye_color = input("Are your eyes brown, green, blue, or red?")
eye_color_list = ["brown", "green", "blue", "red"]
if eye_color not in eye_color_list:
    eye_color = input("Please pick one of the options. Are your eyes brown, green, blue, or red?")
hair_color = input("Is your hair brown, green, blue, red, black, or white?")
hair_color_list = ["brown", "green", "blue", "red", "black", "white"]
if hair_color not in hair_color_list:
    hair_color = input("Please pick one of the options. Is your hair brown, green, blue, red, black, or white?")