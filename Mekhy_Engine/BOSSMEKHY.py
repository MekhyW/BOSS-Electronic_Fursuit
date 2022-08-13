import WiFi
import TelegramBot
import JackClient
import VoiceAnalyser
import Displays
import SoundEffects
import MachineVision
import os
import rospy
from std_msgs.msg import UInt16, float32
import threading
import math

os.system("lxterminal -e roscore")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200")
rospy.init_node('BOSSMEKHY')
expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
voice_pub = rospy.Publisher('/voice_volume', float32, queue_size=10)

def machine_vision_thread():
    while True:
        MachineVision.calculateTargetPoint()

def display_thread():
    while True:
        Displays.GraphicsRefresh(TelegramBot.ExpressionState, (MachineVision.target_point_x, MachineVision.target_point_y, MachineVision.target_point_z))

def ros_thread():
    while True:
        try:
            expression_pub.publish(TelegramBot.ExpressionState)
            voice_pub.publish(VoiceAnalyser.getVolume())
        except Exception as e:
            print(e)
        finally:
            rospy.sleep(0.1)

SoundEffects.PlayBootSound()
JackClient.JackVoicemodRoute("Clear")
if WiFi.ConnectWifi():
    TelegramBot.StartBot()
machine_vision_thread = threading.Thread(target=machine_vision_thread)
machine_vision_thread.start()
display_thread = threading.Thread(target=display_thread)
display_thread.start()
ros_thread = threading.Thread(target=ros_thread)
ros_thread.start()