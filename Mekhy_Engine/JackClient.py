import jack
import os
# Declare client and the software ports of our script
client = jack.Client('BOSS')
in1 = client.inports.register('BOSS_in1')
in2 = client.inports.register('BOSS_in2')
out1 = client.outports.register('BOSS_out1')
out2 = client.outports.register('BOSS_out2')
# Start client and setup dongle-to-headphone route
client.activate()
os.system("lxterminal -e alsa_in -d hw:0")
os.system("lxterminal -e alsa_out -d hw:1")
client.connect("alsa_in:capture_1", "alsa_out:playback_1")
client.connect("alsa_in:capture_2", "alsa_out:playback_2")
client.connect(out1, "system:playback_1")
client.connect(out2, "system:playback_2")

def JackVoicemodRoute(voice):
    os.system("killall jack-rack")
    os.system("lxterminal -e jack-rack ../Voices/{}".format(voice))
    client.connect("system:capture_1", "jack_rack:in_1")
    client.connect("system:capture_2", "jack_rack:in_2")
    client.connect("jack_rack:out_1", "system:playback_1")
    client.connect("jack_rack:out_2", "system:playback_2")
    client.connect("system:capture_1", in1)
    client.connect("system:capture_2", in2)