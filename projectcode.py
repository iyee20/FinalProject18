#the game is heavily based on Fire Emblem Heroes, the mobile game of the Fire Emblem series

import random #import random to use
import sys, pygame #import pygame to use
pygame.font.init() #initialize font module so font functions work

size = width, height = 500, 500 #define size as a certain px area
screen = pygame.display.set_mode(size) #create a Surface called "screen" with pygame (the screen the computer displays)
bg = screen.convert() #bg is a separate Surface based on screen

#define colors by name for convenience
black = (0, 0, 0) #rgb value of black
white = (250, 250, 250) #rgb value of white
fe_blue = (72, 117, 139) #color of Fire Emblem textboxes, midway between the gradient endpoints...ish
light_blue = (112, 172, 201) #a blue to stand out against Fire Emblem blue
red = (223, 29, 64) #a red to represent red-colored characters
blue = (36, 101, 224) #a blue to represent blue-colored characters
green = (6, 165, 41) #a green to represent green-colored characters
gray = (100, 117, 126) #a gray to represent colorless characters

#Anna's image
anna = pygame.image.load("Images/NPC/Anna.png").convert_alpha() #load file as surface

class Player:
    """The class for the Player."""
    def __init__(self, name, appearance, eye_color, hair_color, weapon, color, image, equipped=None):
        self.chartype = "player"
        self.name = name #name is always Player, but this attribute is for consistency
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
        self.equipped = equipped #which weapon is equipped
#base stats based on the first summoned hero in Fire Emblem Heroes, Takumi, at 4 star rarity, except for range
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
roll_imp_img = pygame.image.load("Images/NPC/roll_imp.png").convert_alpha()
bun_dragon_img = pygame.image.load("Images/NPC/bun_dragon.png").convert_alpha()
baguette_devil_img = pygame.image.load("Images/NPC/baguette_devil.png").convert_alpha()
loaf_archer_img = pygame.image.load("Images/NPC/loaf_archer.png").convert_alpha()
roll_imp = Foe("Roll Imp", "lance", "blue", roll_imp_img, 18, 11, 6, 3, 5, 1, 10) #based on Blue Fighter, 1 star with Iron Lance
bun_dragon = Foe("Bun Dragon", "dragonstone", "green", bun_dragon_img, 16, 13, 5, 4, 7, 1, 25) #based on Green Manakete, 2 star with Fire Breath
baguette_devil = Foe("Baguette Devil", "sword", "red", baguette_devil_img, 18, 11, 6, 3, 5, 1, 10) #based on Sword Fighter, 1 star with Iron Sword
loaf_archer = Foe("Loaf Archer", "bow", "colorless", loaf_archer_img, 17, 10, 5, 1, 5, 2, 10) #based on Bow Fighter, 1 star with Iron Bow

def get_bread(defeated, mc):
    """Obtain breadcrumbs from defeating an enemy."""
    mc.breadcrumbs += defeated.drop #add to Player's breadcrumb count
    return

def breadify(mc, menu_box_size):
    """Convert breadcrumbs to bread."""
    global screen, bg
    converted = mc.breadcrumbs % 15 #calculate how many whole breads can be made
    mc.breadcrumbs -= 15 * converted
    mc.bread += converted
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
marth = Bread("Marth", "male", 10) #Marth - the main character of many FE games
lucina = Bread("Masked Marth", "female", 50) #Lucina - Marth's descendant
masked_marth = Bread("Masked Marth", "nonbinary", 75) #Masked Marth - Lucina, but disguised as Marth to save your timeline... but that's another can of worms

def unlock(character, mc):
    """Unlock a character's cutscene."""
    if character.bread == 0:
        None #if character has already been unlocked, nothing happens
    elif mc.bread < character.bread:
        input(f"You don't have enough bread to unlock {character.name} yet.") #fix
    elif mc.bread >= character.bread:
        input(f"{character.name} unlocked!")
        mc.bread -= character.bread
        character.bread = 0 #character's bread cost is now 0
    return

def in_range(attacker, defender):
    x_dif = abs(attacker.x - defender.x)
    y_dif = abs(attacker.y - defender.y)
    if x_dif + y_dif <= attacker.rng: #this allows attackers with range 2 to attack within 2 spaces
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
def attack(attacker, defender, menu_box_size):
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
    defender.hp -= int(dmg)
    display_health(menu_box_size, [attacker, defender])
    return

def check_defeat(defeated):
    """Check if a character has been defeated."""
    if defeated.hp == 0:
        return True
    else:
        return False

