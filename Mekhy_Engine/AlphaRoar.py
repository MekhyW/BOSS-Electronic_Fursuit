import math
import random
import pygame
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

def howl(x):
    return {
        1: sfx_howl1.play(),
        2: sfx_howl2.play(),
        3: sfx_howl3.play()
    }[x]

def snarl(x):
    return {
        1: sfx_snarl1.play(),
        2: sfx_snarl2.play(),
        3: sfx_snarl3.play()
    }[x]

def woof(x):
    return {
        1: sfx_woof1.play(),
        2: sfx_woof2.play(),
        3: sfx_woof3.play()
    }[x]

def cry(x):
    return {
        1: sfx_cry1.play(),
        2: sfx_cry2.play(),
        3: sfx_cry3.play()
    }[x]

def huff(x):
    return {
        1: sfx_huff1.play(),
        2: sfx_huff2.play(),
        3: sfx_huff3.play()
    }[x]

def sniff(x):
    return {
        1: sfx_sniff1.play(),
        2: sfx_sniff2.play(),
        3: sfx_sniff3.play()
    }[x]

def chitter(x):
    return {
        1: sfx_chitter1.play(),
        2: sfx_chitter2.play()
    }[x]

def fart(x):
    return {
        1: sfx_fart1.play(),
        2: sfx_fart2.play(),
        3: sfx_fart3.play()
    }[x]

def growl(x):
    return {
        1: sfx_growl1.play(),
        2: sfx_growl2.play(),
        3: sfx_growl3.play()
    }[x]

def PlaySound(x):
    return {
        1: howl(random.randint(1, 3)),
        2: snarl(random.randint(1, 3)),
        3: woof(random.randint(1, 3)),
        4: cry(random.randint(1, 3)),
        5: huff(random.randint(1, 3)),
        6: sniff(random.randint(1, 3)),
        7: chitter(random.randint(1, 2)),
        8: fart(random.randint(1, 3)),
        9: growl(random.randint(1, 3))
    }[x]