#the game is heavily based on Fire Emblem Heroes, the mobile game of the Fire Emblem series

import sys, pygame #import pygame to use
pygame.font.init() #initialize font module so font functions work

size = width, height = 500, 500 #define size as a certain px area
screen = pygame.display.set_mode(size) #create a Surface called "screen" with pygame (the screen the computer displays)

#define colors by name for convenience
black = (0, 0, 0) #rgb value of black
white = (250, 250, 250) #rgb value of white
fe_blue = (72, 117, 139) #color of Fire Emblem textboxes, midway between the gradient endpoints...ish

def opening_screen():
    """Draw the opening screen on the Surface."""
    bg = screen.convert()
    
    bg.fill(white) #the opening bg is white, for now
    
    #title words
    title_font = pygame.font.Font(None, 25) #title font is the default font at 25px size
    title_text = title_font.render("Fire Emblem: Let's Get This Bread", 1, black) #title text is antialiasing and black
    title_text_position = title_text.get_rect() #position of title text
    title_text_position.centerx = screen.get_rect().centerx #center of title text is center of the screen
    title_text_position.height = screen.get_rect().height / 2 #text is in the middle of the screen
    bg.blit(title_text, title_text_position) #draw title text at title_text_position

    #opening instructions
    font = pygame.font.Font(None, 15) #instructions are default font at 15px size
    text = font.render("Press any key to start.", 1, black)
    text_position = text.get_rect() #position of instructions
    text_position.centerx = screen.get_rect().centerx
    text_position.height = screen.get_rect().height / 3 #text is at 1/3 of the screen height
    bg.blit(text, text_position) #draw instructions at text_position

    screen.blit(bg, (0, 0)) #draw bg with text on screen

    while True: #event loop - start
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the Player tries to close the window...
                sys.exit()
            elif event.type == pygame.KEYDOWN: #if the Player presses a key...
                return

def mc_customize():
    """Customize the Player character using keyboard input."""

    bg = screen.convert()
    bg.fill(white)

    q_box = pygame.display.set_mode(500, 250) #question box is a separate surface
    box_bg = q_box.convert()
    box_bg.fill(fe_blue)

    question = "What is your name?" #change later; example
    #question text
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render(question, 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.centerx = screen.get_rect().centerx
    q_text_position.height = screen.get_rect().height / 2
    box_bg.blit(q_text, q_text_position)

opening_screen()

#test image stuff that can be worked out later
#marth_img = pygame.image.load("FEH_Marth.png").convert() #load image as surface
#while True:
    #screen.fill(black)
    #screen.blit(marth_img, (0,0))

#this is the text-based form of "Fire Emblem: Let's Get This Bread" so far

class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color, weapon, color, equipped=None):
        self.name = name.title()
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
        self.equipped = equipped
#base stats based on the first hero in Fire Emblem Heroes, Takumi, at 4 star rarity, except for range
        self.hp = 17 #health
        self.a = 8 #attack
        self.d = 5 #defense
        self.res = 4 #resistance
        self.spd = 7 #speed
        self.rng = 1 #range
        self.breadcrumbs = 0 #obtained breadcrumbs
        self.bread = 0 #obtained bread

class Foe:
    """The class for the enemies."""
    def __init__(self, name, weapon, color, hp, a, d, res, spd, rng, drop):
        self.name = name
        self.weapon = weapon
        self.color = color
        self.hp = hp
        self.a = a
        self.d = d
        self.res = res
        self.spd = spd
        self.rng = rng
        self.drop = drop #how many breadcrumbs are dropped by the enemy
roll_imp = Foe("Roll Imp", "lance", "blue", 18, 11, 6, 3, 5, 1, 10) #based on Blue Fighter, 1 star with Iron Lance
bun_dragon = Foe("Bun Dragon", "dragonstone", "green", 16, 13, 5, 4, 7, 1, 25) #based on Green Manakete, 2 star with Fire Breath
baguette_devil = Foe("Baguette Devil", "sword", "red", 18, 11, 6, 3, 5, 1, 10) #based on Sword Fighter, 1 star with Iron Sword
loaf_archer = Foe("Loaf Archer", "bow", "colorless", 17, 10, 5, 1, 5, 2, 10) #based on Bow Fighter, 1 star with Iron Bow

