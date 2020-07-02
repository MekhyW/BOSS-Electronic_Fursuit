import snowboydecoder
import sys
import signal
models = sys.argv[1:]

def passingfunc():
    pass

callbacks = [lambda: print("Key 1"), lambda: print("Key 2"), lambda: print("Key 3"), lambda: print("Key 4"), lambda: print("Key 5"), lambda: print("Key 6"), lambda: print("Key 7"), lambda: print("Key 8"), lambda: print("Key 9"), lambda: print("Key 10"), lambda: print("Key 11"), lambda: print("Key 12"), lambda: print("Key 13"), lambda: print("Key 14"), lambda: print("Key 15"), lambda: print("Key 16"), lambda: print("Key 17"), lambda: print("Key 18"), lambda: print("Key 19"), lambda: print("Key 20")]
detector = snowboydecoder.HotwordDetector(models, sensitivity=[0.5]*len(models))
detector.start(detected_callback=callbacks, interrupt_check=passingfunc, sleep_time=0)

while 1:
    pass