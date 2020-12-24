import os
import math
import time
import pygame
pygame.mixer.init()
pygame.init()
Display = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
frametime = 0
currentframe = 0

class EyesSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(EyesSprite, self).__init__()
        self.neutralimages = []
        self.aggressiveimages = []
        self.sleepingimages = []
        self.cheerfulimages = []
        self.embarrassedimages = []
        self.questionmarkimages = []
        self.cryingimages = []
        self.shockedimages = []
        self.sillyimages = []
        self.heartimages = []
        self.hypnoticimages = []
        files = os.listdir('EYES')
        files.sort()
        for filename in files:
            tag = filename.split("_")[0]
            if tag == 'neutral':
                self.neutralimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'aggressive':
                self.aggressiveimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'sleeping':
                self.sleepingimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'cheerful':
                self.cheerfulimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'embarrassed':
                self.embarrassedimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'questionmark':
                self.questionmarkimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'crying':
                self.cryingimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'shocked':
                self.shockedimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'silly':
                self.sillyimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'heart':
                self.heartimages.append(pygame.image.load(os.path.join('EYES', filename)))
            elif tag == 'hypnotic':
                self.hypnoticimages.append(pygame.image.load(os.path.join('EYES', filename)))
        self.index = 0
        self.image = self.images[0][self.index]
        self.rect = pygame.Rect(0, 0, 1600, 480)
    def update(self, ExpressionState):
        global frametime
        global currentframe
        if(time.clock() - frametime > 0.017): #60 FPS
            def imageAssign(i):
                switcher = {
                    0: self.neutralimages,
                    1: self.aggressiveimages,
                    2: self.sleepingimages,
                    3: self.cheerfulimages,
                    4: self.embarrassedimages,
                    5: self.questionmarkimages,
                    6: self.cryingimages,
                    7: self.shockedimages,
                    8: self.sillyimages,
                    9: self.heartimages,
                    10: self.hypnoticimages
                }
                return switcher.get(i, "Invalid Expression")
            arr = imageAssign(ExpressionState)
            self.index += 1
            if self.index >= len(arr):
                self.index = 0
            self.image = arr[self.index]
            frametime = time.clock()
            currentframe = self.index
            Display.blit(self.image, self.image.get_rect())

my_sprite = EyesSprite()
my_group = pygame.sprite.Group(my_sprite)

def GraphicsRefresh(ExpressionState):
    my_group.update(ExpressionState)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()