import SoundEffects
import snowboydecoder
import signal
ExpressionState = 1
#Expressions: 0=owo, 1=Ò-Ó, 2=Zzz, 3=^^, 4=><, 5=?w?, 6=;w;, 7=⊙w⊙, 8=qwp, 9=S2wS2, 10=@w@
#SOUND EFFECTS COMMANDS: howl = "Blood moon", snarl = "Hunt the prey", woof = "Woof woof", cry = "I´m gonna cry", huff = "Tongue is out", sniff = "Sniff sniff", chitter = "Slash Racc", fart = "Dragon spell", growl = "It´s Vore time"
#EXPRESSION COMMANDS: neutral = "Neutral stance", aggressive = "I Am Angwy", sleeping = "Sweet dreams", cheerful = "Good Boy", embarrassed = "Red cheeks", question mark = "I am confused", crying = "This is so sad", shocked = "Unbelievable", silly = "Dum Dummy", heart = "Love is in the air", hypnotic = "You are mine now"

def passingfunc():
    pass

def SetExpressionState(x):
    global ExpressionState
    ExpressionState = x

def StartDetector(arguments):
    models = arguments
    callbacks = [lambda: SetExpressionState(0), lambda: SetExpressionState(1), lambda: SetExpressionState(2), lambda: SetExpressionState(3), lambda: SetExpressionState(4), lambda: SetExpressionState(5), lambda: SetExpressionState(6), lambda: SetExpressionState(7), lambda: SetExpressionState(8), lambda: SetExpressionState(9), lambda: SetExpressionState(10), lambda: SoundEffects.PlaySound(1), lambda: SoundEffects.PlaySound(2), lambda:SoundEffects.PlaySound(3), lambda:SoundEffects.PlaySound(4), lambda:SoundEffects.PlaySound(5), lambda:SoundEffects.PlaySound(6), lambda:SoundEffects.PlaySound(7), lambda:SoundEffects.PlaySound(8), lambda:SoundEffects.PlaySound(9)]
    detector = snowboydecoder.HotwordDetector(models, sensitivity=[0.5]*len(models))
    detector.start(detected_callback=callbacks, interrupt_check=passingfunc, sleep_time=0)