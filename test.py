#A file for testing code.
import sys, pygame
screen = pygame.display.set_mode((500, 500))

marth_img = pygame.image.load("FEH_Marth.png").convert_alpha() #load image as surface
x = 0
while True:
    x += 1
    screen.fill((0,0,0))
    screen.blit(marth_img, (0,0))
    pygame.display.flip()