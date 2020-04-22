import vlc
from time import sleep

v=vlc.Instance()
m=v.media_new('v4l2:///dev/video0')
p=v.media_player_new()
p.set_media(m)
p.play()
sleep(10)
p.stop()
sleep(10)
p.play()
sleep(5)
p.stop()
del p
del v
