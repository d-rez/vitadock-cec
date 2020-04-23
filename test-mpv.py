#!/usr/bin/python3
# By d-rez a.k.a. /u/dark_skeleton
# See https://github.com/d-rez/vitadock-cec

import mpv
import time

# Simply load mpv and play the Vita stream for 10 seconds and exit
player_object = mpv.MPV(fullscreen=True, profile="low-latency", fps=60, framedrop="no", speed=1.21, really_quiet=True)
player_object.play("/dev/video0")
time.sleep(7)
player_object.play("/home/pi/my_splash.png")
time.sleep(5)
player_object.play("/dev/video0")
time.sleep(7)
player_object.command("stop")
player_object.terminate()
del player_object
