from pyudev import Context,Monitor

context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

for device in iter(monitor.poll, None):
    if device.action == 'add':
        print('{} connected'.format(device))