def reset_hp(character):
    """Reset a character's hp after battle."""
    if character.chartype != "foe":
       character.hp = 17 #Player hp is reset
    else: #reset foe hp
        if character.name == "Roll Imp" or character.name == "Baguette Devil":
            character.hp = 18
        elif character.name == "Bun Dragon":
            character.hp = 16
        elif character.name == "Loaf Archer":
            character.hp = 17
    return 

class Weapon:
    """The class for weapons that can be equipped by the Player."""
    def __init__(self, name, might, rng):
        self.name = name
        self.might = might #the attack power of the weapon
        self.rng = rng

    def equip(self, mc):
        """Equip a weapon."""
        mc.a += self.might
        mc.rng = self.rng
        mc.equipped = self.name
iron_sword = Weapon("Iron Sword", 6, 1)
iron_lance = Weapon("Iron Lance", 6, 1)
iron_axe = Weapon("Iron Axe", 6, 1)
iron_bow = Weapon("Iron Bow", 4, 2)
iron_dagger = Weapon("Iron Dagger", 3, 2)
fire_breath = Weapon("Fire Breath", 6, 1)
fire_tome = Weapon("Fire", 4, 2) #red tome
light_tome = Weapon("Light", 4, 2) #blue tome
wind_tome = Weapon("Wind", 4, 2) #green tome

def print_question(question, q_box, bg):
    """Print a question on q_box."""
    q_font = pygame.font.Font(None, 25)
    q_text = q_font.render(question, 1, black)
    q_text_position = q_text.get_rect()
    q_text_position.center = q_box.center #question text is at center of q_box
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
    text_position.center = button.center #print button text at center of button
    bg.blit(text, text_position)
    return

