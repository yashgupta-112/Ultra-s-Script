#!/bin/bash

if [ ! -d "$HOME/scripts" ]; then
  mkdir -p "$HOME/scripts/app_monitor"
fi



wget -P $HOME/scripts/app_monitor/ https://raw.githubusercontent.com/yashgupta-112/Support-Script/master/traffic_monitor.py
clear

croncmd="/usr/bin/python3 $HOME/scripts/traffic_monitor.py > /dev/null 2>&1"
cronjob="*/5 * * * * $croncmd"
(
    crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
    echo "$cronjob"
) | crontab -



/usr/bin/python3 $HOME/scripts/traffic_monitor.py 