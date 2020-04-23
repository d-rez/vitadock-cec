#!/usr/bin/python3
# By d-rez a.k.a. /u/dark_skeleton
# See https://github.com/d-rez/vitadock-cec

import cec
import time
from threading import Lock, Thread
from pyudev import Context, Monitor, MonitorObserver
import mpv

last_routing_change_time = 0

src_isdock = False
vita_isconnected = False
streaming = False
was_streaming_before_poweroff = False
player_object = None


def control_mpv(enable):
    global player_object, streaming
    if not player_object:
        player_object = mpv.MPV(fullscreen=True, profile="low-latency", fps=60, framedrop="no", speed=1.21, really_quiet=True)
    if enable and not streaming:
        print("Starting stream")
        player_object.play("/dev/video0")
        with Lock():
            streaming = True
    if not enable and streaming:
        print("Terminating stream")
        # player_object.terminate()
        player_object.command("stop")
        with Lock():
            streaming = False


def player_control(enable):
    # some logic here like choosing player and sending commands to it
    control_mpv(enable)

    # set CEC active to wake up / switch to TV Source
    if enable:
        cec.set_active_source()


def check_tv_source():
    global src_isdock
    time.sleep(2)
    with Lock():
        if not src_isdock:
            print("TV source changed")
            player_control(False)
        elif vita_isconnected:
            print("TV source changed to VitaDock")
            player_control(True)


def cec_callback(event, *args):
    global last_routing_change_time, src_isdock, was_streaming_before_poweroff

    if event == cec.EVENT_COMMAND:
        args = args[0]
        if args['opcode'] == cec.CEC_OPCODE_STANDBY:
            print("TV off")
            if streaming:
                was_streaming_before_poweroff = True
            player_control(False)
        elif args['opcode'] == cec.CEC_OPCODE_ROUTING_CHANGE:
            # print("TV changing source... waiting for activation request")
            last_routing_change_time = time.time()
            t = Thread(target=check_tv_source)
            src_isdock = False
            t.start()
        elif (args['opcode'] == cec.CEC_OPCODE_REPORT_PHYSICAL_ADDRESS
                and args['initiator'] == cec.CECDEVICE_TV
                and args['destination'] == cec.CECDEVICE_BROADCAST):
            # This should mean that TV has just been turned ON
            print("TV on")
            if not streaming and was_streaming_before_poweroff:
                print("Resuming previous stream")
                player_control(True)
    elif event == cec.EVENT_ACTIVATED:
        if last_routing_change_time != 0 and time.time() - last_routing_change_time < 1:
            src_isdock = True


#  setup udev
def udev_log_event(action, device):
    global vita_isconnected
    if action == "add" and device.attributes.get("name") == b"PSVita":
        with Lock():
            vita_isconnected = True
        print("Vita connected")
        player_control(True)
    if action == "remove":
        with Lock():
            vita_isconnected = False
        print("Vita disconnected")
        player_control(False)


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
print("Init: Ading CEC callbacks")
cec.add_callback(cec_callback, cec.EVENT_ALL & ~cec.EVENT_LOG)

print("Init: CEC library")
cec.init()

tv = cec.Device(cec.CEC_DEVICE_TYPE_TV)
print("Current TV state: ", "on" if tv.is_on() else "off")
print("Current Vita state: ", "connected" if vita_isconnected else "not connected")

if tv.is_on() and vita_isconnected:
    #  Assume Pi was restarted?
    player_control(True)
else:
    player_control(False)

while True:
    # loop forever
    time.sleep(10)
