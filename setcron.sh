#!/bin/bash

line="*/30 0-4,15-23 * * * python /home/pi/src/garage-alarm/run.py"
(crontab -l; echo "$line") | crontab -

