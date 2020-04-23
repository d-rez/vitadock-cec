#!/usr/bin/python3
# By d-rez a.k.a. /u/dark_skeleton
# See https://github.com/d-rez/vitadock-cec

import cec
import time
from threading import Lock, Thread
from pyudev import Context, Monitor, MonitorObserver
# import mpv

last_routing_change_time = 0

src_isdock = False
vita_isconnected = False
tv_power = False
player_launched = False
player_object = None


def control_mpv(enable):
    global player_object, player_launched
    if enable and not player_launched:
        # player_object = mpv.MPV(fullscreen=True, profile="low-latency", fps=60, framedrop="no", speed=1.21, really_quiet=True)
        # player_object.play("/dev/video0")
        print("Would start stream")
        with Lock():
            player_launched = True
    if not enable and player_launched:
        # player_object.terminate()
        print("Would start stream")
        with Lock():
            player_launched = False


def player_control(enable):
    # some logic here like choosing player and sending commands to it
    control_mpv(enable)

    # set CEC active
    cec.set_active_source()


def check_tv_source():
    global src_isdock
    print("Waiting 2 seconds to see if the new TV source is vitadock")
    time.sleep(2)
    with Lock():
        if not src_isdock:
            player_control(False)
        elif vita_isconnected:
            player_control(True)


def cec_callback(event, *args):
    global last_routing_change_time, src_isdock

    if event == cec.EVENT_COMMAND:
        args = args[0]
        if args['opcode'] == cec.CEC_OPCODE_STANDBY:
            print("TV off")
            player_control(False)
        elif args['opcode'] == cec.CEC_OPCODE_ROUTING_CHANGE:
            print("TV changing source... waiting for activation request")
            last_routing_change_time = time.time()
            t = Thread(target=check_tv_source)
            src_isdock = False
            t.start()
        #  else:
        #    print("Got event", event, "with data", args)
    elif event == cec.EVENT_ACTIVATED:
        if last_routing_change_time != 0 and time.time() - last_routing_change_time < 1:
            src_isdock = True
            if not player_launched and vita_isconnected:
                print("Activation request received, starting stream")
                player_control(True)
    #  else:
    #    print("Got event", event, "with data", args)


def decision_dispatcher():
    """ We decide here based on multiple factors whether we want to launch stream, kill it, or do nothing """
    global vita_isconnected
    with Lock():
        pass


#  setup udev
def udev_log_event(action, device):
    global vita_isconnected
    if action == "add" and device.attributes.get("name") == b"PSVita":
        with Lock():
            vita_isconnected = True
        print("Vita connected")
    if action == "remove":
        with Lock():
            vita_isconnected = False
        print("Vita disconnected")
    # print(device)
    # print_attributes(device)
    decision_dispatcher()


udev_context = Context()
for device in udev_context.list_devices(subsystem="video4linux"):
    # print(device)
    if device.attributes.get("name") == b"PSVita":
        vita_isconnected = True
        print("Init: Vita was already connected")
udev_monitor = Monitor.from_netlink(udev_context)
udev_monitor.filter_by(subsystem='video4linux')

# start observer for udev callbacks
observer = MonitorObserver(udev_monitor, udev_log_event)
observer.start()

#  cec.add_callback(cb, cec.EVENT_COMMAND & cec.EVENT_ACTIVATED)
cec.add_callback(cec_callback, cec.EVENT_ALL & ~cec.EVENT_LOG)

print("Callbacks added")
time.sleep(2)

print("Initializing CEC library")
cec.init()

# First run - get params
# Creating Device object for TV
tv = cec.Device(cec.CEC_DEVICE_TYPE_TV)
print("Current TV state: ", "on" if tv.is_on() else "off")
print("Current Vita state: ", "connected" if vita_isconnected else "not connected")

if tv.is_on() and vita_isconnected:
    #  Assume Pi was restarted?
    player_control(True)

while True:
    time.sleep(10)
