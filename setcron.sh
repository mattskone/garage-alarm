#!/bin/bash

line="*/30 2-6 * * * python /home/pi/src/garage_alarm/run.py"
(crontab -l; echo "$line") | crontab -

