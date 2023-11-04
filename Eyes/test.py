import vlc

video_path_1 = 'happy.mp4'
video_path_2 = 'happy.mp4'

vlc_instance = vlc.Instance('--no-xlib')
media_player = vlc_instance.media_player_new()

media = vlc_instance.media_new(video_path_1)
media2 = vlc_instance.media_new(video_path_2)

media_player.set_media(media)
media_player.play()
while True:
    if media_player.get_state() == vlc.State.Ended:
        media_player.set_media(media2)
        media_player.set_time(0)
        media_player.play()
        media.release()