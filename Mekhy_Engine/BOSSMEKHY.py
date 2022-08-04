import WiFi
import TelegramBot
import VoiceMod
import VoiceAnalyser
import Displays
import SoundEffects
import MachineVision
import os
import rospy
from std_msgs.msg import UInt16, float32

os.system("lxterminal -e roscore")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200")
os.system("lxterminal -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 _baud:=115200")
rospy.init_node('BOSSMEKHY')
expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
voice_pub = rospy.Publisher('/voice_volume', float32, queue_size=10)

if WiFi.ConnectWifi():
    TelegramBot.StartBot()

while True:
    try:
        MachineVision.calculateTargetPoint()
        Displays.GraphicsRefresh(TelegramBot.ExpressionState)
        expression_pub.publish(TelegramBot.ExpressionState)
        voice_pub.publish(VoiceAnalyser.getVolume())
    except Exception as e:
        print(e)
    finally:
        rospy.sleep(0.1)