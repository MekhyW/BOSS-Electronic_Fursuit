import aubio
import numpy
import pyaudio

BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE

pA = pyaudio.PyAudio()
mic = pA.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=PERIOD_SIZE_IN_FRAME)
volume = 0
volume_raw = 0
volume_array = [0] * BUFFER_SIZE

def rolling_mean(current_value, array):
    array.pop(0)
    array.append(current_value)
    mean = sum(array) / len(array)
    return mean, array

def getVolume():
    data = mic.read(PERIOD_SIZE_IN_FRAME)
    samples = numpy.fromstring(data, dtype=aubio.float_type)
    volume_raw = (volume_raw * 0.5) + ((numpy.sum(samples**2)/len(samples)) * 0.5)
    volume_mean, volume_array = rolling_mean(volume_raw, volume_array)
    volume = volume_raw/volume_mean
    return volume