import os
Pitch = -350
Bass = 20

def SetVoice(voice):
    global Pitch
    global Bass
    os.system("killall play")
    if voice == 'Mekhy':
        os.system("lxterminal -e play '|rec --buffer 512 -d pitch {} bass {}'".format(Pitch, Bass))
    elif voice == 'Baby':
        os.system("lxterminal -e play '|rec --buffer 512 -d pitch {}'".format(abs(Pitch*2)))
    elif voice == 'No Effects':
        os.system("lxterminal -e play '|rec --buffer 512 -d'")
    elif voice == 'Mute':
        os.system("lxterminal -e play '|rec --buffer 512 -d vol 0'")

os.system('pacmd set-default-source "alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono"')
os.system("pactl load-module module-echo-cancel")
os.system('pacmd set-default-sink "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo"')

SetVoice('Mekhy')