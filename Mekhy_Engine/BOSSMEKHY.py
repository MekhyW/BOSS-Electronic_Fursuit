import WiFi
import TelegramBot
import JackClient
import VoiceAnalyser
import Displays
import SoundEffects
import MachineVision
import Leds
import os
import cv2
import rospy
from std_msgs.msg import UInt16, float32, Int8MultiArray
import threading

os.system("lxterminal -e roscore")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200")
rospy.init_node('BOSSMEKHY')
expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
voice_pub = rospy.Publisher('/voice_volume', float32, queue_size=10)
led_red_pub = rospy.Publisher('/led_red', Int8MultiArray, queue_size=10)
led_green_pub = rospy.Publisher('/led_green', Int8MultiArray, queue_size=10)
led_blue_pub = rospy.Publisher('/led_blue', Int8MultiArray, queue_size=10)

def machine_vision_thread_A():
    while True:
        try:
            MachineVision.FacemeshRecognition()
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
            Displays.GraphicsRefresh(TelegramBot.ExpressionState, MachineVision.displacement_eye)
        except Exception as e:
            print(e)
        finally:
            cv2.waitKey(1)

def leds_thread():
    while True:
        try:
            Leds.update_leds_video()
        except Exception as e:
            print(e)

def ros_thread():
    while True:
        try:
            expression_pub.publish(TelegramBot.ExpressionState)
            voice_pub.publish(VoiceAnalyser.getVolume())
            led_red_pub.publish(Leds.led_red)
            led_green_pub.publish(Leds.led_green)
            led_blue_pub.publish(Leds.led_blue)
        except Exception as e:
            print(e)
        finally:
            rospy.sleep(0.1)

SoundEffects.PlayBootSound()
JackClient.JackVoicemodRoute("Clear")
if WiFi.ConnectWifi():
    TelegramBot.StartBot()
machine_vision_thread_A = threading.Thread(target=machine_vision_thread_A)
machine_vision_thread_B = threading.Thread(target=machine_vision_thread_B)
display_thread = threading.Thread(target=display_thread)
leds_thread = threading.Thread(target=leds_thread)
ros_thread = threading.Thread(target=ros_thread)
machine_vision_thread_A.start()
machine_vision_thread_B.start()
display_thread.start()
leds_thread.start()
ros_thread.start()