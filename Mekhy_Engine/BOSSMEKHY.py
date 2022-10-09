import WiFi
import TelegramBot
import JackClient
import VoiceAnalyser
import Displays
import SoundEffects
import MachineVision
import Leds
import os
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

def machine_vision_thread():
    while True:
        MachineVision.FacialRecognition()

def display_thread():
    while True:
        Displays.GraphicsRefresh(TelegramBot.ExpressionState, MachineVision.left_eye_center, MachineVision.right_eye_center)

def leds_thread():
    while True:
        Leds.update_leds_video()

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
machine_vision_thread = threading.Thread(target=machine_vision_thread)
display_thread = threading.Thread(target=display_thread)
leds_thread = threading.Thread(target=leds_thread)
ros_thread = threading.Thread(target=ros_thread)
machine_vision_thread.start()
display_thread.start()
leds_thread.start()
ros_thread.start()