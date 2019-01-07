#the game is heavily based on Fire Emblem Heroes, the mobile game of the Fire Emblem series

import random #import random to use
import sys, pygame #import pygame to use
pygame.font.init() #initialize font module so font functions work

size = width, height = 500, 500 #define size as a certain px area
screen = pygame.display.set_mode(size) #create a Surface called "screen" with pygame (the screen the computer displays)

#define colors by name for convenience
black = (0, 0, 0) #rgb value of black
white = (250, 250, 250) #rgb value of white
fe_blue = (72, 117, 139) #color of Fire Emblem textboxes, midway between the gradient endpoints...ish
light_blue = (112, 172, 201) #a blue to stand out against Fire Emblem blue

#default stats
name = "Takumi"
appearance = "male"
eye_color = "red"
hair_color = "gray"
weapon = "bow"
color = "colorless"

class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color, weapon, color, equipped=None):
        self.chartype = "player"
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
        self.chartype = "foe"
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

def opening_screen():
    """Opening screen"""
    bg = screen.convert()
    
    bg.fill(white) #the opening bg is white, for now
    pygame.display.flip()
    
    #title words
    title_font = pygame.font.Font(None, 35) #title font is the default font at 35px size
    title_text = title_font.render("Fire Emblem: Let's Get This Bread", 1, black) #title text is antialiasing and black
    title_text_position = title_text.get_rect() #position of title text
    title_text_position.centerx = screen.get_rect().centerx #center of title text is at center of the screen's width
    title_text_position.bottom = screen.get_rect().bottom * 3 / 8 #title text is at 3/8 of screen's height
    bg.blit(title_text, title_text_position) #draw title text at title_text_position

    #opening instructions
    font = pygame.font.Font(None, 25) #instructions are default font at 25px size
    text = font.render("Press any key to start.", 1, black)
    text_position = text.get_rect() #position of instructions
    text_position.center = screen.get_rect().center #text is at center of screen
    bg.blit(text, text_position) #draw instructions at text_position

    screen.blit(bg, (0, 0)) #draw bg with text on screen
    pygame.display.flip()

    while True: #event loop - start
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the Player tries to close the window...
                sys.exit()
            elif event.type == pygame.KEYDOWN: #if the Player presses a key...
                return

def button_text(button, text):
    """Display a label on a button."""
    font = pygame.font.Font(None, 20)
    text = font.render(text, 1, black)
    return text

def button_text_position(button, button_text):
    """Display a label on a button."""
    text_position = button_text.get_rect()
    text_position.center = button.center
    return text_position

def add_button_text(screen, button_text, button_text_position):
    """Print text on a button."""
    screen.blit(button_text, button_text_position)
    return

def user_name():
    """Take user input to write the Player's name."""
    name = ""
    while True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    name += " "
                elif event.key == pygame.K_BACKSPACE:
                    name -= name[-1]
                elif pygame.key.name(event.key).isalpha() == True:
                    name += pygame.key.name(event.key)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return name.title()
                else:
                    None

def is_clicked(button):
    """Check if a button has been clicked."""
    pass
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button.left <= mouse[0] <= button.right and button.bottom <= mouse[1] <= button.top:
        if click[0] == 1:
            return True
        else:
            return False
    else:
        return False

def spawn(character):
    """Spawn a character on the screen."""
    global screen
    pass #remove
    #location is based on a 6 x 6 tile map
    squarex = random.randint(1, 6)
    squarey = random.randint(1, 6)
    location = screen.get_width() * squarex / 6, screen.get_height() * squarey / 6
    screen.blit(character, location)
    pygame.display.flip()
    return

def tilex(character):
    """Check which tile in the x direction a character is on."""
    global screen
    pass #remove
    character = character.get_rect()
    for x in range(1, 6):
        if character.right == screen.get_width() * x / 6:
            return x
        else:
            None

def tiley(character):
    """Check which title in the y direction a character is on."""
    global screen
    pass #remove
    character = character.get_rect()
    for y in range(1, 6):
        if character.bottom == screen.get_height() * y / 6:
            return y
        else:
            None

def move(character, tilexmove, tileymove):
    """Move a character on the screen."""
    global screen
    pass #remove
    position = character.get_rect()
    if tilex(character) + 2 > 6:
        tilexmove = 6 - tilex(character)
    if tiley(character) + 2 > 6:
        tileymove = 6 - tiley(character)
    position = position.move(tilexmove, tileymove)
    screen.blit(character, position)
    pygame.display.flip()
    return

#opening_screen()

