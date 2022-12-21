import jack
import os
# Declare client and the software ports of our script
client = jack.Client('BOSS')
in1 = client.inports.register('BOSS_in1')
in2 = client.inports.register('BOSS_in2')
out1 = client.outports.register('BOSS_out1')
out2 = client.outports.register('BOSS_out2')
client.activate()
os.system("lxterminal -e alsa_in -d plughw:CARD=X,DEV=0 -j kraken_mic")
os.system("lxterminal -e alsa_out -d front:CARD=X,DEV=0 -j kraken_headphones")
os.system("lxterminal -e alsa_out -d hw:CARD=Headphones,DEV=0 -j speaker")
client.connect(out1, "speaker:playback_1")
client.connect(out2, "speaker:playback_2")

def JackVoicemodRoute(voice):
    os.system("killall jack-rack")
    os.system("lxterminal -e jack-rack ../Voices/{}".format(voice))
    client.connect("kraken_mic:capture_1", "jack_rack:in_1")
    client.connect("kraken_mic:capture_2", "jack_rack:in_2")
    client.connect("kraken_mic:capture_1", in1)
    client.connect("kraken_mic:capture_2", in2)
    client.connect("jack_rack:out_1", "speaker:playback_1")
    client.connect("jack_rack:out_2", "speaker:playback_2")
    client.connect("jack_rack:out_1", "kraken_headphones:playback_1")
    client.connect("jack_rack:out_2", "kraken_headphones:playback_2")