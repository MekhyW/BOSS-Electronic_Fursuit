import TelegramBot
import VoiceChanger
import Displays
import SoundEffects
import Assistant
import Serial
import cv2
import time
import threading

def display_thread():
    Displays.startThreads()
    while True:
        try:
            Displays.displacement_eye = (0, 0)
            Displays.left_eye_closed = False
            Displays.right_eye_closed = False
            Displays.GraphicsRefresh(Serial.convertExpressionStringToNumber(TelegramBot.ManualExpression))
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)
            Displays.ManageWindows()

def serial_thread():
    Serial.serialConnect()
    while True:
        try:
            expression = Serial.convertExpressionStringToNumber(TelegramBot.ManualExpression)
            if not TelegramBot.actuators_enabled:
                Serial.serialSendActuators("99")
            else:
                Serial.serialSendActuators(expression)
            if not TelegramBot.leds_enabled:
                Serial.serialSendLeds("99")
            else:
                telegrambot_status = Serial.convertStatuscodeStringToNumber(TelegramBot.status_code)
                assistant_status = Serial.convertStatuscodeStringToNumber(Assistant.status_code)
                if assistant_status:
                    Serial.serialSendLeds(assistant_status)
                elif telegrambot_status:
                    Serial.serialSendLeds(telegrambot_status)
                else:
                    Serial.serialSendLeds(expression)
        except Exception as e:
            print(e)
        finally:
            time.sleep(0.1)
            
def assistant_thread():
    while True:
        try:
            Assistant.refresh()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    SoundEffects.PlayBootSound()
    VoiceChanger.SetVoice("Mekhy")
    Assistant.start()
    display_thread = threading.Thread(target=display_thread)
    serial_thread = threading.Thread(target=serial_thread)
    assistant_thread = threading.Thread(target=assistant_thread)
    display_thread.start()
    serial_thread.start()
    assistant_thread.start()
    while not TelegramBot.StartBot():
        pass