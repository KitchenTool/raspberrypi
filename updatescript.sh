#!/bin/bash
##
## Cron script to periodically update script
##

git -C /home/pi/screen pull -f

pkill python3

python3 /home/pi/screen/main.py
