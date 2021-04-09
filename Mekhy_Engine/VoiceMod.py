import os
Pitch = -350
Bass = 20
os.system('pacmd set-default-source "alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono"')
os.system("pactl load-module module-echo-cancel")
os.system('pacmd set-default-sink "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo"')
os.system("gnome-terminal -x play '|rec --buffer 128 -d pitch {} bass {}'".format(Pitch, Bass))

def SetVoice(voice):
    global Pitch
    global Bass
    os.system("killall play")
    if voice == 'Mekhy':
        os.system("gnome-terminal -x play '|rec --buffer 512 -d pitch {} bass {}'".format(Pitch, Bass))
    elif voice == 'Baby Mekhy':
        os.system("gnome-terminal -x play '|rec --buffer 512 -d pitch {} bass {}'".format(abs(Pitch), Bass))
    elif voice == 'No Effects':
        os.system("gnome-terminal -x play '|rec --buffer 512 -d'")
    elif voice == 'Mute':
        os.system("gnome-terminal -x play '|rec --buffer 512 -d vol 0'")