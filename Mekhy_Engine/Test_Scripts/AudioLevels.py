import sounddevice
import numpy
volume = 0

def GetVolume(indata, outdata, frames, time, status):
    global volume
    volume = (numpy.linalg.norm(indata)*6.375*0.5) + (volume*0.5)
    print(int(volume))
    
with sounddevice.Stream(callback=GetVolume):
    import printer
    sounddevice.sleep(99999)