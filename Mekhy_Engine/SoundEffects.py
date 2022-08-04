import os
import pygame
pygame.mixer.init()
pygame.init()
pygame.mixer.Sound('sfx_WINDOWSXPBOOT.wav').play()

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