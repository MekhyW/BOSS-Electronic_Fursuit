ExpressionState = 1
#Cycle expressions: [0, 3]=(owo, 0w0, õwÔ, ūwū)
#Trigger expressions: 4=ÒwÓ, 5=Zzz, 6=^^, 7=><, 8=?w?, 9=;w;, 10=⊙w⊙, 11=qwp, 12=S2wS2, 13=@w@
#SOUND EFFECTS COMMANDS: howl = "Blood moon", snarl = "Hunt the prey", woof = "Woof woof", cry = "I´m gonna cry", huff = "Tongue is out", sniff = "Sniff sniff", chitter = "Slash Racc", fart = "Dragon spell", growl = "It´s Vore time"
#EXPRESSION COMMANDS: neutral = "Neutral stance", aggressive = "I Am Angwy", sleeping = "Sweet dreams", cheerful = "Good Boy", embarrassed = "Red cheeks", question mark = "I am confused", crying = "This is so sad", shocked = "Unbelievable", silly = "Dum Dummy", heart = "Love is in the air", hypnotic = "You are mine now"
import BOSSMEKHY
import AlphaRoar
import snowboydecoder
import sys
import signal
import random
models = sys.argv[1:]
def SetExpressionState(x):
    global ExpressionState
    ExpressionState = x

callbacks = [lambda: SetExpressionState(random.randint(0, 3)), lambda: SetExpressionState(4), lambda: SetExpressionState(5), lambda: SetExpressionState(6), lambda: SetExpressionState(7), lambda: SetExpressionState(8), lambda: SetExpressionState(9), lambda: SetExpressionState(10), lambda: SetExpressionState(11), lambda: SetExpressionState(12), lambda: SetExpressionState(13), lambda: AlphaRoar.PlaySound(1), lambda: AlphaRoar.PlaySound(2), lambda:AlphaRoar.PlaySound(3), lambda:AlphaRoar.PlaySound(4), lambda:AlphaRoar.PlaySound(5), lambda:AlphaRoar.PlaySound(6), lambda:AlphaRoar.PlaySound(7), lambda:AlphaRoar.PlaySound(8), lambda:AlphaRoar.PlaySound(9)]
detector = snowboydecoder.HotwordDetector(models, sensitivity=[0.3]*len(models))
detector.start(detected_callback=callbacks, interrupt_check=SetExpressionState(ExpressionState), sleep_time=0)
