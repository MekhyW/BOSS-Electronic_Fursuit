import os
os.system("pactl load-module module-echo-cancel")

def SetVoice(voice):
    os.system("killall play")
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