import VoiceMod
import Displays
import SoundEffects
import HotwordActivator
import TelegramBot
import LEDsAndServos

while True:
    Displays.GraphicsRefresh(HotwordActivator.ExpressionState)
    LEDsAndServos.ArduinoRefresh(HotwordActivator.ExpressionState)