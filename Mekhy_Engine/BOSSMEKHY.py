import TelegramBot
import VoiceChanger
import Displays
import SoundEffects
import MachineVision
import Assistant
import Serial
import cv2
import time
import threading

def display_thread():
    Displays.startThreads()
    while True:
        try:
            if TelegramBot.eye_tracking_mode:
                Displays.displacement_eye = MachineVision.displacement_eye
                Displays.left_eye_closed = MachineVision.left_eye_closed
                Displays.right_eye_closed = MachineVision.right_eye_closed
            else:
                Displays.displacement_eye = (0, 0)
                Displays.left_eye_closed = False
                Displays.right_eye_closed = False
            if TelegramBot.manual_expression_mode:     
                Displays.GraphicsRefresh(Serial.convertExpressionStringToNumber(TelegramBot.ManualExpression))
            else:
                Displays.GraphicsRefresh(Serial.convertExpressionStringToNumber(MachineVision.AutomaticExpression))
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)
            Displays.ManageWindows()

def serial_thread():
    Serial.serialConnect()
    while True:
        try:
            if TelegramBot.manual_expression_mode:
                expression = Serial.convertExpressionStringToNumber(TelegramBot.ManualExpression)
            else:
                expression = Serial.convertExpressionStringToNumber(MachineVision.AutomaticExpression)
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
    MachineVision.startThreads()
    display_thread = threading.Thread(target=display_thread)
    serial_thread = threading.Thread(target=serial_thread)
    assistant_thread = threading.Thread(target=assistant_thread)
    display_thread.start()
    serial_thread.start()
    assistant_thread.start()
    while not TelegramBot.StartBot():
        pass