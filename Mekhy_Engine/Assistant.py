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
    pcms = []
    for i in range(0, int(16000 / 512 * 5)):
        pcm = recorder.read()
        pcms.append(pcm)
    for pcm in pcms:
        wavfile.writeframes(struct.pack("h" * len(pcm), *pcm))
    wavfile.close()

def assistant_query(query):
    query = query.capitalize()
    completion = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {query}\nAnswer: ",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n", " User:", " AI:"],
    )
    answer = completion.choices[0].text
    return answer

def trigger():
    print("Triggered")
    recorder.stop()
    SoundEffects.PlayOnDemand("resources/assistant_listening.wav", remove_file=False)
    time.sleep(0.5)
    print("Recording")
    recorder.start()
    record_query()
    recorder.stop()
    SoundEffects.PlayOnDemand("resources/assistant_ok.wav", remove_file=False)
    with open("resources/query.wav", "rb") as query:
        transcript = openai.Audio.transcribe("whisper-1", query)['text']
    query.close()
    print(transcript)
    answer = assistant_query(transcript)
    if len(answer):
        print(answer)
        SoundEffects.TTS(answer)
    else:
        print("No answer")
    recorder.start()

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