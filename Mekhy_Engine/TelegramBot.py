import SoundEffects
import Displays
import VoiceChanger
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
manual_expression_mode = False
ManualExpression = 'Neutral'
voices = ['Mekhy', 'Demon', 'Voice of Conscience', 'Baby', 'Chipmunk', 'Earrape', 'Radio', 'No Effects', 'Mute']
expressions = ['Neutral', '😡', '😒', '😢', '😊', '😱', '😍', 'Hypno 🌈', '😏', '😈']

updates = fursuitbot.getUpdates()
if updates:
    last_update_id = updates[-1]['update_id']
    fursuitbot.getUpdates(offset=last_update_id+1)

fursuitbot.sendMessage(mekhyID, 'I am online')

def SetExpression(fursuitbot, chat_id, msg):
    global ManualExpression, manual_expression_mode
    manual_expression_mode = True
    if msg['text'] == 'Neutral':
        ManualExpression = 0
    elif msg['text'] == '😡':
        ManualExpression = 'Angry'
    elif msg['text'] == '😒':
        ManualExpression = 'Disgusted'
    elif msg['text'] == '😢':
        ManualExpression = 'Sad'
    elif msg['text'] == '😊':
        ManualExpression = 'Happy'
    elif msg['text'] == '😱':
        ManualExpression = 'Scared'
    elif msg['text'] == '😍':
        ManualExpression = 'Heart'
    elif msg['text'] == 'Hypno 🌈':
        ManualExpression = 'Hypnotic'
    elif msg['text'] == '😏':
        ManualExpression = 'Sexy'
    elif msg['text'] == '😈':
        ManualExpression = 'Demonic'
    fursuitbot.sendMessage(chat_id, '>>>Mood Set to: {}'.format(msg['text']))

def toggleAutoMood(fursuitbot, chat_id, msg):
    global manual_expression_mode
    if manual_expression_mode:
        manual_expression_mode = False
        fursuitbot.sendMessage(chat_id, '>>>Auto Mood Enabled (ON)')
    else:
        manual_expression_mode = True
        fursuitbot.sendMessage(chat_id, '>>>Auto Mood Disabled (OFF)')

def PlaySongName(fursuitbot, chat_id, msg):
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

def TTS(fursuitbot, chat_id, msg):
    fursuitbot.sendMessage(chat_id, '>>>Speaking...')
    msgToSpeak = msg['text'].replace('/speak ', '')
    language = translator.detect(msgToSpeak).lang
    filename = "{}.mp3".format(msg['message_id'])
    gTTS(text=msgToSpeak, lang=language, slow=False).save(filename)
    SoundEffects.PlayOnDemand(filename)

def PlayVideoFile(fursuitbot, chat_id, msg):
    fursuitbot.sendMessage(chat_id, '>>>Visual Received!')
    if 'video' in msg:
        file_path = fursuitbot.getFile(msg['video']['file_id'])['file_path']
    else:
        file_path = fursuitbot.getFile(msg['photo'][0]['file_id'])['file_path']
    file_name = file_path.split("/")[1]
    r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    if 'video' in msg:
        SoundEffects.PlayOnDemand(file_name)
        Displays.PlayVideo(file_name)
    else:
        subprocess.call(["ffmpeg", "-loop", "1", "-i", file_name, "-c:v", "libx264", "-t", "15", "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "out.mp4"])
        Displays.PlayVideo("out.mp4")
    fursuitbot.sendMessage(chat_id, ">>>Playing.....\n\nUse 'Stop Media' to make me stop òwó")

def PlayAudioFile(fursuitbot, chat_id, msg):
    fursuitbot.sendMessage(chat_id, '>>>Audio Received!')
    if 'audio' in msg:
        file_path = fursuitbot.getFile(msg['audio']['file_id'])['file_path']
    else:
        file_path = fursuitbot.getFile(msg['voice']['file_id'])['file_path']
    file_name = file_path.split("/")[1]
    r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    SoundEffects.PlayOnDemand(file_name)
    fursuitbot.sendMessage(chat_id, ">>>Playing.....\n\nUse 'Stop Media' to make me stop òwó")

def handle(msg):
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        current_keyboard = 'Main'
        if content_type == 'text':
            if msg['text'] == '/start':
                fursuitbot.sendMessage(chat_id, 'Welcome!')
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with any song name to search and play\n\nExample: bohemian rhapsody':
                PlaySongName(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Play Song':
                fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with any song name to search and play\n\nExample: Bohemian Rhapsody')
                current_keyboard = 'none'
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)':
                TTS(fursuitbot, chat_id, msg)
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
            elif msg['text'] == 'Stop Media':
                fursuitbot.sendMessage(chat_id, '>>>OK')
                SoundEffects.StopSound()
                Displays.playingvideo = False
            elif msg['text'] == 'Set Mood':
                current_keyboard = 'Choose Mood'
            elif msg['text'] == 'Toggle Automatic Mood':
                toggleAutoMood(fursuitbot, chat_id, msg)
            elif msg['text'] in expressions:
                SetExpression(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Change Voice':
                current_keyboard = 'Choose Voice'
            elif msg['text'] in voices:
                fursuitbot.sendMessage(chat_id, '>>>Voice Set to: {}'.format(msg['text']))
                VoiceChanger.SetVoice(msg['text'])
            elif msg['text'] == '⬅️(Back to commands)':
                current_keyboard = 'Main'
        elif content_type in ['audio', 'voice']:
            PlayAudioFile(fursuitbot, chat_id, msg)
        elif content_type in ['video', 'photo']:
            PlayVideoFile(fursuitbot, chat_id, msg)
        elif content_type in ['document', 'sticker', 'video_note', 'location', 'contact', 'venue', 'game', 'poll', 'invoice', 'successful_payment', 'passport_data', 'web_page']:
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot interpret that kind of input.\nPlease forward to @MekhyW')
        if current_keyboard == 'Main':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Play Song"), KeyboardButton(text="Stop Media")], [KeyboardButton(text="Set Mood"), KeyboardButton(text="Toggle Automatic Mood")], [KeyboardButton(text="Speak"), KeyboardButton(text="Change Voice")], [KeyboardButton(text="Running time")], [KeyboardButton(text="Reboot"), KeyboardButton(text="Turn me off")]], resize_keyboard=True)
            fursuitbot.sendMessage(chat_id, '>>>Awaiting -Command- or -Audio- or -Link-', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Mood':
            keyboard = [[KeyboardButton(text="⬅️(Back to commands)")]]
            for expression in expressions:
                keyboard.append([KeyboardButton(text=expression)])
            command_keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
            fursuitbot.sendMessage(chat_id, '>>>Which mood?', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Voice':
            keyboard = [[KeyboardButton(text="⬅️(Back to commands)")]]
            for voice in voices:
                keyboard.append([KeyboardButton(text=voice)])
            command_keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
            fursuitbot.sendMessage(chat_id, '>>>What voice?', reply_markup=command_keyboard)
    except:
        if 'ConnectionResetError' not in traceback.format_exc():
            fursuitbot.sendMessage(mekhyID, traceback.format_exc())
            fursuitbot.sendMessage(mekhyID, str(msg))

def StartBot():
    MessageLoop(fursuitbot, handle).run_as_thread()