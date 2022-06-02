import TelegramBot
import VoiceMod
import Displays
import SoundEffects
import rospy
from std_msgs.msg import UInt16, String

rospy.init_node('BOSSMEKHY')
expression_pub = rospy.Publisher('/expression', UInt16, queue_size=10)
voice_pub = rospy.Publisher('/voice', String, queue_size=10)

while True:
    try:
        Displays.GraphicsRefresh(TelegramBot.ExpressionState)
        expression_pub.publish(TelegramBot.ExpressionState)
    except Exception as e:
        print(e)

