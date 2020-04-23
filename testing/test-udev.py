#!/usr/bin/python3
# By d-rez a.k.a. /u/dark_skeleton
# See https://github.com/d-rez/vitadock-cec

from pyudev import Context, Monitor, MonitorObserver
import time

context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem='video4linux')


def print_attributes(device):
    for a in device.attributes.available_attributes:
        print("%s = %s" % (a, device.attributes.get(a)))


def log_event(action, device):
    if action == "add" and device.attributes.get("name") == b"PSVita":
        print("Connected")
    if action == "remove":
        print("Disconnected")
    # print(device)
    # print_attributes(device)


observer = MonitorObserver(monitor, log_event)
observer.start()

for device in context.list_devices(subsystem="video4linux"):
    # print(device)
    if device.attributes.get("name") == b"PSVita":
        print("Already connected before script started")


while True:
    time.sleep(1)
