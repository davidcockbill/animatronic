
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