def spawn(character, spawned):
    """Spawn a character on the screen."""
    global screen, bg
    #location is based on a 6 x 5 tile map
    squarex = random.randint(0, 5)
    squarey = random.randint(1, 5) #the top row is taken up by the menu box, so spawn starting at the second row down
    if spawned != None:
        for other in spawned:
            if squarex == other.x and squarey == other.y: #re-spawn a character if they would spawn on top of another character
                squarex = random.randint(0, 5)
                squarey = random.randint(1, 5)
    location = (screen.get_width() * squarex / 6) + 100/6, (screen.get_height() * squarey / 6) + 100/6
    character.x = squarex
    character.y = squarey #record x, y location
    bg.blit(character.image, location)
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def move(character, tilexmove, tileymove, others):
    """Move a character on the screen."""
    global screen, bg
    position = pygame.Rect((screen.get_width() * character.x / 6) + 100/6, (screen.get_height() * character.y / 6) + 100/6, screen.get_width()/6, screen.get_height()/6)
    if character.x + tilexmove > 5 or character.x + tilexmove < 0: #character can't move beyond the screen
        tilexmove = 0
    if character.y + tileymove > 5 or character.y + tileymove < 1:
        tileymove = 0
    for char in others:
        if character.x + tilexmove == char.x and character.y + tileymove == char.y:
            tilexmove = 0
            tileymove = 0 #nullify movement if it would move on top of another character
    character.x += tilexmove
    character.y += tileymove
    tilexmove *= screen.get_width()/6
    tileymove *= screen.get_height()/6
    new_pos = position.move(tilexmove, tileymove)
    clean_map(others)
    bg.blit(character.image, new_pos)
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def draw_map():
    """Draw the battle map on the screen."""
    global screen, bg
    fill_space = pygame.Rect(0, bg.get_height()/6, bg.get_width(), bg.get_height()*5/6) #only fill the 5 x 6 grid below the menu
    bg.fill((250, 250, 250), fill_space)
    for x in range(1,6): #draw grid lines
        linespace = screen.get_width() * x / 6
        pygame.draw.line(bg, (0,0,0), (linespace, bg.get_height()/6), (linespace, bg.get_height()))
    for y in range(1,6):
        linespace = screen.get_height() * y / 6
        pygame.draw.line(bg, (0,0,0), (0, linespace), (bg.get_width(), linespace))
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def anna_box(menu_box_size, dialogue, line2):
    """Draw Anna's dialogue box on the screen."""
    global screen, bg, anna
    bg.fill(fe_blue, menu_box_size)
    white_box = pygame.Rect(10, 0, screen.get_width() - 20, menu_box_size.height)
    bg.fill(white, white_box)
    bg.blit(anna, (10,0)) #print Anna's image

    font = pygame.font.Font(None, 20)
    text = font.render("ANNA", 1, black) #print Anna's name
    text_position = text.get_rect()
    text_position.left = 60
    bg.blit(text, text_position)
    
    dialogue_text = font.render(dialogue, 1, black) #print first line of dialogue
    dialogue_text_pos = dialogue_text.get_rect()
    dialogue_text_pos.left = 60
    dialogue_text_pos.top = text_position.height + 5
    bg.blit(dialogue_text, dialogue_text_pos)

    if line2 != None: #if there is a second line of dialogue, print it
        line2_text = font.render(line2, 1, black)
        line2_text_pos = line2_text.get_rect()
        line2_text_pos.left = 60
        line2_text_pos.top = dialogue_text_pos.top + 25
        bg.blit(line2_text, line2_text_pos)

    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def display_health(menu_box_size, characters):
    """Display the health of all characters on the screen."""
    global screen, bg
    bg.fill(fe_blue, menu_box_size)
    font = pygame.font.Font(None, 20)
    above = -20
    for character in characters:
        above += 30 #add 30px to the above line
        text = font.render(f"{character.name}: {character.hp} HP", 1, black)
        text_pos = text.get_rect()
        text_pos.left = 10
        text_pos.top = above
        bg.blit(text, text_pos)
    
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def draw_menu(menu_box_size):
    """Draw the menu box on the screen."""
    global screen, bg
    bg.fill(fe_blue, menu_box_size) #fill menu bg
    check_bread_box = pygame.Rect(10, 10, menu_box_size.width/3 - 10, menu_box_size.height - 20)
    unlock_bread_box = pygame.Rect(menu_box_size.width/3 + 6, 10, menu_box_size.width/3 - 10, menu_box_size.height - 20)
    new_lvl_box = pygame.Rect(menu_box_size.width*2/3, 10, menu_box_size.width/3 - 10, menu_box_size.height - 20)
    bg.fill(light_blue, check_bread_box)
    bg.fill(light_blue, unlock_bread_box)
    bg.fill(light_blue, new_lvl_box) #fill buttons

    font = pygame.font.Font(None, 20)
    t1 = font.render("1. Check Bread", 1, black) #check bread button
    t1_pos = t1.get_rect()
    t1_pos.center = check_bread_box.center
    bg.blit(t1, t1_pos)

    t2 = font.render("2. Unlock Bread", 1, black) #unlock bread button
    t2_pos = t2.get_rect()
    t2_pos.center = unlock_bread_box.center
    bg.blit(t2, t2_pos)

    t3 = font.render("3. New Level", 1, black) #new level button
    t3_pos = t3.get_rect()
    t3_pos.center = new_lvl_box.center
    bg.blit(t3, t3_pos)

    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def bread_menu(menu_box_size, mc):
    """Draw the bread menu on the screen and interact with it."""
    global screen, bg
    bg.fill(fe_blue, menu_box_size) #fill menu bg
    breadcrumb_box = pygame.Rect(10, 10, menu_box_size.width/3 - 10, menu_box_size.height/2 - 11)
    bread_box = pygame.Rect(10, menu_box_size.height/2 + 2, menu_box_size.width/3 - 10, menu_box_size.height/2 - 11)
    convert_bread_box = pygame.Rect(menu_box_size.width/3 + 6, 10, menu_box_size.width/3 - 10, menu_box_size.height - 20)
    go_back_box = pygame.Rect(menu_box_size.width*2/3, 10, menu_box_size.width/3 - 10, menu_box_size.height - 20)
    bg.fill(light_blue, breadcrumb_box) #fill buttons
    bg.fill(light_blue, bread_box)
    bg.fill(light_blue, convert_bread_box)
    bg.fill(light_blue, go_back_box)

    font = pygame.font.Font(None, 20)
    t1 = font.render(f"Breadcrumbs: {mc.breadcrumbs}", 1, black) #display number of breadcrumbs
    t1_pos = t1.get_rect()
    t1_pos.center = breadcrumb_box.center
    bg.blit(t1, t1_pos)

    t2 = font.render(f"Bread: {mc.bread}", 1, black) #display amount of bread
    t2_pos = t2.get_rect()
    t2_pos.center = bread_box.center
    bg.blit(t2, t2_pos)

    t3 = font.render("1. Convert Bread", 1, black) #convert breadcrumbs to bread button
    t3_pos = t3.get_rect()
    t3_pos.center = convert_bread_box.center
    bg.blit(t3, t3_pos)

    t4 = font.render("2. Exit Bread Menu", 1, black) #exit bread menu button
    t4_pos = t4.get_rect()
    t4_pos.center = go_back_box.center
    bg.blit(t4, t4_pos)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    wait_to_start = True
    while wait_to_start == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    breadify(mc, menu_box_size) #convert bread if the button is "pressed"
                    wait_to_start = False
                elif pressed[pygame.K_2] == True:
                    wait_to_start = False

    return

