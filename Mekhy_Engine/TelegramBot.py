import SoundEffects
import Displays
import VoiceChanger
import requests, os, subprocess, math, time
import traceback
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import threading
import psutil
import json
Token = json.load(open('resources/credentials.json'))['fursuitbot_token']
fursuitbot = telepot.Bot(Token)
mekhyID = 780875868
start_time = time.time()
eye_tracking_mode = False
actuators_enabled = 1
leds_enabled = 0
ManualExpression = 'Neutral'
sfx = ['AWOOO', '*racc sounds* 🦝', 'Woof! Bark!', 'Sad dog', 'Hungry growl', 'huff huff 👅', '*snif snif*', 'Zzz', 'FART']
voices = ['Mekhy', 'Demon', 'Voice of Conscience', 'Baby', 'Chipmunk', 'Radio', 'No Effects', 'Mute']
expressions = ['Neutral', '😡', '😒', '😢', '😊', '😱', '😍', 'Hypno 🌈', '😏', '😈']
status_code = 'Ok'

def SFX(fursuitbot, chat_id, msg):
    if msg['text'] == 'AWOOO':
        SoundEffects.SoundEffect('howl')
    elif msg['text'] == '*racc sounds* 🦝':
        SoundEffects.SoundEffect('chitter')
    elif msg['text'] == 'Woof! Bark!':
        SoundEffects.SoundEffect('woof')
    elif msg['text'] == 'Sad dog':
        SoundEffects.SoundEffect('cry')
    elif msg['text'] == 'Hungry growl':
        SoundEffects.SoundEffect('growl')
    elif msg['text'] == 'huff huff 👅':
        SoundEffects.SoundEffect('huff')
    elif msg['text'] == '*snif snif*':
        SoundEffects.SoundEffect('sniff')
    elif msg['text'] == 'Zzz':
        SoundEffects.SoundEffect('snore')
    elif msg['text'] == 'FART':
        SoundEffects.SoundEffect('fart')
    fursuitbot.sendMessage(chat_id, '>>>Playing: {}'.format(msg['text']))

def SetExpression(fursuitbot, chat_id, msg):
    global ManualExpression
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

def toggleEyeTracking(fursuitbot, chat_id, msg):
    global eye_tracking_mode
    eye_tracking_mode = not eye_tracking_mode
    if not eye_tracking_mode:
        fursuitbot.sendMessage(chat_id, '>>>Eye Tracking Disabled (OFF)')
    else:
        fursuitbot.sendMessage(chat_id, '>>>Eye Tracking Enabled (ON)')

def toggleLEDs(fursuitbot, chat_id, msg):
    global leds_enabled
    if leds_enabled == 1:
        leds_enabled = 0
        fursuitbot.sendMessage(chat_id, '>>>LEDs Disabled (OFF)')
    else:
        leds_enabled = 1
        fursuitbot.sendMessage(chat_id, '>>>LEDs Enabled (ON)')

def toggleActuators(fursuitbot, chat_id, msg):
    global actuators_enabled
    if actuators_enabled == 1:
        actuators_enabled = 0
        fursuitbot.sendMessage(chat_id, '>>>Actuators Disabled (OFF)')
    else:
        actuators_enabled = 1
        fursuitbot.sendMessage(chat_id, '>>>Actuators Enabled (ON)')

def PlaySongName(fursuitbot, chat_id, msg):
    global status_code
    status_code = 'Processing media'
    for file in os.listdir('.'):
        if file.endswith('.wav'):
            os.remove(file)
    fursuitbot.sendMessage(chat_id, '>>>Downloading song with query "{}"...'.format(msg['text']))
    command = 'spotdl "{}" --format wav --preload --no-cache'.format(msg['text'])
    os.system(command)
    for file in os.listdir('.'):
        if file.endswith('.wav'):
            file_name = file
            break
    fursuitbot.sendMessage(chat_id, 'Done!\n>>>Playing now')
    SoundEffects.PlayOnDemand(file_name, True)

def TTS(fursuitbot, chat_id, msg):
    global status_code
    status_code = 'Processing media'
    fursuitbot.sendMessage(chat_id, '>>>Loading text-to-speech...')
    msgToSpeak = msg['text'].replace('/speak ', '')
    SoundEffects.TTS(msgToSpeak)
    fursuitbot.sendMessage(chat_id, '>>>Speaking...')

