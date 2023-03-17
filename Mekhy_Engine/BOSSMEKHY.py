import TelegramBot
import VoiceChanger
import Displays
import SoundEffects
import MachineVision
import Assistant
import cv2
import serial, time
import threading

def convertExpressionStringToNumber(expression):
    if expression == "Neutral":
        return 0
    elif expression == "Angry":
        return 1
    elif expression == "Disgusted":
        return 2
    elif expression == "Sad":
        return 3
    elif expression == "Happy":
        return 4
    elif expression == "Scared":
        return 5
    elif expression == "Heart":
        return 6
    elif expression == "Hypnotic":
        return 7
    elif expression == "Sexy":
        return 8
    elif expression == "Demonic":
        return 9
    else:
        return 0

def machine_vision_thread_A():
    while True:
        try:
            if TelegramBot.eye_tracking_mode:
                MachineVision.FacemeshRecognition()
            else:
                MachineVision.displacement_eye = (0, 0)
                MachineVision.left_eye_closed = False
                MachineVision.right_eye_closed = False
        except Exception as e:
            print(e)

def machine_vision_thread_B():
    while True:
        try:
            MachineVision.EmotionRecognition()
        except Exception as e:
            print(e)

def display_thread():
    Displays.startThreads()
    while True:
        try:
            Displays.displacement_eye = MachineVision.displacement_eye
            if TelegramBot.manual_expression_mode:     
                Displays.GraphicsRefresh(convertExpressionStringToNumber(TelegramBot.ManualExpression))
            else:
                Displays.GraphicsRefresh(convertExpressionStringToNumber(MachineVision.AutomaticExpression))
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)

def serial_thread():
    try:
        ser_actuators = serial.Serial('/dev/ttyACM0', 9600)
        ser_leds = serial.Serial('/dev/ttyACM1', 9600)
    except Exception as e:
        print(e)
    while True:
        try:
            if TelegramBot.manual_expression_mode:
                expression = TelegramBot.ManualExpression
            else:
                expression = MachineVision.AutomaticExpression
            if not TelegramBot.actuators_enabled:
                ser_actuators.write(str.encode("99"))
            else:
                ser_actuators.write(str.encode(expression))
            if not TelegramBot.leds_enabled:
                ser_leds.write(str.encode("99"))
            else:
                ser_leds.write(str.encode(expression))
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
    machine_vision_thread_A = threading.Thread(target=machine_vision_thread_A)
    machine_vision_thread_B = threading.Thread(target=machine_vision_thread_B)
    display_thread = threading.Thread(target=display_thread)
    serial_thread = threading.Thread(target=serial_thread)
    assistant_thread = threading.Thread(target=assistant_thread)
    machine_vision_thread_A.start()
    machine_vision_thread_B.start()
    display_thread.start()
    serial_thread.start()
    assistant_thread.start()
    while not TelegramBot.StartBot():
        pass