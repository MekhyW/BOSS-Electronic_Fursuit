import math
import random
import os
import pygame
import wave
pygame.mixer.init(frequency=wave.open('sfx_WINDOWSXPBOOT.wav').getframerate())
pygame.init()
pygame.mixer.Sound('sfx_WINDOWSXPBOOT.wav').play()
sfx_howl1 = pygame.mixer.Sound('sfx_howl1.wav')
sfx_howl2 = pygame.mixer.Sound('sfx_howl2.wav')
sfx_howl3 = pygame.mixer.Sound('sfx_howl3.wav')
sfx_snarl1 = pygame.mixer.Sound('sfx_snarl1.wav')
sfx_snarl2 = pygame.mixer.Sound('sfx_snarl2.wav')
sfx_snarl3 = pygame.mixer.Sound('sfx_snarl3.wav')
sfx_woof1 = pygame.mixer.Sound('sfx_woof1.wav')
sfx_woof2 = pygame.mixer.Sound('sfx_woof2.wav')
sfx_woof3 = pygame.mixer.Sound('sfx_woof3.wav')
sfx_cry1 = pygame.mixer.Sound('sfx_cry1.wav')
sfx_cry2 = pygame.mixer.Sound('sfx_cry2.wav')
sfx_cry3 = pygame.mixer.Sound('sfx_cry3.wav')
sfx_huff1 = pygame.mixer.Sound('sfx_huff1.wav')
sfx_huff2 = pygame.mixer.Sound('sfx_huff2.wav')
sfx_huff3 = pygame.mixer.Sound('sfx_huff3.wav')
sfx_sniff1 = pygame.mixer.Sound('sfx_sniff1.wav')
sfx_sniff2 = pygame.mixer.Sound('sfx_sniff2.wav')
sfx_sniff3 = pygame.mixer.Sound('sfx_sniff3.wav')
sfx_chitter1 = pygame.mixer.Sound('sfx_chitter1.wav')
sfx_chitter2 = pygame.mixer.Sound('sfx_chitter2.wav')
sfx_fart1 = pygame.mixer.Sound('sfx_fart1.wav')
sfx_fart2 = pygame.mixer.Sound('sfx_fart2.wav')
sfx_fart3 = pygame.mixer.Sound('sfx_fart3.wav')
sfx_growl1 = pygame.mixer.Sound('sfx_growl1.wav')
sfx_growl2 = pygame.mixer.Sound('sfx_growl2.wav')
sfx_growl3 = pygame.mixer.Sound('sfx_growl3.wav')
for x in os.listdir():
    if '.mp3' in x or '.xm' in x:
        os.remove(x)

def StopSound():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def PlayOnDemand(file_name):
    extension = file_name.split('.')[1]
    print(extension)
    if extension in ('wav', 'ogg'):
        sound = pygame.mixer.Sound(file_name)
        sound.play()
        os.remove(file_name)
    elif extension in ('mp3', 'xm'):
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()

def howl(x):
    if x == 1:
        sfx_howl1.play()
    elif x == 2:
        sfx_howl2.play()
    elif x == 3:
        sfx_howl3.play()

def snarl(x):
    if x == 1:
        sfx_snarl1.play()
    elif x == 2:
        sfx_snarl2.play()
    elif x == 3:
        sfx_snarl3.play()

def woof(x):
    if x == 1:
        sfx_woof1.play()
    elif x == 2:
        sfx_woof2.play()
    elif x == 3:
        sfx_woof3.play()

def cry(x):
    if x == 1:
        sfx_cry1.play()
    elif x == 2:
        sfx_cry2.play()
    elif x == 3:
        sfx_cry3.play()

def huff(x):
    if x == 1:
        sfx_huff1.play()
    elif x == 2:
        sfx_huff2.play()
    elif x == 3:
        sfx_huff3.play()

def sniff(x):
    if x == 1:
        sfx_sniff1.play()
    elif x == 2:
        sfx_sniff2.play()
    elif x == 3:
        sfx_sniff3.play()

def chitter(x):
    if x == 1:
        sfx_chitter1.play()
    elif x == 2:
        sfx_chitter2.play()

def fart(x):
    if x == 1:
        sfx_fart1.play()
    elif x == 2:
        sfx_fart2.play()
    elif x == 3:
        sfx_fart3.play()

def growl(x):
    if x == 1:
        sfx_growl1.play()
    elif x == 2:
        sfx_growl2.play()
    elif x == 3:
        sfx_growl3.play()

def PlaySound(x):
    if x == 1:
        howl(random.randint(1, 3))
    elif x == 2:
        snarl(random.randint(1, 3))
    elif x == 3:
        woof(random.randint(1, 3))
    elif x == 4:
        cry(random.randint(1, 3))
    elif x == 5:
        huff(random.randint(1, 3))
    elif x == 6:
        sniff(random.randint(1, 3))
    elif x == 7:
        chitter(random.randint(1, 2))
    elif x == 8:
        fart(random.randint(1, 3))
    elif x == 9:
        growl(random.randint(1, 3))