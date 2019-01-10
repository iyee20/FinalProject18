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

class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color, weapon, color, image, equipped=None):
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
        self.image = image
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
        self.x = 0 #x square on screen
        self.y = 0 #y square on screen

class Foe:
    """The class for the enemies."""
    def __init__(self, name, weapon, color, image, hp, a, d, res, spd, rng, drop):
        self.chartype = "foe"
        self.name = name
        self.weapon = weapon
        self.color = color
        self.image = image
        self.hp = hp
        self.a = a
        self.d = d
        self.res = res
        self.spd = spd
        self.rng = rng
        self.drop = drop #how many breadcrumbs are dropped by the enemy
        self.x = 0
        self.y = 0
bg = screen.convert()
roll_imp_img = pygame.Rect((0,0,50,50)) #replace later
bun_dragon_img = pygame.Rect((0,0,50,50))
baguette_devil_img = pygame.Rect((0,0,50,50))
loaf_archer_img = pygame.Rect((0,0,50,50))
roll_imp = Foe("Roll Imp", "lance", "blue", roll_imp_img, 18, 11, 6, 3, 5, 1, 10) #based on Blue Fighter, 1 star with Iron Lance
bun_dragon = Foe("Bun Dragon", "dragonstone", "green", bun_dragon_img, 16, 13, 5, 4, 7, 1, 25) #based on Green Manakete, 2 star with Fire Breath
baguette_devil = Foe("Baguette Devil", "sword", "red", baguette_devil_img, 18, 11, 6, 3, 5, 1, 10) #based on Sword Fighter, 1 star with Iron Sword
loaf_archer = Foe("Loaf Archer", "bow", "colorless", loaf_archer_img, 17, 10, 5, 1, 5, 2, 10) #based on Bow Fighter, 1 star with Iron Bow

def get_bread(defeated, mc):
    """Obtain breadcrumbs from defeating an enemy."""
    input(f"You received {defeated.drop} breadcrumbs.")
    mc.breadcrumbs += defeated.drop
    return

def breadify(mc):
    """Convert breadcrumbs to bread."""
    converted = mc.breadcrumbs % 15 #how many whole breads can be made
    mc.breadcrumbs -= 15 * converted
    input(f"You received {converted} bread.")
    input(f"You now have {mc.breadcrumbs} breadcrumbs.")
    mc.bread += converted
    return

def check_bread(mc):
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
masked_marth = Bread("Masked Marth", "nonbinary", 75)
lucina = Bread("Masked Marth", "female", 50)

def unlock(character, mc):
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

def in_range(attacker, defender):
    x_dif = abs(attacker.x - defender.x)
    y_dif = abs(attacker.y - defender.y)
    if x_dif + y_dif <= attacker.range:
        return True
    else:
        return False

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

    def equip(self, mc):
        """Equip a weapon."""
        print(f"Equipped the {self.name}.")
        mc.a += self.might
        mc.rng = self.rng
        mc.equipped = self.name

    def unequip(self, mc):
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

