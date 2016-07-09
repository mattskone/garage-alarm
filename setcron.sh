#!/bin/bash

line="*/30 4-6 * * * python /home/pi/src/garage-alarm/run.py"
(crontab -l; echo "$line") | crontab -

