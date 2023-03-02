import TelegramBot
import VoiceChanger
import Displays
import SoundEffects
import MachineVision
import subprocess
import cv2
import rospy
from std_msgs.msg import UInt16, Int8MultiArray
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

def ros_thread():
    while True:
        try:
            if TelegramBot.manual_expression_mode:     
                expression_pub.publish(convertExpressionStringToNumber(TelegramBot.ManualExpression))
            else:
                expression_pub.publish(convertExpressionStringToNumber(MachineVision.AutomaticExpression))
        except Exception as e:
            print(e)
        finally:
            rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        subprocess.check_output("lxterminal -e roscore", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200", stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        subprocess.check_output("gnome-terminal -e roscore", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("gnome-terminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("gnome-terminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200", stderr=subprocess.STDOUT, shell=True)
    rospy.init_node('BOSSMEKHY')
    expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
    led_red_pub = rospy.Publisher('/led_red', Int8MultiArray, queue_size=10)
    led_green_pub = rospy.Publisher('/led_green', Int8MultiArray, queue_size=10)
    led_blue_pub = rospy.Publisher('/led_blue', Int8MultiArray, queue_size=10)
    SoundEffects.PlayBootSound()
    VoiceChanger.SetVoice("Clear")
    machine_vision_thread_A = threading.Thread(target=machine_vision_thread_A)
    machine_vision_thread_B = threading.Thread(target=machine_vision_thread_B)
    display_thread = threading.Thread(target=display_thread)
    ros_thread = threading.Thread(target=ros_thread)
    machine_vision_thread_A.start()
    machine_vision_thread_B.start()
    display_thread.start()
    ros_thread.start()
    while not TelegramBot.StartBot():
        pass