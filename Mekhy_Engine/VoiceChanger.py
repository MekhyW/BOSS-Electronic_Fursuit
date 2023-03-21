import os
import time
import threading
os.system("pactl load-module module-echo-cancel")

def sox_thread(voice):
    print("Killing SoX windows")
    os.system("killall play")
    print("Setting new voice")
    if voice == 'Mekhy':
        os.system("lxterminal -e play '|rec --buffer 2048 -d pitch -250 bass 20'")
    elif voice == 'Demon':
        os.system("lxterminal -e play '|rec --buffer 2048 -d pitch -600 bass 30 reverb vol 0.2'")
    elif voice == 'Voice of Conscience':
        os.system("lxterminal -e play '|rec --buffer 2048 -d echo 0.8 0.9 200 0.3 bass 30 reverb vol 0.2'")
    elif voice == 'Baby':
        os.system("lxterminal -e play '|rec --buffer 2048 -d pitch 400 bass 20'")
    elif voice == 'Chipmunk':
        os.system("lxterminal -e play '|rec --buffer 2048 -d pitch 800'")
    elif voice == 'Earrape':
        os.system("lxterminal -e play '|rec --buffer 8192 -d bass 50'")
    elif voice == 'Radio':
        os.system("lxterminal -e play '|rec --buffer 2048 -d downsample 10'")
    elif voice == 'No Effects':
        os.system("lxterminal -e play '|rec --buffer 8192 -d'")
    elif voice == 'Mute':
        os.system("lxterminal -e play '|rec --buffer 8192 -d vol 0'")

def SetVoice(voice):
    soxthread = threading.Thread(target=sox_thread, args=(voice,))
    soxthread.start()

if __name__ == '__main__':
    SetVoice('No Effects')
    time.sleep(5)
    SetVoice('Mekhy')
    time.sleep(5)
    os.system("killall play")