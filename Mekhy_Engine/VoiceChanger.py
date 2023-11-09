import os
import time
import threading
#os.system("pactl load-module module-echo-cancel")
#os.system("pacmd set-default-source alsa_input.usb-Razer_Razer_Kraken_V3_X_00000000-00.iec958-stereo.echo-cancel")

def sox_thread(voice):
    print("Killing SoX windows")
    os.system("killall play")
    print("Setting new voice")
    if voice == 'Mekhy':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch -300 vol 10 band 40 5k'")
    elif voice == 'Demon':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch -600 bass 30 reverb vol 10 band 40 5k'")
    elif voice == 'Voice of Conscience':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d echo 0.8 0.9 200 0.3 bass 30 reverb vol 10 band 40 5k'")
    elif voice == 'Baby':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch 400 bass 20 vol 10 band 40 5k'")
    elif voice == 'Chipmunk':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch 800 vol 10 band 40 5k'")
    elif voice == 'Radio':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d downsample 10 vol 10 band 40 5k'")
    elif voice == 'No Effects':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 512 -d vol 10 band 40 5k'")
    elif voice == 'Mute':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 512 -d vol 0'")
    
def minimize_thread():
    time.sleep(3)
    os.system("xdotool getactivewindow windowminimize")

def SetVoice(voice):
    soxthread = threading.Thread(target=sox_thread, args=(voice,))
    minimizethread = threading.Thread(target=minimize_thread)
    soxthread.start()
    minimizethread.start()

if __name__ == '__main__':
    SetVoice('No Effects')
    time.sleep(5)
    SetVoice('Mekhy')
    time.sleep(5)
    os.system("killall play")