def unlock_menu(menu_box_size):
    """Draw the bread unlocking box on the screen."""
    global screen, bg
    bg.fill(fe_blue, menu_box_size) #fill menu bg
    marth_box = pygame.Rect(10, 10, menu_box_size.width/4 - 10, menu_box_size.height - 20)
    lucina_box = pygame.Rect(menu_box_size.width/4, 10, menu_box_size.width/4 - 10, menu_box_size.height - 20)
    masked_marth_box = pygame.Rect(menu_box_size.width/2, 10, menu_box_size.width/4 - 10, menu_box_size.height - 20)
    go_back_box = pygame.Rect(menu_box_size.width*3/4, 10, menu_box_size.width/4 - 10, menu_box_size.height - 20)
    if marth.bread == 0:
        bg.fill(light_blue, marth_box) #fill button blue if unlocked
    else:
        bg.fill(gray, marth_box) #fill button gray if not unlocked
    if lucina.bread == 0:
        bg.fill(light_blue, lucina_box)
    else:
        bg.fill(gray, lucina_box)
    if masked_marth.bread == 0:
        bg.fill(light_blue, masked_marth_box)
    else:
        bg.fill(gray, masked_marth_box)
    bg.fill(light_blue, exit_box)

    font = pygame.font.Font(None, 20)
    t1 = font.render("1. Marth", 1, black) #Marth cutscene button
    t1_pos = t1.get_rect()
    t1_pos.center = marth_box.center
    bg.blit(t1, t1_pos)

    t2 = font.render("2. Lucina", 1, black) #Lucina cutscene button
    t2_pos = t2.get_rect()
    t2_pos.center = lucina_box.center
    bg.blit(t2, t2_pos)

    t3 = font.render("3. Masked Marth", 1, black) #Masked Marth cutscene button
    t3_pos = t3.get_rect()
    t3_pos.center = masked_marth_box.center
    bg.blit(t3, t3_pos)

    t4 = font.render("4. Exit Unlock Menu", 1, black) #exit unlock menu button
    t4_pos = t4.get_rect()
    t4_pos.center = go_back_box.center
    bg.blit(t4, t4_pos)

    screen.blit(bg, (0,0))
    pygame.display.flip()

    wait_to_start = True
    while wait_to_start == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_1] == True:
                    #marth cutscene
                    wait_to_start = False
                elif pressed[pygame.K_2] == True:
                    #lucina cutscene
                    wait_to_start = False
                elif pressed[pygame.K_3] == True:
                    #masked marth cutscene
                    wait_to_start = False
                elif pressed[pygame.K_4] == True:
                    wait_to_start = False

    return

def highlight(square, color):
    """Highlight a square with a colored outline."""
    global bg, screen
    pygame.draw.rect(bg, color, square, 5) #draw a colored rectangle with width 5
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def move_options(character, others):
    """Highlight the player's move options in green."""
    square_width = screen.get_width()/6
    square_height = screen.get_height()/6
    character_left = character.x * square_width
    character_top = character.y * square_height
    
    #characters can only move 1 space. otherwise, I would die from writing instructions.
    upsquare = pygame.Rect(character_left, character_top - square_height, square_width, square_height)
    leftsquare = pygame.Rect(character_left - square_width, character_top, square_width, square_height)
    rightsquare = pygame.Rect(character_left + square_width, character_top, square_width, square_height)
    downsquare = pygame.Rect(character_left, character_top + square_height, square_width, square_height)

    squares = [upsquare, leftsquare, rightsquare, downsquare]
    for option in squares: #for each square...
        squarex = option.left * square_width
        squarey = option.top * square_height
        for char in others: #check against all char in list others
            if squarex == char.x and squarey == char.y:
                None #if the square is occupied, don't highlight it
            else:
                if squarey != 0:
                    highlight(option, green) #highlight unoccupied squares green

    return

