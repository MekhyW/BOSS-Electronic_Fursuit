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
previous_questions = ["Who won the world series in 2020?", "Você é fofo!"]
previous_answers = ["The Los Angeles Dodgers", "Não, você que é fofo! UwU"]
status_code = 'Ok'

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
    global previous_question, previous_answer
    query = query.capitalize()
    prompt_beginning = "You are a helpful and silly assistant. Your name is Cookie Bot. Respond in the same language as the question"
    messages=[{"role": "system", "content": prompt_beginning}]
    for i in range(len(previous_questions)):
        messages.append({"role": "user", "content": previous_questions[i]})
        messages.append({"role": "assistant", "content": previous_answers[i]})
    messages.append({"role": "user", "content": query})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    answer = completion.choices[0].message.content
    if len(query) and len(answer):
        previous_questions.append(query)
        previous_answers.append(answer)
    return answer

def trigger():
    global status_code
    status_code = 'Assistant listening'
    print("Triggered")
    recorder.stop()
    SoundEffects.PlayOnDemand("resources/assistant_listening.wav", remove_file=False)
    time.sleep(0.5)
    print("Recording")
    recorder.start()
    record_query()
    recorder.stop()
    print("Processing")
    status_code = 'Assistant processing'
    SoundEffects.PlayOnDemand("resources/assistant_ok.wav", remove_file=False)
    with open("resources/query.wav", "rb") as query:
        print("Transcribing")
        transcript = openai.Audio.transcribe("whisper-1", query)['text']
    query.close()
    print(transcript)
    answer = assistant_query(transcript)
    status_code = 'Assistant responding'
    if len(answer):
        print(answer)
        SoundEffects.TTS(answer)
    else:
        print("No answer")
        SoundEffects.TTS("I don't have an answer to that")
    status_code = 'Ok'
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