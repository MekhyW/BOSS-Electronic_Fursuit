import os
import math
import time
import pygame
pygame.mixer.init()
pygame.init()
Display = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
frametime = 0
currentframe = 0
ExpressionState = 1

class EyesSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(EyesSprite, self).__init__()
        self.trueneutralimages = []
        self.happyneutralimages = []
        self.dubiousneutralimages = []
        self.boredneutralimages = []
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
        files = os.listdir('.')
        files.sort()
        for filename in files:
            tag = filename.split("_")[0]
            if tag == 'trueneutral':
                self.trueneutralimages.append(pygame.image.load(filename))
            elif tag == 'happyneutral':
                self.happyneutralimages.append(pygame.image.load(filename))
            elif tag == 'dubiousneutral':
                self.dubiousneutralimages.append(pygame.image.load(filename))
            elif tag == 'boredneutral':
                self.boredneutralimages.append(pygame.image.load(filename))
            elif tag == 'aggressive':
                self.aggressiveimages.append(pygame.image.load(filename))
            elif tag == 'sleeping':
                self.sleepingimages.append(pygame.image.load(filename))
            elif tag == 'cheerful':
                self.cheerfulimages.append(pygame.image.load(filename))
            elif tag == 'embarrassed':
                self.embarrassedimages.append(pygame.image.load(filename))
            elif tag == 'questionmark':
                self.questionmarkimages.append(pygame.image.load(filename))
            elif tag == 'crying':
                self.cryingimages.append(pygame.image.load(filename))
            elif tag == 'shocked':
                self.shockedimages.append(pygame.image.load(filename))
            elif tag == 'silly':
                self.sillyimages.append(pygame.image.load(filename))
            elif tag == 'heart':
                self.heartimages.append(pygame.image.load(filename))
            elif tag == 'hypnotic':
                self.hypnoticimages.append(pygame.image.load(filename))
        self.index = 0
        self.image = self.images[0][self.index]
        self.rect = pygame.Rect(0, 0, 1600, 480)
    def update(self, ExpressionState, CurrentFrame = None):
        global frametime
        global currentframe
        if(time.clock() - frametime > 0.034): #30 FPS
            def imageAssign(i):
                switcher = {
                    0: self.trueneutralimages,
                    1: self.happyneutralimages,
                    2: self.dubiousneutralimages,
                    3: self.boredneutralimages,
                    4: self.aggressiveimages,
                    5: self.sleepingimages,
                    6: self.cheerfulimages,
                    7: self.embarrassedimages,
                    8: self.questionmarkimages,
                    9: self.cryingimages,
                    10: self.shockedimages,
                    11: self.sillyimages,
                    12: self.heartimages,
                    13: self.hypnoticimages
                }
                return switcher.get(i, "Invalid Expression")
            arr = imageAssign(ExpressionState)
            if CurrentFrame:
                self.index = CurrentFrame
            self.index += 1
            if self.index >= len(arr):
                self.index = 0
            self.image = arr[self.index]
            frametime = time.clock()
            currentframe = self.index
            Display.blit(self.image, self.image.get_rect())

my_sprite = EyesSprite()
my_group = pygame.sprite.Group(my_sprite)

def GraphicsRefresh(ExpressionState, CurrentFrame = None):
    my_group.update(ExpressionState, currentframe)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


import serial
RASPI = serial.Serial('/dev/ttyS0', 9600)
while(True):
    global ExpressionState
    global frametime
    global currentframe
    line = RASPI.readline.decode()
    if line:
        while RASPI.in_waiting():
            print(RASPI.readline())
        line.split("-")
        ExpressionState = int(line[0])
        currentframe = int(line[1])
        GraphicsRefresh(ExpressionState, currentframe)
    else:
        GraphicsRefresh(ExpressionState)