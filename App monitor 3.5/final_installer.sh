#!/bin/bash

if [ ! -d "$HOME/scripts" ]; then
  mkdir -p "$HOME/scripts/app_monitor"
fi

printf "\033[0;31mDisclaimer: This Script is unofficial and Ultra.cc staff will not support any issues with it will monitor your applications and restart them if application are not running it\033[0m\n"
read -rp "Type confirm if you wish to continue: " input
if [ ! "$input" = "confirm" ]; then
  exit
fi

discord(){
wget -P {Github URl}

clear

croncmd="/usr/bin/python3 $HOME/scripts/app_monitor/Discord_Notfication_monitory.py > /dev/null 2>&1"
cronjob="*/5 * * * * $croncmd"
(
    crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
    echo "$cronjob"
) | crontab -


/usr/bin/python3 $HOME/scripts/app_monitor/Discord_Notfication_monitory.py
}

logs(){
wget -P $HOME/scripts/app_monitor/ {correct URL}

croncmd="/usr/bin/python3 $HOME/scripts/traffic_monitor.py > /dev/null 2>&1"
cronjob="*/5 * * * * $croncmd"
(
    crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
    echo "$cronjob"
) | crontab -



/usr/bin/python3 $HOME/scripts/traffic_monitor.py 
}


printf "Please choose option from below if you want notification on discord or info as a log file on your service\n"
printf "1. Store Applications status on your service at {~/script/app_monitor}\n"
printf "2. To get application status on your Discord(You need Discord Webhook for it)\n"

read -rp "Please select option 1 or 2: " choice

if [ "$choice" = "1" ]; then
  logs
fi

if [ "$choice" = "2" ]; then
  discord
fi

if [ ! "$choice" = "1" ] && [ ! "$choice" = "2" ]; then
  echo "Wrong choice"
fi