def move_player(mc, others):
    """Move the Player on the map."""
    global bg, screen
    choosing = True
    while choosing == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN: #if a key is pressed...
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP] == True:
                    move(mc, 0, -1, others)
                    choosing = False
                elif pressed[pygame.K_LEFT] == True:
                    move(mc, -1, 0, others)
                    choosing = False
                elif pressed[pygame.K_RIGHT] == True:
                    move(mc, 1, 0, others)
                    choosing = False
                elif pressed[pygame.K_DOWN] == True:
                    move(mc, 0, 1, others)
                    choosing = False
                elif pressed[pygame.K_KP_ENTER] == True or pressed[pygame.K_RETURN] == True:
                    choosing = False #don't move if the Player presses ENTER

    return

def move_npc(character, others):
    """Move an enemy on the map."""
    direction = random.randint(1,4) #randomly pick a direction
    if direction == 1:
        move(character, 0, -1, others) #1 = move up
    elif direction == 2:
        move(character, 1, 0, others) #2 = move right
    elif direction == 3:
        move(character, 0, 1, others) #3 = move down
    elif direction == 4:
        move(character, -1, 0, others) #4 = move left

    return

def clean_map(characters):
    """Draw the map with characters placed on it."""
    global bg, screen
    draw_map()
    for char in characters: #for every char in the list characters...
        location = pygame.Rect((screen.get_width() * char.x / 6) + 100/6, (screen.get_height() * char.y / 6) + 100/6, screen.get_width()/6, screen.get_height()/6)
        bg.blit(char.image, location)
    screen.blit(bg, (0,0))
    pygame.display.flip()
    return

