#https://www.raspberrypi-spy.co.uk/2017/03/amplified-voice-changer-using-a-raspberry-pi-zero/
#https://hackaday.com/2015/10/30/raspberry-pi-halloween-voice-changer/
#http://sox.sourceforge.net/sox.html
import os
os.system("play '|rec -d pitch -200 bass +10'")