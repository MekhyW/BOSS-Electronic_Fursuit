import KillerEyes
import AncientRoar
import HypnoticChords
import HawkPerception
import DragonSummoner
import RainbowHeart

def MainLoop():
    gazelog = open("gazelog.txt", "r").readlines()
    KillerEyes.GraphicsRefresh(DragonSummoner.ExpressionState, int(gazelog[0]), int(gazelog[1]))
    RainbowHeart.ArduinoRefresh(DragonSummoner.ExpressionState)