def print_question(question, q_box, bg):
    """Print a question on q_box."""
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render(question, 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center
    bg.blit(q_text, q_text_position) #blit question text
    q_font_sub = pygame.font.Font(None, 20)
    q_text = q_font_sub.render("Type the number on the button.", 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.centerx, q_box.bottom - 20
    bg.blit(q_text, q_text_position) #blit subtext
    return

def print_button_text(text, button, bg):
    """Print text on a button."""
    font = pygame.font.Font(None, 20)
    text = font.render(text, 1, black)
    text_position = text.get_rect()
    text_position.center = button.center
    bg.blit(text, text_position)
    return

def spawn(character):
    """Spawn a character on the screen."""
    global screen, bg
    #location is based on a 6 x 6 tile map
    squarex = random.randint(1, 6)
    squarey = random.randint(1, 6)
    #location = screen.get_width() * squarex / 6, screen.get_height() * squarey / 6
    character.image.left = (screen.get_width() * squarex / 6) + 100/6 #temp, while images are Rects
    character.image.top = (screen.get_height() * squarey / 6) + 100/6
    character.x = squarex
    character.y = squarey
    if character.name == "You":
        bg.fill(light_blue, character.image) #temp, while images are Rects
    else:
        bg.fill(fe_blue, character.image)
    #bg.blit(character.image, location)
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def tilex(character):
    """Check which tile in the x direction a character is on."""
    global screen
    for x in range(1, 6):
        if x == character.x:
            return x
        else:
            None

def tiley(character):
    """Check which title in the y direction a character is on."""
    global screen
    for y in range(1, 6):
        if y == character.y:
            return y
        else:
            None

def move(character, tilexmove, tileymove):
    """Move a character on the screen."""
    global screen, bg
    position = character.get_rect()
    if tilex(character) + 2 > 6:
        tilexmove = 6 - tilex(character)
    if tiley(character) + 2 > 6:
        tileymove = 6 - tiley(character)
    position = position.move(tilexmove, tileymove)
    bg.blit(character, position)
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def draw_map():
    """Draw the battle map on the screen."""
    pass #remove later
    global screen, bg
    bg.fill((250, 250, 250))
    for x in range(1,6):
        linespace = screen.get_width() * x / 6
        pygame.draw.line(bg, (0,0,0), (linespace, 0), (linespace, screen.get_height()))
    for y in range(1,6):
        linespace = screen.get_height() * y / 6
        pygame.draw.line(bg, (0,0,0), (0, linespace), (screen.get_width(), linespace))
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def main():
    """The code of the game."""
    #opening screen
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

    intro = True
    while intro == True: #event loop - start
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the Player tries to close the window...
                return
            elif event.type == pygame.KEYDOWN: #if the Player presses a key...
                intro = False

    #start Player customization
    bg.fill(white)
    pygame.display.flip()
    
    q_box_size = pygame.Rect(0, 0, 500, 100)
    q_box = bg.fill(fe_blue, q_box_size) #question box is a filled rectangle
    q_box.topleft = 0, 0

    #question text
    name = "You" #Player is always referred to as "You"
    #Player appearance (gender)
    print_question("Do you identify as male, female, or nonbinary?", q_box, bg)
    screen.blit(bg, (0,0))
    pygame.display.flip()

    #define the size of buttons
    a_box_size = pygame.Rect(0, 0, 500, 50) #a_box is a Rect, 500 x 50 px
    a_box_width = a_box_size.width
    a_box_height = a_box_size.height #the height of a_box is used as the button height
    button_width = (a_box_width / 3) - 10
    button_top = bg.get_height() - a_box_height
    c_button_left = (a_box_width / 2) - (button_width / 2)
    r_button_left = a_box_width - button_width
    l_button_size = pygame.Rect(0, button_top, button_width, a_box_height)
    c_button_size = pygame.Rect(c_button_left, button_top, button_width, a_box_height)
    r_button_size = pygame.Rect(r_button_left, button_top, button_width, a_box_height)

    l_button = bg.fill(light_blue, l_button_size) #left button
    print_button_text("1. Male", l_button, bg)

    c_button = bg.fill(light_blue, c_button_size) #center button
    print_button_text("2. Female", c_button, bg)

    r_button = bg.fill(light_blue, r_button_size) #right button
    print_button_text("3. Nonbinary", r_button, bg)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    choosing = True
    while choosing == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    appearance = "male"
                    choosing = False
                elif pressed[pygame.K_2] == True:
                    appearance = "female"
                    choosing = False
                elif pressed[pygame.K_3] == True:
                    appearance = "nonbinary"
                    choosing = False

    #Player eye color
    q_box = bg.fill(fe_blue, q_box_size) #clear q_box and re-fill
    print_question("What color are your eyes?", q_box, bg)

    l_button = bg.fill(light_blue, l_button_size) #clear buttons and re-fill
    c_button = bg.fill(light_blue, c_button_size)
    r_button = bg.fill(light_blue, r_button_size)

    print_button_text("1. Red", l_button, bg) #new button text
    print_button_text("2. Green", c_button, bg)
    print_button_text("3. Blue", r_button, bg)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    choosing = True
    while choosing == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return            
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    eye_color = "red"
                    choosing = False
                elif pressed[pygame.K_2] == True:
                    eye_color = "green"
                    choosing = False
                elif pressed[pygame.K_3] == True:
                    eye_color = "blue"
                    choosing = False
    
    #Player hair color
    q_box = bg.fill(fe_blue, q_box_size) #clear q_box and re-fill
    print_question("What color is your hair?", q_box, bg)

    l_button = bg.fill(light_blue, l_button_size) #clear buttons and re-fill
    c_button = bg.fill(light_blue, c_button_size)
    r_button = bg.fill(light_blue, r_button_size)

    print_button_text("1. Red", l_button, bg)
    print_button_text("2. Green", c_button, bg)
    print_button_text("3. Blue", r_button, bg)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    choosing = True
    while choosing == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    hair_color = "red"
                    choosing = False
                elif pressed[pygame.K_2] == True:
                    hair_color = "green"
                    choosing = False
                elif pressed[pygame.K_3] == True:
                    hair_color = "blue"
                    choosing = False
    
    #mc_appearance_eye color_hair color
    mc_m_r_r = pygame.Rect((0,0,50,50)) #replace later
    mc_m_r_g = pygame.Rect((0,0,50,50))
    mc_m_r_b = pygame.Rect((0,0,50,50))
    mc_m_b_r = pygame.Rect((0,0,50,50))
    mc_m_b_b = pygame.Rect((0,0,50,50))
    mc_m_b_g = pygame.Rect((0,0,50,50))
    mc_m_g_r = pygame.Rect((0,0,50,50))
    mc_m_g_b = pygame.Rect((0,0,50,50))
    mc_m_g_g = pygame.Rect((0,0,50,50))
    mc_f_r_r = pygame.Rect((0,0,50,50))
    mc_f_r_g = pygame.Rect((0,0,50,50))
    mc_f_r_b = pygame.Rect((0,0,50,50))
    mc_f_b_r = pygame.Rect((0,0,50,50))
    mc_f_b_b = pygame.Rect((0,0,50,50))
    mc_f_b_g = pygame.Rect((0,0,50,50))
    mc_f_g_r = pygame.Rect((0,0,50,50))
    mc_f_g_b = pygame.Rect((0,0,50,50))
    mc_f_g_g = pygame.Rect((0,0,50,50))
    mc_n_r_r = pygame.Rect((0,0,50,50))
    mc_n_r_g = pygame.Rect((0,0,50,50))
    mc_n_r_b = pygame.Rect((0,0,50,50))
    mc_n_b_r = pygame.Rect((0,0,50,50))
    mc_n_b_b = pygame.Rect((0,0,50,50))
    mc_n_b_g = pygame.Rect((0,0,50,50))
    mc_n_g_r = pygame.Rect((0,0,50,50))
    mc_n_g_b = pygame.Rect((0,0,50,50))
    mc_n_g_g = pygame.Rect((0,0,50,50))
    #image logic - which icon is used
    if appearance == "male":
        if eye_color == "red":
            if hair_color == "red":
                image = mc_m_r_r
            elif hair_color == "blue":
                image = mc_m_r_b
            elif hair_color == "green":
                image = mc_m_r_g
        elif eye_color == "blue":
            if hair_color == "red":
                image = mc_m_b_r
            elif hair_color == "blue":
                image = mc_m_b_b
            elif hair_color == "green":
                image = mc_m_b_g
        elif eye_color == "green":
            if hair_color == "red":
                image = mc_m_g_r
            elif hair_color == "blue":
                image = mc_m_g_b
            elif hair_color == "green":
                image = mc_m_g_g
    elif appearance == "female":
        if eye_color == "red":
            if hair_color == "red":
                image = mc_f_r_r
            elif hair_color == "blue":
                image = mc_f_r_b
            elif hair_color == "green":
                image = mc_f_r_g
        elif eye_color == "blue":
            if hair_color == "red":
                image = mc_f_b_r
            elif hair_color == "blue":
                image = mc_f_b_b
            elif hair_color == "green":
                image = mc_f_b_g
        elif eye_color == "green":
            if hair_color == "red":
                image = mc_f_g_r
            elif hair_color == "blue":
                image = mc_f_g_b
            elif hair_color == "green":
                image = mc_f_g_g
    elif appearance == "nonbinary":
        if eye_color == "red":
            if hair_color == "red":
                image = mc_n_r_r
            elif hair_color == "blue":
                image = mc_n_r_b
            elif hair_color == "green":
                image = mc_n_r_g
        elif eye_color == "blue":
            if hair_color == "red":
                image = mc_n_b_r
            elif hair_color == "blue":
                image = mc_n_b_b
            elif hair_color == "green":
                image = mc_n_b_g
        elif eye_color == "green":
            if hair_color == "red":
                image = mc_n_g_r
            elif hair_color == "blue":
                image = mc_n_g_b
            elif hair_color == "green":
                image = mc_n_g_g

    #Player weapon
    bg.fill(white) #refill background to start a new question
    pygame.display.flip()

    q_box = bg.fill(fe_blue, q_box_size)
    print_question("Pick a weapon.", q_box, bg)

    button_top_1 = q_box.height + 10
    button_top_2 = bg.get_rect().centery + (a_box_height / 2)
    b1_size = pygame.Rect(0, button_top_1, button_width, a_box_height)
    b2_size = pygame.Rect(r_button_left, button_top_1, button_width, a_box_height)
    b3_size = pygame.Rect(0, button_top_2, button_width, a_box_height)
    b4_size = pygame.Rect(r_button_left, button_top_2, button_width, a_box_height)
    b5_size = pygame.Rect(0, button_top, button_width, a_box_height)
    b6_size = pygame.Rect(c_button_left, button_top, button_width, a_box_height)
    b7_size = pygame.Rect(r_button_left, button_top, button_width, a_box_height)
    
    b1 = bg.fill(light_blue, b1_size)
    b2 = bg.fill(light_blue, b2_size)
    b3 = bg.fill(light_blue, b3_size)
    b4 = bg.fill(light_blue, b4_size)
    b5 = bg.fill(light_blue, b5_size)
    b6 = bg.fill(light_blue, b6_size)
    b7 = bg.fill(light_blue, b7_size)

    print_button_text("1. Sword", b1, bg)
    print_button_text("2. Lance", b2, bg)
    print_button_text("3. Axe", b3, bg)
    print_button_text("4. Bow", b4, bg)
    print_button_text("5. Dagger", b5, bg)
    print_button_text("6. Dragonstone", b6, bg)
    print_button_text("7. Tome", b7, bg)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    choosing = True
    while choosing == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    weapon = "sword"
                    choosing = False
                elif pressed[pygame.K_2] == True:
                    weapon = "lance"
                    choosing = False
                elif pressed[pygame.K_3] == True:
                    weapon = "axe"
                    choosing = False
                elif pressed[pygame.K_4] == True:
                    weapon = "bow"
                    choosing = False
                elif pressed[pygame.K_5] == True:
                    weapon = "dagger"
                    choosing = False
                elif pressed[pygame.K_6] == True:
                    weapon = "dragonstone"
                    choosing = False
                elif pressed[pygame.K_7] == True:
                    weapon = "tome"
                    choosing = False

    colors = ["red", "blue", "green"] #I've elected to remove the colorless option for daggers, bows, and dragonstones
    if weapon == "sword":
        color = "red"
    elif weapon == "lance":
        color = "blue"
    elif weapon == "axe":
        color = "green"
    elif weapon == "dagger" or weapon == "bow" or weapon == "dragonstone" or weapon == "tome":
        color = random.choice(colors) #random color assignment, to be fair

    mc = Player(name, appearance, eye_color, hair_color, weapon, color, image, None)

    bg.fill(white)
    q_box = bg.fill(white, q_box_size) #q_box is white for the equipment screen

    if weapon == "sword":
        print_button_text("You received an Iron Sword!", q_box, bg) #print text on q_box (q_box is the "button")
        iron_sword.equip(mc)
    elif weapon == "lance":
        print_button_text("You received an Iron Lance!", q_box, bg)
        iron_lance.equip(mc)
    elif weapon == "axe":
        print_button_text("You received an Iron Axe!", q_box, bg)
        iron_axe.equip(mc)
    elif weapon == "dagger":
        print_button_text(f"You received a {color} Iron Dagger!", q_box, bg)
        iron_dagger.equip(mc)
    elif weapon == "bow":
        print_button_text(f"You received a {color} Iron Bow!", q_box, bg)
        iron_bow.equip(mc)
    elif weapon == "dragonstone":
        print_button_text(f"You received a {color} Fire Breath dragonstone!", q_box, bg)
        fire_breath.equip(mc)
    elif weapon == "tome":
        if color == "red":
            print_button_text("You received a Fire tome!", q_box, bg)
            fire_tome.equip(mc)
        elif color == "blue":
            print_button_text("You received a Light tome!", q_box, bg)
            light_tome.equip(mc)
        elif color == "green":
            print_button_text("You received a Wind tome!", q_box, bg)
            wind_tome.equip(mc)
    
    bottom_text = font.render("Press any key to continue.", 1, black) #font = size of instructions on opening screen, 25px
    bg.blit(bottom_text, text_position)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    wait_to_start = True
    while wait_to_start == True: #wait for Player to press a key
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                wait_to_start = False    

    draw_map()
    spawn(mc)
    spawn(roll_imp) #fix so it uncovers mc
    while True:
        if tilex(roll_imp) == tilex(mc) and tiley(roll_imp) == tiley(mc):
            move(roll_imp, 1, 1)
        else:
            break

    #temp, while testing
    wait_to_start = True
    while wait_to_start == True: #wait for Player to press a key
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                wait_to_start = False    
    return

main()

#see textmc.py for the terminal-based customization code