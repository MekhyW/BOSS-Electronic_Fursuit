import SoundEffects
#import HotwordActivator
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
Token = '1201452483:AAErTkoil0EDAyfprtCz6W0VC5AFEvVnTLQ'
mekhybot = telepot.Bot(Token)
from googletrans import Translator
translator = Translator()
from gtts import gTTS
import requests
import os
import random
import time
firstpass = True
start_time = time.time()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    current_keyboard = 'Main'
    global firstpass
    if time.time() - start_time > 3:
        firstpass = False
    if firstpass == False:
        if content_type == 'text':
            if msg['text'] == '/start':
                mekhybot.sendMessage(chat_id, 'Welcome!')
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)':
                mekhybot.sendMessage(chat_id, '>>>Speaking...')
                msgToSpeak = msg['text'].replace('/speak ', '')
                language = translator.detect(msgToSpeak).lang
                filename = "{}.mp3".format(msg['message_id'])
                gTTS(text=msgToSpeak, lang=language, slow=False).save(filename)
                SoundEffects.PlayOnDemand(filename)
            elif msg['text'] == 'Speak':
                mekhybot.sendMessage(chat_id, '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)')
            elif msg['text'] == 'Refsheet':
                mekhybot.sendMessage(chat_id, '>>>7 Files Detected 0w0\nLaunching Images....')
                for doc in os.listdir("FursonaRefs"):
                    opened = open("FursonaRefs/{}".format(doc), 'rb')
                    mekhybot.sendPhoto(chat_id, opened)
                mekhybot.sendMessage(chat_id, 'Success!')
            elif msg['text'] == 'Pronouns':
                mekhybot.sendMessage(chat_id, 'Please call me a He or They!\nI am Male ♂️ and Bisexual 🏳️‍🌈⚥')
            elif msg['text'] == 'Reboot':
                mekhybot.sendMessage(chat_id, '>>>System Reboot initiated.....')
                os.system("reboot")
            elif msg['text'] == 'Turn me off':
                mekhybot.sendMessage(chat_id, '>>>System Shutdown initiated.....\nI hope we meet again! :P')
                os.system("poweroff")
            elif msg['text'] == 'Stop sound':
                mekhybot.sendMessage(chat_id, '>>>OK')
                SoundEffects.StopSound()
            elif msg['text'] == 'Set Mood':
                current_keyboard = 'Choose Mood'
            elif msg['text'] == 'Neutral':
                mekhybot.sendMessage(chat_id, '>>>Mood Reverted back to Neutral')
                HotwordActivator.SetExpressionState(random.randint(0, 3))
            elif msg['text'] == '😡':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: Congratufuckinlations u made me PISSED')
                HotwordActivator.SetExpressionState(4)
            elif msg['text'] == 'Zzz':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: Nighty night')
                HotwordActivator.SetExpressionState(5)
            elif msg['text'] == '😊':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: A Happy boye')
                HotwordActivator.SetExpressionState(6)
            elif msg['text'] == '>w<':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: omg look he blushing')
                HotwordActivator.SetExpressionState(7)
            elif msg['text'] == '?w?':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: ??uhh..')
                HotwordActivator.SetExpressionState(8)
            elif msg['text'] == '😢':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: All around me are familiar faces')
                HotwordActivator.SetExpressionState(9)
            elif msg['text'] == '😱':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: BRUH')
                HotwordActivator.SetExpressionState(10)
            elif msg['text'] == '🤪':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: 🥔')
                HotwordActivator.SetExpressionState(11)
            elif msg['text'] == '😍':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: OHHH Somebody hold me')
                HotwordActivator.SetExpressionState(12)
            elif msg['text'] == 'Hypnotic 🌈':
                mekhybot.sendMessage(chat_id, '>>>Mood Set to: Look at me if u dare bitch')
                HotwordActivator.SetExpressionState(13)
            elif msg['text'] == 'Sound Effect':
                current_keyboard = 'Choose SFX'
            elif msg['text'] == 'AWOOO!':
                mekhybot.sendMessage(chat_id, '>>>Howling...')
                SoundEffects.PlaySound(1)
            elif msg['text'] == '*amgy*':
                mekhybot.sendMessage(chat_id, '>>>Snarling...')
                SoundEffects.PlaySound(2)
            elif msg['text'] == 'Woof! Woof!':
                mekhybot.sendMessage(chat_id, '>>>Woofing...')
                SoundEffects.PlaySound(3)
            elif msg['text'] == '*cry*':
                mekhybot.sendMessage(chat_id, '>>>Crying...')
                SoundEffects.PlaySound(4)
            elif msg['text'] == 'Huff':
                mekhybot.sendMessage(chat_id, '>>>Huffing...')
                SoundEffects.PlaySound(5)
            elif msg['text'] == '*snif snif*':
                mekhybot.sendMessage(chat_id, '>>>Sniffing...')
                SoundEffects.PlaySound(6)
            elif msg['text'] == 'Racc noises':
                mekhybot.sendMessage(chat_id, '>>>Chittering...')
                SoundEffects.PlaySound(7)
            elif msg['text'] == 'Fart':
                mekhybot.sendMessage(chat_id, '>>>Farting...')
                SoundEffects.PlaySound(8)
            elif msg['text'] == 'Stomach growl':
                mekhybot.sendMessage(chat_id, '>>>Growling...')
                SoundEffects.PlaySound(9)
            elif msg['text'] == '⬅️(Back to commands)':
                current_keyboard = 'Main'
            else:
                mekhybot.sendMessage(chat_id, msg['text'])
        elif content_type == 'photo':
            mekhybot.sendMessage(chat_id, 'Sorry, I can´t interpret images')
        elif content_type == 'voice':
            print(msg['voice']['file_id'])
            mekhybot.sendMessage(chat_id, '>>>Voice Received!')
            f = requests.get("https://api.telegram.org/bot{}/getFile?file_id={}".format(Token, msg['voice']['file_id'])).text
            file_path = f.split(",")[4].split(":")[1].replace('"', '').replace('}', '')
            file_name = file_path.split("/")[1]
            r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
            open(file_name, 'wb').write(r.content)
            #convert OGA file to something readable
            #SoundEffects.PlayOnDemand()
            #mekhybot.sendMessage(chat_id, '>>>Playing.....\n\nInvoke /stopsound to make me stop òwó') 
        elif content_type == 'audio':
            print(msg['audio']['file_id'])
            mekhybot.sendMessage(chat_id, '>>>Audio Received!')
            f = requests.get("https://api.telegram.org/bot{}/getFile?file_id={}".format(Token, msg['audio']['file_id'])).text
            file_path = f.split(",")[4].split(":")[1].replace('"', '').replace('}', '')
            file_name = file_path.split("/")[1]
            r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
            open(file_name, 'wb').write(r.content)
            SoundEffects.PlayOnDemand(file_name)
            mekhybot.sendMessage(chat_id, '>>>Playing.....\n\nInvoke /stopsound to make me stop òwó')
        elif content_type == 'document':
            mekhybot.sendMessage(chat_id, 'Sorry, I cannot read images and documents.\nPlease forward to @MekhyW')
        if current_keyboard == 'Main':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Set Mood"), KeyboardButton(text="Sound Effect")], [KeyboardButton(text="Speak")], [KeyboardButton(text="Refsheet"), KeyboardButton(text="Pronouns")], [KeyboardButton(text="Stop sound"), KeyboardButton(text="Reboot"), KeyboardButton(text="Turn me off")]])
            mekhybot.sendMessage(chat_id, '>>>Awaiting -Command- or -Audio-', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Mood':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️(Back to commands)")], [KeyboardButton(text="Neutral")], [KeyboardButton(text="😡"), KeyboardButton(text="Zzz"), KeyboardButton(text="😊"), KeyboardButton(text=">w<"), KeyboardButton(text="?w?")], [KeyboardButton(text="😢"), KeyboardButton(text="😱"), KeyboardButton(text="🤪"), KeyboardButton(text="😍"), KeyboardButton(text="Hypnotic 🌈")]])
            mekhybot.sendMessage(chat_id, '>>>Which mood?', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose SFX':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️(Back to commands)")], [KeyboardButton(text="AWOOO!"), KeyboardButton(text="*amgy*"), KeyboardButton(text="Woof! Woof!"), KeyboardButton(text="*cry*")], [KeyboardButton(text="Huff"), KeyboardButton(text="*snif snif*"), KeyboardButton(text="Racc noises"), KeyboardButton(text="Fart"), KeyboardButton(text="Stomach growl")]])
            mekhybot.sendMessage(chat_id, '>>>Which SFX?', reply_markup=command_keyboard)
MessageLoop(mekhybot, handle).run_as_thread()
print('Listening in 3...')

while 1:
    time.sleep(2)