def get_bread(defeated):
    """Obtain breadcrumbs from defeating an enemy."""
    input(f"You received {defeated.drop} breadcrumbs.")
    mc.breadcrumbs += defeated.drop
    return

def breadify():
    """Convert breadcrumbs to bread."""
    converted = mc.breadcrumbs % 15 #how many whole breads can be made
    mc.breadcrumbs -= 15 * converted
    input(f"You received {converted} bread.")
    input(f"You now have {mc.breadcrumbs} breadcrumbs.")
    mc.bread += converted
    return

def check_bread():
    """Check how many breadcrumbs and how much bread the player has."""
    input(f"Breadcrumbs: {mc.breadcrumbs}")
    input(f"Bread: {mc.bread}")
    return

class Bread:
    """The class for the Fire Emblem characters with cutscenes."""
    def __init__(self, name, appearance, bread):
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
        self.bread = bread #how much bread is required to unlock their cutscene
marth = Bread("Marth", "male", 10)
groom_marth = Bread("Groom Marth", "male", 25)
hero_king_marth = Bread("Hero King Marth", "male", 50)
masked_marth = Bread("Masked Marth", "nonbinary", 75)
lucina = Bread("Masked Marth", "female", 50)

def unlock(character):
    """Unlock a character's cutscene."""
    if character.bread == 0:
        None #if character has already been unlocked, nothing happens
    elif mc.bread < character.bread:
        input(f"You don't have enough bread to unlock {character.name} yet.")
    elif mc.bread >= character.bread:
        input(f"{character.name} unlocked!")
        mc.bread -= character.bread
        input(f"You now have {mc.bread} bread.")
        character.bread = 0 #character's bread cost is now 0
    return

weapon_triangle = { #the value to each key is the color it has an advantage over
    "red": "green",
    "blue": "red",
    "green": "blue",
    "colorless": ""
    }
def advantage(attacker, defender):
    """Factor the weapon-triangle advantages into attacks."""
    if defender.color == weapon_triangle[attacker.color]:
        return 1.2 #20% increase for advantage
    elif attacker.color == weapon_triangle[defender.color]:
        return 0.8 #20% decrease for disadvantage
    else:
        return 1

physical_weapons = ["sword", "lance", "axe", "bow", "dagger"]
magic_weapons = ["tome", "dragonstone"]
def attack(attacker, defender):
    """The attacker attacks the defender."""
    if attacker.weapon in physical_weapons:
        dmg = attacker.a - defender.d
    if attacker.weapon in magic_weapons:
        dmg = attacker.a - defender.res
    dmg *= advantage(attacker, defender) #alter damage based on the weapon-triangle advantage multiplier
    if dmg > defender.hp:
        dmg = defender.hp
    if dmg <= 0:
        dmg = 0
    defender.hp -= dmg
    input(f"{defender.name} took {dmg} damage.")
    return

def check_defeat(defeated):
    """Check if a character has been defeated."""
    if defeated.hp == 0:
        return True
    else:
        return False

class Weapon:
    """The class for weapons that can be equipped by the Player."""
    def __init__(self, name, might, rng):
        self.name = name
        self.might = might
        self.rng = rng

    def equip(self):
        """Equip a weapon."""
        print(f"Equipped the {self.name}.")
        mc.a += self.might
        mc.rng = self.rng
        mc.equipped = self.name

    def unequip(self):
        """Unequip a weapon."""
        print(f"Unequipped the {self.name}.")
        mc.a -= self.might
        mc.equipped = None
        mc.rng = 1
iron_sword = Weapon("Iron Sword", 6, 1)
iron_lance = Weapon("Iron Lance", 6, 1)
iron_axe = Weapon("Iron Axe", 6, 1)
iron_bow = Weapon("Iron Bow", 4, 2)
iron_dagger = Weapon("Iron Dagger", 3, 2)
fire_breath = Weapon("Fire Breath", 6, 1)
fire_tome = Weapon("Fire", 4, 2)
light_tome = Weapon("Light", 4, 2)
wind_tome = Weapon("Wind", 4, 2)

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