import os
Pitch = -325
Bass = 20
os.system('pacmd set-default-source "alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono"')
os.system("pactl load-module module-echo-cancel")
os.system('pacmd set-default-sink "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo"')
os.system("play '|rec -d pitch {} bass {}'".format(Pitch, Bass))