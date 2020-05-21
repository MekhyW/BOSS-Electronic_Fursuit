import os
import time 
import pygame
pygame.init()
Display = pygame.display.set_mode((1600, 480))
frametime = 0

class BoxSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(BoxSprite, self).__init__()
        self.boximages = []
        self.circleimages = []
        files = os.listdir('.')
        files.sort()
        for filename in files:
            tag = filename.split("_")[0]
            if tag == 'box':
                self.boximages.append(pygame.image.load(filename))
            if tag == 'circle':
                self.circleimages.append(pygame.image.load(filename))
        self.index = 0
        self.image = self.boximages[self.index]
        self.rect = pygame.Rect(0, 0, 1600, 480)
    def update(self, ExpressionState):
        global frametime
        if(time.clock() - frametime > 0.034): #30 FPS
            def imageAssign(i):
                switcher = {
                    0: self.boximages,
                    1: self.circleimages
                }
                return switcher.get(i, "Invalid Shape")
            arr = imageAssign(ExpressionState)
            self.index += 1
            if self.index >= len(arr):
                self.index = 0
            self.image = arr[self.index]
            frametime = time.clock()
            Display.blit(self.image, self.image.get_rect())

my_sprite = BoxSprite()
my_group = pygame.sprite.Group(my_sprite)

while True:
    if(time.clock() < 5):
        my_group.update(0)
    else:
        my_group.update(1)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()