import math
import random
import pygame
pygame.mixer.init()
pygame.init()
Display = pygame.display.set_mode((1600, 480), pygame.NOFRAME)
from AncientRoar import *

def GraphicsRefresh(ExpressionState, GazeX, GazeY):
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()