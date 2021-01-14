import serial
import pyglet
ExpressionState_Local = 0  
Video_Time = 0
currenttime = 0
window = pyglet.window.Window(fullscreen=True)  
NeutralEyes = pyglet.media.load("Neutral Eyes_Left.mp4")
AggressiveEyes = pyglet.media.load("Aggressive Eyes_Left.mp4")
SleepingEyes = pyglet.media.load("Sleeping Eyes_Left.mp4")
CryingEyes = pyglet.media.load("Crying Eyes_Left.mp4")
CheerfulEyes = pyglet.media.load("Cheerful Eyes_Left.mp4")
EmbarrasedEyes = pyglet.media.load("Embarrassed Eyes_Left.mp4")
QuestionMarkEyes = pyglet.media.load("QuestionMark Eyes_Left.mp4")
ShockedEyes = pyglet.media.load("Shocked Eyes_Left.mp4")
SillyEyes = pyglet.media.load("Silly Eyes_Left.mp4")
HeartEyes = pyglet.media.load("Heart Eyes_Left.mp4")
HypnoticEyes = pyglet.media.load("Hypnotic Eyes_Left.mp4")
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
player.queue(NeutralEyes) 
player.play()

@window.event 
def on_draw():
    global Video_Time
    global currenttime 
    window.clear() 
    if player.source and player.source.video_format: 
        player.get_texture().blit(0, 0)
    if player.time > Video_Time-0.5:
        player.seek(0)
        player.play() 

def GraphicsRefresh(ExpressionState):
    global ExpressionState_Local
    global Video_Time
    if ExpressionState != ExpressionState_Local:
        if ExpressionState==0:
            player.queue(NeutralEyes)
            Video_Time = NeutralEyes.duration
        elif ExpressionState==1:
            player.queue(AggressiveEyes) 
            Video_Time = AggressiveEyes.duration
        elif ExpressionState==2:
            player.queue(SleepingEyes)
            Video_Time = SleepingEyes.duration
        elif ExpressionState==3:
            player.queue(CryingEyes)
            Video_Time = CryingEyes.duration
        elif ExpressionState==4:
            player.queue(CheerfulEyes)
            Video_Time = CheerfulEyes.duration
        elif ExpressionState==5:
            player.queue(EmbarrasedEyes)
            Video_Time = EmbarrasedEyes.duration
        elif ExpressionState==6:
            player.queue(QuestionMarkEyes)
            Video_Time = QuestionMarkEyes.duration
        elif ExpressionState==7:
            player.queue(ShockedEyes)
            Video_Time = ShockedEyes.duration
        elif ExpressionState==8:
            player.queue(SillyEyes)
            Video_Time = SillyEyes.duration
        elif ExpressionState==9:
            player.queue(HeartEyes)
            Video_Time = HeartEyes.duration
        elif ExpressionState==10:
            player.queue(HypnoticEyes)
            Video_Time = HypnoticEyes.duration
        player.next_source() 
        player.play()    
    ExpressionState_Local = ExpressionState
    pyglet.clock.tick()
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()

while True:
    try:
        JETSON = serial.Serial('/dev/ttyS0', 9600)
        break
    except:
        print("failed")

while True:
    try:
        if(JETSON == None):
            JETSON = serial.Serial('/dev/ttyS0', 9600)
        global ExpressionState
        global frametime
        global currenttime
        line = JETSON.readline.decode()
        if line:
            while JETSON.in_waiting():
                print(JETSON.readline())
            line.split("-")
            ExpressionState = int(line[0])
            currenttime = int(line[1])
            GraphicsRefresh(ExpressionState)
            player.seek(currenttime)
        else:
            GraphicsRefresh(ExpressionState)
    except:
        print("failed")
        if(not(JETSON == None)):
            JETSON.close()
            JETSON = None