def PlayVideoFile(fursuitbot, chat_id, msg):
    global status_code
    status_code = 'Processing media'
    fursuitbot.sendMessage(chat_id, '>>>Visual Received!')
    if 'video' in msg:
        file_path = fursuitbot.getFile(msg['video']['file_id'])['file_path']
    else:
        file_path = fursuitbot.getFile(msg['photo'][0]['file_id'])['file_path']
    file_name = file_path.split("/")[1]
    r = requests.get("https://api.telegram.org/file/bot{}/{}".format(Token, file_path), allow_redirects=True)
    open(file_name, 'wb').write(r.content)
    if 'video' in msg:
        subprocess.call(["ffmpeg", "-i", file_name, "-vf", "scale=800:480", "out.mp4", "-y"])
        subprocess.call(["ffmpeg", "-i", "out.mp4", "-i", "out.mp4", "-filter_complex", "hstack=inputs=2", "outconcat.mp4", "-y"])
        try:
            SoundEffects.PlayOnDemand(file_name)
        except Exception as e:
            fursuitbot.sendMessage(chat_id, '>>>WARNING: no audio detected (will play video anyways)'.format(e))
    else:
        subprocess.call(["ffmpeg", "-loop", "1", "-i", file_name, "-c:v", "libx264", "-t", "15", "-pix_fmt", "yuv420p", "-vf", "scale=800:480", "out.mp4", "-y"])
        subprocess.call(["ffmpeg", "-i", "out.mp4", "-i", "out.mp4", "-filter_complex", "hstack=inputs=2", "outconcat.mp4", "-y"])
    try:
        os.remove("out.mp4")
        os.remove(file_name)
    except FileNotFoundError:
        pass
    Displays.PlayVideo("outconcat.mp4")
    fursuitbot.sendMessage(chat_id, ">>>Playing.....\n\nUse 'Stop Media' to make me stop òwó")

def PlayAudioFile(fursuitbot, chat_id, msg):
    global status_code
    status_code = 'Processing media'
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

def BashCommand(fursuitbot, chat_id, msg):
    try:
        result = subprocess.check_output(msg['text'], stderr=subprocess.STDOUT, shell=True)
        if len(result):
            fursuitbot.sendMessage(chat_id, result)
        else:
            fursuitbot.sendMessage(chat_id, 'ok')
    except subprocess.CalledProcessError as e:
        fursuitbot.sendMessage(chat_id, e.output)

