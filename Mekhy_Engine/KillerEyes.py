import math
import pygame
pygame.init()
pygame.mixer.init()
Display = pygame.display.set_mode((1600, 480), pygame.NOFRAME)

def GraphicsRefresh(ExpressionState, GazeX, GazeY):
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()