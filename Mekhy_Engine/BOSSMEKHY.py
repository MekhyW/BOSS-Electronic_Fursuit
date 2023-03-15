import TelegramBot
import VoiceChanger
import Displays
import SoundEffects
import MachineVision
import Assistant
import os
import cv2
import rospy
from std_msgs.msg import UInt16
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
    while True:
        try:
            if TelegramBot.manual_expression_mode:     
                Displays.GraphicsRefresh(convertExpressionStringToNumber(TelegramBot.ManualExpression), MachineVision.displacement_eye)
            else:
                Displays.GraphicsRefresh(convertExpressionStringToNumber(MachineVision.AutomaticExpression), MachineVision.displacement_eye)
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)

def roscore_thread():
    os.system("xterm -e 'rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200'")
    os.system("xterm -e 'rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200'")
    os.system("xterm -e 'roscore'")

def ros_thread():
    while True:
        try:
            if TelegramBot.manual_expression_mode:     
                expression_pub.publish(convertExpressionStringToNumber(TelegramBot.ManualExpression))
            else:
                expression_pub.publish(convertExpressionStringToNumber(MachineVision.AutomaticExpression))
            leds_enabled_pub.publish(TelegramBot.leds_enabled)
            actuators_enabled_pub.publish(TelegramBot.actuators_enabled)
        except Exception as e:
            print(e)
        finally:
            rospy.sleep(0.1)

def assistant_thread():
    while True:
        try:
            Assistant.refresh()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    rospy.init_node('BOSSMEKHY')
    roscore_thread = threading.Thread(target=roscore_thread)
    roscore_thread.start()
    expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
    leds_enabled_pub = rospy.Publisher('/leds_enabled', UInt16, queue_size=10)
    actuators_enabled_pub = rospy.Publisher('/actuators_enabled', UInt16, queue_size=10)
    SoundEffects.PlayBootSound()
    VoiceChanger.SetVoice("Mekhy")
    Assistant.start()
    machine_vision_thread_A = threading.Thread(target=machine_vision_thread_A)
    machine_vision_thread_B = threading.Thread(target=machine_vision_thread_B)
    display_thread = threading.Thread(target=display_thread)
    ros_thread = threading.Thread(target=ros_thread)
    assistant_thread = threading.Thread(target=assistant_thread)
    machine_vision_thread_A.start()
    machine_vision_thread_B.start()
    display_thread.start()
    ros_thread.start()
    assistant_thread.start()
    while not TelegramBot.StartBot():
        pass