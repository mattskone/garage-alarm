#!/bin/bash

line="*/30 2-4 * * * python /home/pi/src/garage-alarm/run.py"
(crontab -l; echo "$line") | crontab -

