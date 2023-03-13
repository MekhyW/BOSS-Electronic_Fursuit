import os, subprocess
import time
import random
from gtts import gTTS
from googletrans import Translator
import pygame
translator = Translator()
pygame.mixer.init()
pygame.init()

def PlayBootSound():
    pygame.mixer.Sound('resources/sfx_WINDOWSXPBOOT.wav').play()

def StopSound():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
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

def SoundEffect(sfx_name):
    num = random.randint(1, 3)
    PlayOnDemand(f"resources/sfx/sfx_{sfx_name}{num}.wav", False)

def TTS(text):
    language = translator.detect(text).lang
    tts = gTTS(text=text, lang=language, slow=False)
    StopSound()
    tts.save("resources/tts.mp3")
    PlayOnDemand("resources/tts.mp3", False)

if __name__ == '__main__':
    PlayBootSound()
    time.sleep(5)
    PlayOnDemand('resources/sfx_WINDOWSXPBOOT.wav', False)
    time.sleep(2)
    StopSound()
    PlayOnDemand('resources/file_example_MP3_700KB.mp3', False)
    time.sleep(5)
    StopSound()
    TTS("Coé rapaziada blz?")
    time.sleep(2)
    TTS("Tudo certo?")
    time.sleep(2)
