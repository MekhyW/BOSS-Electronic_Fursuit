import os
import time
import threading
os.system("pactl unload-module module-echo-cancel")
os.system("pactl load-module module-echo-cancel aec_method=webrtc source_name=echocancel sink_name=echocancel1")
os.system("pacmd set-default-source echocancel")
os.system("pacmd set-default-sink echocancel1")

def sox_thread(voice):
    print("Killing SoX windows")
    os.system("killall play")
    print("Setting new voice")
    if voice == 'Mekhy':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch -300 band 40 5k'")
    elif voice == 'Demon':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch -600 bass 30 reverb band 40 5k'")
    elif voice == 'Voice of Conscience':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d echo 0.8 0.9 200 0.3 bass 30 reverb band 40 5k'")
    elif voice == 'Baby':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch 400 bass 20 band 40 5k'")
    elif voice == 'Chipmunk':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d pitch 800 band 40 5k'")
    elif voice == 'Radio':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 128 -d downsample 10 band 40 5k'")
    elif voice == 'No Effects':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 512 -d band 40 5k'")
    elif voice == 'Mute':
        os.system("lxterminal -e play '|rec -c 2 -b 16 -r 44100 --buffer 512 -d vol 0'")

def SetVoice(voice):
    soxthread = threading.Thread(target=sox_thread, args=(voice,))
    soxthread.start()

if __name__ == '__main__':
    SetVoice('No Effects')
    time.sleep(5)
    SetVoice('Mekhy')
    time.sleep(5)
    os.system("killall play")