def thread_function(msg):
    global status_code
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        status_code = 'Message received'
        print(content_type, chat_type, chat_id)
        current_keyboard = 'Main'
        if content_type == 'text':
            if msg['text'] == '/start':
                fursuitbot.sendMessage(chat_id, 'Welcome!')
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with any song name to search and play\n\nExample: Bohemian Rhapsody':
                PlaySongName(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Play Song':
                fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with any song name to search and play\n\nExample: Bohemian Rhapsody')
                current_keyboard = 'none'
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)':
                TTS(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Speak':
                fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with what you want me to speak\n(Almost any language works!)')
                current_keyboard = 'none'
            elif 'reply_to_message' in msg and msg['reply_to_message']['text'] == '>>>Reply to THIS message with the command you want me to execute':
                BashCommand(fursuitbot, chat_id, msg)
            elif msg['text'] in ['Bash Command', 'Reboot', 'Turn me off', 'Exit process']:
                if chat_id != mekhyID:
                    fursuitbot.sendMessage(chat_id, 'This command can only be used by myself!')
                elif msg['text'] == 'Bash Command':
                    fursuitbot.sendMessage(chat_id, '>>>Reply to THIS message with the command you want me to execute')
                elif msg['text'] == 'Reboot':
                    fursuitbot.sendMessage(chat_id, '>>>System Reboot initiated.....')
                    os.system("systemctl reboot -i")
                elif msg['text'] == 'Turn me off':
                    fursuitbot.sendMessage(chat_id, '>>>System Shutdown initiated.....')
                    os.system("systemctl poweroff -i")
                elif msg['text'] == 'Exit process':
                    fursuitbot.sendMessage(chat_id, '>>>Terminating process.....')
                    os._exit(0)
                current_keyboard = 'none'
            elif msg['text'] == 'Benchmark Statistics':
                answer = f"CPU Usage: {psutil.cpu_percent()}%\nRAM Usage: {psutil.virtual_memory().percent}%\nDisk Usage: {psutil.disk_usage('/').percent}%\n\n"
                s = time.time() - start_time
                if s >= 3600:
                    answer += f'Suit active for: {int(math.floor(s/3600))} Hours + {str((s - (3600 * math.floor(s/3600)))/60)[:4]} Minutes'
                else:
                    answer += f'Suit active for: {str(s/60)[:4]} Minutes'
                fursuitbot.sendMessage(chat_id, answer)
            elif msg['text'] == 'Stop Media':
                fursuitbot.sendMessage(chat_id, '>>>OK')
                SoundEffects.StopSound()
                Displays.playingvideo = False
            elif msg['text'] == 'Sound Effect':
                current_keyboard = 'Choose Sound Effect'
            elif msg['text'] == 'Set Mood':
                current_keyboard = 'Choose Mood'
            elif msg['text'] == 'Toggle Eye Tracking':
                toggleEyeTracking(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Toggle LEDs':
                toggleLEDs(fursuitbot, chat_id, msg)
            elif msg['text'] == 'Toggle Actuators':
                toggleActuators(fursuitbot, chat_id, msg)
            elif msg['text'] == "Refsheet / Sticker Pack":
                fursuitbot.sendPhoto(chat_id, open('resources/refsheet.jpg', 'rb'), caption="My Refsheet:")
                fursuitbot.sendMessage(chat_id, 'My Stickers: https://t.me/addstickers/MekhyW', disable_web_page_preview=False)
                fursuitbot.sendMessage(chat_id, 'My GitHub: https://github.com/MekhyW', disable_web_page_preview=False)
            elif msg['text'] in sfx:
                SFX(fursuitbot, chat_id, msg)
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
            #PlayVideoFile(fursuitbot, chat_id, msg)
            fursuitbot.sendMessage(chat_id, 'Video playback is currently disabled due to performance issues.')
        elif content_type in ['document', 'sticker', 'video_note', 'location', 'contact', 'venue', 'game', 'poll', 'invoice', 'successful_payment', 'passport_data', 'web_page']:
            fursuitbot.sendMessage(chat_id, 'Sorry, I still cannot interpret that kind of input.\nPlease forward to @MekhyW')
        if current_keyboard == 'Main':
            command_keyboard = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Set Mood")],
                [KeyboardButton(text="Play Song"), KeyboardButton(text="Stop Media")],  
                [KeyboardButton(text="Sound Effect"), KeyboardButton(text="Speak")],
                [KeyboardButton(text="Change Voice")],  
                [KeyboardButton(text="Toggle Actuators")],
                [KeyboardButton(text="Benchmark Statistics")],
                [KeyboardButton(text="Refsheet / Sticker Pack")],
                [KeyboardButton(text="Bash Command"), KeyboardButton(text="Exit process")],
                [KeyboardButton(text="Reboot"), KeyboardButton(text="Turn me off")]
            ], resize_keyboard=True)
            fursuitbot.sendMessage(chat_id, '>>>Awaiting -Command- or -Audio-', reply_markup=command_keyboard)
        elif current_keyboard == 'Choose Sound Effect':
            keyboard = [[KeyboardButton(text="⬅️(Back to commands)")]]
            for sound in sfx:
                keyboard.append([KeyboardButton(text=sound)])
            command_keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
            fursuitbot.sendMessage(chat_id, '>>>Which sound effect?', reply_markup=command_keyboard)
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
    except Exception as e:
        print(e)
        if 'ConnectionResetError' not in traceback.format_exc():
            fursuitbot.sendMessage(mekhyID, traceback.format_exc())
            fursuitbot.sendMessage(mekhyID, str(msg))
    finally:
        status_code = 'Ok'

def handle(msg):
    try:
        new_thread = threading.Thread(target=thread_function, args=(msg,))
        new_thread.start()
    except:
        fursuitbot.sendMessage(mekhyID, traceback.format_exc())

def StartBot():
    global bot_online
    try:
        updates = fursuitbot.getUpdates()
        if updates:
            last_update_id = updates[-1]['update_id']
            fursuitbot.getUpdates(offset=last_update_id+1)
        fursuitbot.sendMessage(mekhyID, '>>> READY! <<<')
        MessageLoop(fursuitbot, handle).run_as_thread()
        print("bot online")
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    while not StartBot():
        print("bot offline")
    while True:
        pass