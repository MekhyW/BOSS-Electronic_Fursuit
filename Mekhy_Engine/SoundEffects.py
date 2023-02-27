import os, subprocess
import time
import pygame
pygame.mixer.init()
pygame.init()

def PlayBootSound():
    pygame.mixer.Sound('resources/sfx_WINDOWSXPBOOT.wav').play()

def StopSound():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def PlayOnDemand(file_name, remove_file=True):
    extension = file_name.split('.')[1]
    if extension in ('mp3', 'xm'):
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
    else:
        if not extension in ('wav', 'ogg'):
            new_filename = file_name.split('.')[0] + '.wav'
            subprocess.call(["ffmpeg", "-i", file_name, new_filename])
            sound = pygame.mixer.Sound(new_filename)
            sound.play()
            os.remove(new_filename)
        else:
            sound = pygame.mixer.Sound(file_name)
            sound.play()
    if remove_file:
        os.remove(file_name)

if __name__ == '__main__':
    PlayBootSound()
    time.sleep(5)
    PlayOnDemand('resources/sfx_WINDOWSXPBOOT.wav', False)
    time.sleep(2)
    StopSound()
    PlayOnDemand('resources/file_example_MP3_700KB.mp3', False)
    time.sleep(5)
    StopSound()
