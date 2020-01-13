import KillerEyes
import HypnoticChords
import HawkPerception
import AncientRoar
import RainbowHeart

def MainLoop():
    HawkPerception.GazeRefresh()
    KillerEyes.GraphicsRefresh(AncientRoar.ExpressionState, HawkPerception.GazeX, HawkPerception.GazeY)
    RainbowHeart.ArduinoRefresh(AncientRoar.ExpressionState)