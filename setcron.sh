#!/bin/bash

line="0,30 6-20 * * * python /home/pi/src/garage-alarm/run.py"
(crontab -l; echo "$line") | crontab -

