# vitadock-cec
 Better control over when Vita should start/stop streaming when HDMI-CEC capable TV is connected. This will let Vita go to sleep mode when you switch away from VitaDock source or turn TV off (normally it gets "stuck" outputting video if you don't disconnect it and never sleeps)

## Installation
1. Install dependencies
```
    sudo apt-get update && sudo apt-get install -y git python3-pip cec-utils
    sudo pip3 install cec python-vlc pyudev
```
2. Fetch the repo
```
    git clone https://github.com/d-rez/vitadock-cec.git /home/pi/vitadock-cec
```

3. Install to start on boot and start the script
```
(crontab -l 2>/dev/null; echo "@reboot python3 /home/pi/vitadock-cec/vitadock-cec.py") | crontab -
python3 /home/pi/vitadock-cec/vitadock-cec.py&
```

## Logs
By default the script will log its debug messages to `/home/pi/vitadock-cec/vitadock-cec.log`

## Configuration and notes
\# TODO
For now it only supports MPV. I started developing a framework for VLC as well but imo VLC starts too slow, MPV is much superior in this regard (and nobody needs a full GUI that boots 2 minutes longer)
