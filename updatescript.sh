#!/bin/bash
##
## Cron script to periodically update script
##

git -C /home/pi/raspberrypi pull -f

pkill python3

python3 /home/pi/raspberrypi/main.py
