import pyautogui
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
import vlc
import os
vlc_instance = vlc.Instance('--no-xlib')
media_player = vlc_instance.media_player_new()
display_height = 480
display_width = 800
mask_neutral = vlc_instance.media_new('../Eyes/mask_neutral.mp4')
mask_sad = vlc_instance.media_new('../Eyes/mask_sad.mp4')
mask_happy = vlc_instance.media_new('../Eyes/mask_happy.mp4')
mask_scared = vlc_instance.media_new('../Eyes/mask_scared.mp4')
mask_angry = vlc_instance.media_new('../Eyes/mask_angry.mp4')
mask_disgusted = vlc_instance.media_new('../Eyes/mask_disgusted.mp4')
mask_heart = vlc_instance.media_new('../Eyes/mask_heart.mp4')
mask_hypnotic = vlc_instance.media_new('../Eyes/mask_hipnotic.mp4')
mask_sexy = vlc_instance.media_new('../Eyes/mask_sexy.mp4')
mask_demonic = vlc_instance.media_new('../Eyes/mask_demonic.mp4')
current_mask = mask_neutral
cached_expression = 99
playingvideo = False

def ManageWindows():
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(0, 0)
    screen = Wnck.Screen.get_default()
    screen.force_update()
    for window in screen.get_windows():
        window_name = window.get_name()
        window_name = window_name.lower()
        if any([x in window_name for x in ["eyes", "vlc", "VLC"]]):
            window.maximize()
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.X, 0, 0, display_width, display_height - screen.get_height())
            window.set_geometry(Wnck.WindowGravity.STATIC, Wnck.WindowMoveResizeMask.Y, 0, 0, display_width, display_height - screen.get_height())
        elif any([x in window_name for x in ["terminal", "sh", "play"]]):
            window.minimize()

def PlayVideo(file_name, remove_file=True):
    global playingvideo
    playingvideo = True
    media = vlc_instance.media_new(file_name)
    media_player.set_media(media)
    media_player.play()
    while media_player.get_state() != vlc.State.Ended:
        ManageWindows()
    media.release()
    playingvideo = False
    if remove_file:
        os.remove(file_name)

def GraphicsRefresh(expression):
    global cached_expression, current_mask, playingvideo
    ManageWindows()
    if expression != cached_expression:
        cached_expression = expression
        if cached_expression == 0:
            media_player.set_media(mask_neutral)
            current_mask = mask_neutral
        elif cached_expression == 1:
            media_player.set_media(mask_angry)
            current_mask = mask_angry
        elif cached_expression == 2:
            media_player.set_media(mask_disgusted)
            current_mask = mask_disgusted
        elif cached_expression == 3:
            media_player.set_media(mask_sad)
            current_mask = mask_sad
        elif cached_expression == 4:
            media_player.set_media(mask_happy)
            current_mask = mask_happy
        elif cached_expression == 5:
            media_player.set_media(mask_scared)
            current_mask = mask_scared
        elif cached_expression == 6:
            media_player.set_media(mask_heart)
            current_mask = mask_heart
        elif cached_expression == 7:
            media_player.set_media(mask_hypnotic)
            current_mask = mask_hypnotic
        elif cached_expression == 8:
            media_player.set_media(mask_sexy)
            current_mask = mask_sexy
        elif cached_expression == 9:
            media_player.set_media(mask_demonic)
            current_mask = mask_demonic
        media_player.set_media(current_mask)
        media_player.play()
    if not playingvideo:
        if media_player.get_state() == vlc.State.Ended:
            media_player.set_media(current_mask)
            media_player.set_time(0)
            media_player.play()

if __name__ == '__main__':
    PlayVideo('resources/small.mp4', False)
    while True:
        GraphicsRefresh(7)