def main():
    """The code of the game."""
    #opening screen
    global screen, bg
    
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
    
    #mc_appearance_eye color_hair color - load file as surface
    mc_m_r_r = pygame.image.load("Images/Player/mc_m_r_r.png").convert_alpha() #yes, I lost a few brain cells while copying and pasting these lines
    mc_m_r_g = pygame.image.load("Images/Player/mc_m_r_g.png").convert_alpha() #I lost a few more while coloring and saving all of the images, too
    mc_m_r_b = pygame.image.load("Images/Player/mc_m_r_b.png").convert_alpha()
    mc_m_b_r = pygame.image.load("Images/Player/mc_m_b_r.png").convert_alpha()
    mc_m_b_b = pygame.image.load("Images/Player/mc_m_b_b.png").convert_alpha()
    mc_m_b_g = pygame.image.load("Images/Player/mc_m_b_g.png").convert_alpha()
    mc_m_g_r = pygame.image.load("Images/Player/mc_m_g_r.png").convert_alpha()
    mc_m_g_b = pygame.image.load("Images/Player/mc_m_g_b.png").convert_alpha()
    mc_m_g_g = pygame.image.load("Images/Player/mc_m_g_g.png").convert_alpha()
    mc_f_r_r = pygame.image.load("Images/Player/mc_f_r_r.png").convert_alpha()
    mc_f_r_g = pygame.image.load("Images/Player/mc_f_r_g.png").convert_alpha()
    mc_f_r_b = pygame.image.load("Images/Player/mc_f_r_b.png").convert_alpha()
    mc_f_b_r = pygame.image.load("Images/Player/mc_f_b_r.png").convert_alpha()
    mc_f_b_b = pygame.image.load("Images/Player/mc_f_b_b.png").convert_alpha()
    mc_f_b_g = pygame.image.load("Images/Player/mc_f_b_g.png").convert_alpha()
    mc_f_g_r = pygame.image.load("Images/Player/mc_f_g_r.png").convert_alpha()
    mc_f_g_b = pygame.image.load("Images/Player/mc_f_g_b.png").convert_alpha()
    mc_f_g_g = pygame.image.load("Images/Player/mc_f_g_g.png").convert_alpha()
    mc_n_r_r = pygame.image.load("Images/Player/mc_n_r_r.png").convert_alpha()
    mc_n_r_g = pygame.image.load("Images/Player/mc_n_r_g.png").convert_alpha()
    mc_n_r_b = pygame.image.load("Images/Player/mc_n_r_b.png").convert_alpha()
    mc_n_b_r = pygame.image.load("Images/Player/mc_n_b_r.png").convert_alpha()
    mc_n_b_b = pygame.image.load("Images/Player/mc_n_b_b.png").convert_alpha()
    mc_n_b_g = pygame.image.load("Images/Player/mc_n_b_g.png").convert_alpha()
    mc_n_g_r = pygame.image.load("Images/Player/mc_n_g_r.png").convert_alpha()
    mc_n_g_b = pygame.image.load("Images/Player/mc_n_g_b.png").convert_alpha()
    mc_n_g_g = pygame.image.load("Images/Player/mc_n_g_g.png").convert_alpha()
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
        print_button_text("You received a red Iron Sword!", q_box, bg) #print text on q_box (q_box is the "button")
        iron_sword.equip(mc)
    elif weapon == "lance":
        print_button_text("You received a blue Iron Lance!", q_box, bg)
        iron_lance.equip(mc)
    elif weapon == "axe":
        print_button_text("You received a green Iron Axe!", q_box, bg)
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
            print_button_text("You received a red Fire tome!", q_box, bg)
            fire_tome.equip(mc)
        elif color == "blue":
            print_button_text("You received a blue Light tome!", q_box, bg)
            light_tome.equip(mc)
        elif color == "green":
            print_button_text("You received a green Wind tome!", q_box, bg)
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

    draw_map() #draw the bg
    spawn(mc, None) #spawn mc on map
    spawn(roll_imp, [mc]) #spawn Roll Imp on map, not on mc
    menu_box_size = pygame.Rect(0, 0, screen.get_width(), screen.get_height()/6)
    #menu_box = bg.fill(fe_blue, menu_box_size)
    #draw_menu(menu_box_size)
    anna_box(menu_box_size, "Good morning! It's good to see that you're finally awake.", None)
    pygame.time.delay(2000) #Player gets 2 seconds to read
    anna_box(menu_box_size, "The forces of Brioche have invaded Mantou. We need your help!", None)
    pygame.time.delay(4000)

    #tutorial dialogue
    square = pygame.Rect((screen.get_width() * roll_imp.x / 6), (screen.get_height() * roll_imp.y / 6), screen.get_width()/6, screen.get_height()/6)
    highlight(square, red)
    anna_box(menu_box_size, "That's a Roll Imp.", None)
    pygame.time.delay(2000)
    anna_box(menu_box_size, "The Roll Imp has a lance, which is a BLUE weapon.", None)
    pygame.time.delay(4000)
    anna_box(menu_box_size, "Keep the weapon-triangle advantages in mind when you", "attack enemies.")
    pygame.time.delay(5000)
    anna_box(menu_box_size, "BLUE weapons are effective against RED weapons, which are", "effective against GREEN weapons,") 
    pygame.time.delay(5000)
    anna_box(menu_box_size, "and GREEN weapons are effective against BLUE weapons.", None)
    pygame.time.delay(4000)
    anna_box(menu_box_size, "Let's try attacking the Roll Imp!", None)
    pygame.time.delay(2000)
    anna_box(menu_box_size, "Move using the arrow keys until you get in range to attack.", "Press ENTER if you don't need to move.")

    fight1 = True
    turn = "mc"
    while fight1 == True:
        if check_defeat(roll_imp) == True:
            draw_map()
            spawn(mc, None)
            get_bread(roll_imp, mc)
            reset_hp(roll_imp)
            reset_hp(mc)
            fight1 = False
        elif turn == "mc":
            move_options(mc, [roll_imp]) #show Player their move options
            move_player(mc, [roll_imp]) #the Player moves
            if in_range(mc, roll_imp) == True:
                attack(mc, roll_imp, menu_box_size) #the Player automatically attacks if the Roll Imp is in range
            turn = "foe"  
        else:
            move_npc(roll_imp, [mc]) #the Roll Imp moves
            pygame.time.delay(1000)
            if in_range(roll_imp, mc) == True:
                attack(roll_imp, mc, menu_box_size)
                if check_defeat(mc) == True: #this most likely won't happen, but the Player can be defeated by the first enemy
                    fight1 = False
            turn = "mc"

    anna_box(menu_box_size, "Nice work!", None)
    pygame.time.delay(2000)
    anna_box(menu_box_size, "Every time you defeat an enemy, you collect breadcrumbs.", None)
    pygame.time.delay(4000)
    anna_box(menu_box_size, "Press 1 to open the breadcrumb menu.", None)

    wait_to_start = True
    while wait_to_start == True:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN: #the Player doesn't actually have to press 1 this time, but... they don't have to know that
                wait_to_start = False    

    bread_menu(menu_box_size, mc)
    anna_box(menu_box_size, "Breadcrumbs can be converted in the Check Bread menu.", "It takes 15 breadcrumbs to make 1 bread.")
    pygame.time.delay(5000)
    anna_box(menu_box_size, "Bread is used to unlock bread characters. Press 2 to open", "the Unlock Bread menu.")

    pygame.time.delay(2000)

    return

main()

#see textmc.py for the terminal-based customization code