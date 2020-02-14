import math
import random
import pygame
pygame.mixer.init()
pygame.init()
Display = pygame.display.set_mode((1600, 480))
Display.fill((255, 255, 255))
from AncientRoar import *

def GraphicsRefresh(ExpressionState):
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()