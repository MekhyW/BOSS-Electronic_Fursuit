import SoundEffects
import openai
import pvporcupine
from pvrecorder import PvRecorder
import struct
import wave
import time
import json
openai.api_key = json.load(open("resources/credentials.json"))["openai_key"]
porcupine_access_key = json.load(open("resources/credentials.json"))["porcupine_key"]
keyword_paths = ["resources/Cookie-Bot_en_raspberry-pi_v2_1_0.ppn"]
porcupine = pvporcupine.create(access_key=porcupine_access_key, keyword_paths=keyword_paths)
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

def record_query():
    wavfile = wave.open("resources/query.wav", "wb")
    wavfile.setparams((1, 2, 16000, 512, "NONE", "NONE"))
    for i in range(0, int(16000 / 512 * 5)):
        pcm = recorder.read()
        wavfile.writeframes(struct.pack("h" * len(pcm), *pcm))
    wavfile.close()

def trigger():
    SoundEffects.PlayOnDemand("resources/assistant_listening.wav", remove_file=False)
    time.sleep(0.5)
    record_query()
    SoundEffects.PlayOnDemand("resources/assistant_ok.wav", remove_file=False)
    with open("resources/query.wav", "rb") as query:
        transcript = openai.Audio.transcribe("whisper-1", query)
    query.close()
    completion = openai.Completion.create(
        engine="davinci",
        prompt=transcript,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n", " User:", " AI:"],
    )
    SoundEffects.TTS(completion.choices[0].text)

def start():
    recorder.start()

def refresh():
    keyword_index = porcupine.process(recorder.read())
    if keyword_index >= 0:
        trigger()

if __name__ == "__main__":
    start()
    while True:
        refresh()