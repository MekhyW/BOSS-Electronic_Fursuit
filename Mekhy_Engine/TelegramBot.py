import SoundEffects
import VoiceMod
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
Token = ''
fursuitbot = telepot.Bot(Token)
mekhyID = 780875868
from googletrans import Translator
translator = Translator()
from gtts import gTTS
from pytube import YouTube
import requests, os, subprocess, math, time
import traceback
start_time = time.time()
ExpressionState = 0

updates = fursuitbot.getUpdates()
if updates:
    last_update_id = updates[-1]['update_id']
    fursuitbot.getUpdates(offset=last_update_id+1)

fursuitbot.sendMessage(mekhyID, 'I am online')

def handle(msg):
    try:
        global ExpressionState
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        current_keyboard = 'Main'
        if content_type == 'text':
            if msg['text'] == '/start':
                fursuitbot.sendMessage(chat_id, 'Welcome!')
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with any song name to search and play\n\nExample: bohemian rhapsody':
                fursuitbot.sendMessage(chat_id, '>>>Finding song with query "{}"...'.format(msg['text']))
                topic = msg['text']
                count = 0
                lst = str(requests.get('https://www.youtube.com/results?q=' + topic).content).split('"')
                for i in lst:
                    count+=1
                    if i == 'WEB_PAGE_TYPE_WATCH':
                        break
                if lst[count-5] == "/results":
                    raise Exception("No video found.")
                fursuitbot.sendMessage(chat_id, '>>>Song found!')
                fursuitbot.sendMessage(chat_id, '>>>Downloading...')
                video = YouTube("https://www.youtube.com"+lst[count-5]).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                video.download()
                fursuitbot.sendMessage(chat_id, '>>>Conversion process...')
                default_filename = video.default_filename
                new_filename = default_filename.split(".")[0] + ".mp3"
                subprocess.call(["ffmpeg", "-i", default_filename, new_filename])
                fursuitbot.sendMessage(chat_id, 'Done!\n>>>Playing now')
                SoundEffects.PlayOnDemand(new_filename)
            elif msg['text'] == 'Play Song':
                fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with any song name to search and play\n\nExample: bohemian rhapsody')
                current_keyboard = 'none'
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)':
                fursuitbot.sendMessage(chat_id, '>>>Speaking...')
                msgToSpeak = msg['text'].replace('/speak ', '')
                language = translator.detect(msgToSpeak).lang
                filename = "{}.mp3".format(msg['message_id'])
                gTTS(text=msgToSpeak, lang=language, slow=False).save(filename)
                SoundEffects.PlayOnDemand(filename)
            elif msg['text'] == 'Speak':
                fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)')
                current_keyboard = 'none'
            elif msg['text'] == 'Reboot':
                if chat_id==mekhyID:
                    fursuitbot.sendMessage(chat_id, '>>>System Reboot initiated.....')
                    os.system("reboot")
                else:
                    fursuitbot.sendMessage(chat_id, 'This command can only be used by myself!')
            elif msg['text'] == 'Turn me off':
                if chat_id==mekhyID:
                    fursuitbot.sendMessage(chat_id, '>>>System Shutdown initiated.....')
                    os.system("poweroff")
                else:
                    fursuitbot.sendMessage(chat_id, 'This command can only be used by myself!')
            elif msg['text'] == 'Running time':
                s = time.time() - start_time
                if s >= 3600:
                    fursuitbot.sendMessage(chat_id, 'Suit active for: {} Hours + {} Minutes'.format(int(math.floor(s/3600)), str((s - (3600 * math.floor(s/3600)))/60)[:4]))
                else:
                    fursuitbot.sendMessage(chat_id, 'Suit active for: {} Minutes'.format(str(s/60)[:4]))
            elif msg['text'] == 'Stop sound':
                fursuitbot.sendMessage(chat_id, '>>>OK')
                SoundEffects.StopSound()
            elif msg['text'] == 'Set Mood':
                current_keyboard = 'Choose Mood'
            elif msg['text'] == 'Neutral':
                fursuitbot.sendMessage(chat_id, '>>>Mood Reverted back to Neutral')
                ExpressionState = 0
            elif msg['text'] == '😡':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 😡')
                ExpressionState = 1
            elif msg['text'] == 'Zzz':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: Zzz')
                ExpressionState = 2
            elif msg['text'] == '😢':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 😢')
                ExpressionState = 3
            elif msg['text'] == '😊':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 😊')
                ExpressionState = 4
            elif msg['text'] == '>w<':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: >w<')
                ExpressionState = 5
            elif msg['text'] == '?w?':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: ?w?')
                ExpressionState = 6
            elif msg['text'] == '😱':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 😱')
                ExpressionState = 7
            elif msg['text'] == '🤪':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 🤪')
                ExpressionState = 8
            elif msg['text'] == '😍':
                fursuitbot.sendMessage(chat_id, '>>>Mood Set to: 😍')
                ExpressionState = 9
            elif msg['text'] == 'Hypno 🌈':
                fursuitbot.sendMessage(chat_id, 'Hypno 🌈')
                ExpressionState = 10
            elif msg['text'] == 'Change Voice':
                current_keyboard = 'Choose Voice'
            elif msg['text'] in ('Mekhy', 'Baby Mekhy', 'No Effects', 'Mute'):
                fursuitbot.sendMessage(chat_id, '>>>Voice Set to: {}'.format(msg['text']))
                VoiceMod.SetVoice(msg['text'])
            elif msg['text'] == '⬅️(Back to commands)':
                current_keyboard = 'Main'
            else:
                try:
                    requests.get("{}".format(msg['text']))
                    fursuitbot.sendMessage(chat_id, 'Valid link received!\n>>>Forwarding to @MekhyW...OK')
                    fursuitbot.sendMessage(mekhyID, msg['text'])
                except:
                    fursuitbot.sendMessage(chat_id, msg['text'])
        elif content_type == 'voice':
            print(msg['voice']['file_id'])
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot play voice messages.\nPlease forward to @MekhyW')
        elif content_type == 'video':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot play video sounds.\nPlease forward to @MekhyW')
        elif content_type == 'audio':
            print(msg['audio']['file_id'])
            fursuitbot.sendMessage(chat_id, '>>>Audio Received!')
            f = requests.get("https://api.telegram.org/bot{}/getFile?file_id={}".format(Token, msg['audio']['file_id'])).text
            file_path = f.split(",")[4].split(":")[1].replace('"', '').replace('}', '')
            file_name = file_path.split("/")[1]
            r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
            open(file_name, 'wb').write(r.content)
            SoundEffects.PlayOnDemand(file_name)
            fursuitbot.sendMessage(chat_id, '>>>Playing.....\n\nInvoke /stopsound to make me stop òwó')
        elif content_type == 'photo':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot interpret images.\nPlease forward to @MekhyW')
        elif content_type == 'document':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot read images and documents.\nPlease forward to @MekhyW')
        elif content_type == 'location':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot read location data.\nPlease forward to @MekhyW')
        elif content_type == 'sticker':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot interpret stickers.\nPlease forward to @MekhyW')
        elif content_type == 'contact':
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot use contacts.\nPlease forward to @MekhyW')
        if current_keyboard == 'Main':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Play Song"), KeyboardButton(text="Stop sound")], [KeyboardButton(text="Set Mood")], [KeyboardButton(text="Speak"), KeyboardButton(text="Change Voice")], [KeyboardButton(text="Running time")], [KeyboardButton(text="Reboot"), KeyboardButton(text="Turn me off")]], resize_keyboard=True)
            fursuitbot.sendMessage(chat_id, '>>>Awaiting -Command- or -Audio- or -Link-', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Mood':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️(Back to commands)")], [KeyboardButton(text="Neutral")], [KeyboardButton(text="😡"), KeyboardButton(text="Zzz"), KeyboardButton(text="😊"), KeyboardButton(text=">w<"), KeyboardButton(text="?w?")], [KeyboardButton(text="😢"), KeyboardButton(text="😱"), KeyboardButton(text="🤪"), KeyboardButton(text="😍"), KeyboardButton(text="Hypno 🌈")]])
            fursuitbot.sendMessage(chat_id, '>>>Which mood?', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Voice':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️(Back to commands)")], [KeyboardButton(text="Mekhy")], [KeyboardButton(text="Baby Mekhy")], [KeyboardButton(text="No Effects")], [KeyboardButton(text="Mute")]])
            fursuitbot.sendMessage(chat_id, '>>>What voice?', reply_markup=command_keyboard)
    except:
        if 'ConnectionResetError' not in traceback.format_exc():
            fursuitbot.sendMessage(mekhyID, traceback.format_exc())
            fursuitbot.sendMessage(mekhyID, str(msg))

MessageLoop(fursuitbot, handle).run_as_thread()

#while True:
#    pass