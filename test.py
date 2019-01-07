#A file for testing code.
import sys, pygame
screen = pygame.display.set_mode((3000, 3000))

marth_img = pygame.image.load("FEH_Marth.png").convert_alpha() #load image as surface
while True:
    screen.fill((0,0,0))
    screen.blit(marth_img, (0,0))