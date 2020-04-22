import cec
import time
import subprocess, shlex
import os
from threading import Lock, Thread

last_routing_change_time=0
vlc_p=None
src_isdock=False

def check_tv():
    global src_isdock
    print("Waiting 2 seconds to see if the new TV source is vitadock")
    time.sleep(2)
    l = Lock()
    with l:
        if not src_isdock:
            print("It's not. Killing VLC")
            vlc(False)

def vlc(state):
    global vlc_p
    if state and not vlc_p:
        args = shlex.split('/usr/bin/vlc v4l2:///dev/video0 :v4l2-standard= :live-caching=0 :v4l2-fps=60.00')
        vlc_p=subprocess.Popen(args, env=dict(os.environ, DISPLAY=":0.0", XAUTHORITY="/home/pi/.Xauthority"))
        if vlc_p:
            print("VLC started OK")
    elif not state and vlc_p:
        #vlc_p.terminate()
        vlc_p.kill()# sometimes VLC will hang with an error message ang SIGTERM doesn't actually terminate it
        vlc_p.wait()
        vlc_p = None
        print("VLC terminated (internal)")
    else:
        os.system('pkill vlc')
        print("VLC terminated (external)")

def cb(event, *args):
    global last_routing_change_time, vlc_p, src_isdock
    
    if event == cec.EVENT_COMMAND:
        args=args[0]
        if args['opcode'] == cec.CEC_OPCODE_STANDBY:
            print("TV off, shutting VLC down")
            vlc(False)
        elif args['opcode'] == cec.CEC_OPCODE_ROUTING_CHANGE:
            print("TV changing source... waiting for activation request")
            last_routing_change_time = time.time()
            t=Thread(target=check_tv)
            src_isdock = False
            t.start()
        #else:
        #    print("Got event", event, "with data", args)
    elif event == cec.EVENT_ACTIVATED:
        if last_routing_change_time != 0 and time.time() - last_routing_change_time < 1:
            src_isdock = True
            if not vlc_p:
                print("Activation request received, starting VLC")
                vlc(True)
    #else:
    #    print("Got event", event, "with data", args)

#cec.add_callback(cb, cec.EVENT_COMMAND & cec.EVENT_ACTIVATED)
cec.add_callback(cb, cec.EVENT_ALL & ~cec.EVENT_LOG)

print("Callbacks added")
time.sleep(2)

print("Initializing CEC library")
cec.init()

# First run - get params
# Creating Device object for TV
tv = cec.Device(cec.CEC_DEVICE_TYPE_TV)
print("Current TV state: ", "on" if tv.is_on() else "off") 
print("Current Vita state: ", "connected" if os.path.exists('/dev/video0') else "not connected")


while True:
    time.sleep(10)

