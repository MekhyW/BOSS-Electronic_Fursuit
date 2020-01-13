ExpressionState = 1
#Cycle expressions: 1=(😐, 😃, 🤨, ŪwŪ)
#Trigger expressions: 2=😡, 3=😒, 4=ZZZ, 5=^^, 6=><, 7=😵, 8=OwO, 9=😢, 10=qwp, 11=😍
import BOSSMEKHY
import snowboydecoder
import sys
import signal
models = sys.argv[1:]
callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING), lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)]
detector = snowboydecoder.HotwordDetector(models, sensitivity=[0.5]*len(models))
detector.start(detected_callback=callbacks, interrupt_check=BOSSMEKHY.MainLoop, sleep_time=0)
