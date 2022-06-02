import TelegramBot
import VoiceMod
import VoiceAnalyser
import Displays
import SoundEffects
import rospy
from std_msgs.msg import UInt16, float32

VoiceMod.StartSox()
rospy.init_node('BOSSMEKHY')
expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
voice_pub = rospy.Publisher('/voice_volume', float32, queue_size=10)

while True:
    try:
        Displays.GraphicsRefresh(TelegramBot.ExpressionState)
        expression_pub.publish(TelegramBot.ExpressionState)
        voice_pub.publish(VoiceAnalyser.getVolume())
    except Exception as e:
        print(e)
    finally:
        rospy.sleep(0.1)