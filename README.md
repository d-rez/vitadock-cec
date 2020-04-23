# vitadock-cec
 Better control over when Vita should start/stop streaming when HDMI-CEC capable TV is connected. This will let Vita go to sleep mode when you switch away from VitaDock source or turn TV off (normally it gets "stuck" outputting video if you don't disconnect it and never sleeps)

## Installation
1. Install dependencies
```
sudo apt-get update && sudo apt-get install -y git python3-pip libcec-dev build-essential python3-dev
sudo pip3 install pip --upgrade && sudo pip3 install cec python-vlc pyudev python-mpv
```
2. Fetch the repo
```
git clone https://github.com/d-rez/vitadock-cec.git /home/pi/vitadock-cec
```

3. Disable current implementation of device detection (udev)
```
sudo rm /etc/udev/rules.d/91-vita.rules /etc/udev/rules.d/92-dvita.rules
sudo rm /etc/systemd/user/vita.service
sudo udevadm control --reload-rules
sudo systemctl daemon-reload
```

4. Replace ffmpeg and mpv builds with re-compiled ones that support python module required by this script
```
sudo dpkg -i packages/ffmpeg_4.0.2-1_armhf.deb
sudo dpkg -i packages/mpv_0.29.0-1_armhf.deb
```

4. Install to start on boot and start the script
```
(crontab -l 2>/dev/null; echo "@reboot python3 /home/pi/vitadock-cec/vitadock-cec.py") | crontab -
python3 /home/pi/vitadock-cec/vitadock-cec.py&
```

## Logs
By default the script will log its debug messages to `/home/pi/vitadock-cec/vitadock-cec.log`

## Configuration and notes
\# TODO
For now it only supports MPV. I started developing a framework for VLC as well but imo VLC starts too slow, MPV is much superior in this regard (and imo nobody needs a full GUI that boots 3 minutes longer)

If there's a need for VLC version, I may consider it someday based on feedback and interest