###combine opening_screen() and main() later
def main():
    """The body of the game."""
    #start Player customization
    bg = screen.convert()
    bg.fill(white)
    pygame.display.flip()

    q_box_size = pygame.Rect(0, 0, 500, 100)
    q_box = bg.fill(fe_blue, q_box_size) #question box is a filled rectangle
    q_box.topleft = 0, 0

    a_box_size = pygame.Rect(0, 450, 500, 50)
    a_box = bg.fill(fe_blue, a_box_size) #answer box is a filled rectangle

    #question text
    #Player name
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render("What is your name?", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position)
    screen.blit(bg, (0,0))
    pygame.display.flip()

    #answer text: take user input and display it
    name = user_name()
    a_font = pygame.font.Font(None, 20)
    a_text = a_font.render(name, 1, black)
    a_text_position = a_text.get_rect()
    a_text_position.centerx = screen.get_rect().centerx
    a_text_position.bottom = screen.get_rect().bottom

    #check if the Player has entered a name
    while True:
        if name == "":
            q_box = bg.fill(fe_blue, q_box_size)
            q_font = pygame.font.Font(None, 25)
            q_text = q_font.render("You must enter a name. What is your name?", 1, black)
            q_text_position = q_text.get_rect()
            q_text_position.center = q_box.center
            bg.blit(q_text, q_text_position)
            screen.blit(bg, (0,0))
            pygame.display.flip()
            name = user_name()
        else:
            screen.blit(a_text, a_text_position)
            break

    screen.blit(bg, (0,0))
    pygame.display.flip()

    #Player appearance (gender)
    q_box = bg.fill(fe_blue, q_box_size)
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render("Do you identify as male, female, or nonbinary?", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position)
    screen.blit(bg, (0,0))
    pygame.display.flip()

    #define the size of buttons
    a_box_width = a_box.width
    a_box_height = a_box.height #the height of a_box is used as the button height
    button_width = (a_box_width / 3) - 10
    button_size = pygame.Rect(0, 0, button_width, a_box_height)

    l_button = screen.fill(light_blue, button_size) #left button
    l_button.bottomleft = 0, a_box_height
    l_button_text = button_text(l_button, "Male")
    l_button_text_position = button_text_position(l_button, l_button_text)
    add_button_text(screen, l_button_text, l_button_text_position)

    c_button = screen.fill(light_blue, button_size) #center button
    c_button.midbottom = a_box_width / 2, a_box_height
    c_button_text = button_text(c_button, "Female")
    c_button_text_position = button_text_position(c_button, c_button_text)
    add_button_text(screen, c_button_text, c_button_text_position)

    r_button = screen.fill(light_blue, button_size) #right button
    r_button.bottomright = a_box_width, a_box_height
    r_button_text = button_text(r_button, "Nonbinary")
    r_button_text_position = button_text_position(r_button, r_button_text)
    add_button_text(screen, r_button_text, r_button_text_position)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    #find a way to loop this
    if is_clicked(l_button) == True:
        appearance = "male"
    elif is_clicked(c_button) == True:
        appearance = "female"
    elif is_clicked(r_button) == True:
        appearance = "nonbinary"

    #Player eye color
    q_box = bg.fill(fe_blue, q_box_size) #clear q_box and re-fill
    q_font = pygame.font.Font(None, 25) #new q_box text
    q_text = q_font.render("What color are your eyes?", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position)

    l_button = screen.fill(light_blue, button_size) #clear buttons and re-fill
    c_button = screen.fill(light_blue, button_size)
    r_button = screen.fill(light_blue, button_size)

    l_button_text = button_text(l_button, "Red") #new button text
    l_button_text_position = button_text_position(l_button, l_button_text)
    add_button_text(screen, l_button_text, l_button_text_position)
    c_button_text = button_text(c_button, "Blue")
    c_button_text_position = button_text_position(c_button, c_button_text)
    add_button_text(screen, c_button_text, c_button_text_position)
    r_button_text = button_text(r_button, "Green")
    r_button_text_position = button_text_position(r_button, r_button_text)
    add_button_text(screen, r_button_text, r_button_text_position)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    #find a way to loop this
    if is_clicked(l_button) == True:
        eye_color = "red"
    elif is_clicked(c_button) == True:
        eye_color = "green"
    elif is_clicked(r_button) == True:
        eye_color = "blue"
    
    #Player hair color
    q_box = bg.fill(fe_blue, q_box_size) #clear q_box and re-fill
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render("What color is your hair?", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position)

    l_button = screen.fill(light_blue, button_size) #clear buttons and re-fill
    c_button = screen.fill(light_blue, button_size)
    r_button = screen.fill(light_blue, button_size)

    l_button_text = button_text(l_button, "Red") #new button text
    l_button_text_position = button_text_position(l_button, l_button_text)
    add_button_text(screen, l_button_text, l_button_text_position)
    c_button_text = button_text(c_button, "Blue")
    c_button_text_position = button_text_position(c_button, c_button_text)
    add_button_text(screen, c_button_text, c_button_text_position)
    r_button_text = button_text(r_button, "Green")
    r_button_text_position = button_text_position(r_button, r_button_text)
    add_button_text(screen, r_button_text, r_button_text_position)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    #find a way to loop this
    if is_clicked(l_button) == True:
        hair_color = "red"
    elif is_clicked(c_button) == True:
        hair_color = "green"
    elif is_clicked(r_button) == True:
        hair_color = "blue"
    
    #Player weapon
    bg.fill(white) #refill background to start a new question
    pygame.display.flip()

    q_box_size = pygame.Rect(0, 0, 500, 100)
    q_box = bg.fill(fe_blue, q_box_size) #question box is a filled rectangle
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render("Pick a weapon.", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position)

    return

main()

#test image stuff that can be worked out later
#marth_img = pygame.image.load("FEH_Marth.png").convert() #load image as surface
#while True:
    #screen.fill(black)
    #screen.blit(marth_img, (0,0))

mc = Player(name, appearance, eye_color, hair_color, weapon, color, equipped=None)
#see textmc.py for the terminal-based customization code