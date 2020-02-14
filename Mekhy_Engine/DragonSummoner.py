ExpressionState = 1
#Cycle expressions: 1=(😐, 😃, 🤨, ŪwŪ)
#Trigger expressions: 2=😡, 3=😒, 4=ZZZ, 5=^^, 6=><, 7=😵, 8=OwO, 9=😢, 10=qwp, 11=😍
import BOSSMEKHY
import AncientRoar
import snowboydecoder
import sys
import signal
models = sys.argv[1:]
callbacks = [lambda: ExpressionState=1, lambda: ExpressionState=2, lambda: ExpressionState=3, lambda: ExpressionState=4, lambda: ExpressionState=5, lambda: ExpressionState=6, lambda: ExpressionState=7, lambda: ExpressionState=8, lambda: ExpressionState=9, lambda: ExpressionState=10, lambda: ExpressionState=11, lambda: AncientRoar.PlaySound(1), lambda: AncientRoar.PlaySound(2), lambda:AncientRoar.PlaySound(3), lambda:AncientRoar.PlaySound(4), lambda:AncientRoar.PlaySound(5), lambda:AncientRoar.PlaySound(6), lambda:AncientRoar.PlaySound(7), lambda:AncientRoar.PlaySound(8), lambda:AncientRoar.PlaySound(9), lambda:AncientRoar.PlaySound(10)]
detector = snowboydecoder.HotwordDetector(models, sensitivity=[0.3]*len(models))
detector.start(detected_callback=callbacks, interrupt_check=BOSSMEKHY.MainLoop, sleep_time=0)
