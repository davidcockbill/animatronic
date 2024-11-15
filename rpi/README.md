
# Animatronic Robot

## Boot

`boot.py` is called on startup of the rpi; via systemd.

Configuration is in `/lib/systemd/system/robot.service`:

```
[Unit]
Description=Animatronic Robot
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/git/animatronic/rpi/boot.py
User=pi

[Install]
WantedBy=multi-user.target
```

Systemd commands:
```
systemctl start robot.service
systemctl enable robot.service
systemctl status robot.service
```

To check systemd logs if it does not start: 

```
journalctl -u robot.service
```

## Overheating

Temperature can be checked as follows:

```
cat /sys/class/thermal/thermal_zone0/temp
```

The Raspberry PI has an operating range up to 85C. It aparently throttles performance after this.
Image processing is CPU intensive and if we run the OpenCV face detection in a tight loop it overheats quickly.
The robot therefore seeks slowly, then switches up to a fast scan (for responsive behaviour) whilst a face is detected.