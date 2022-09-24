#!/bin/bash

printf "\033[0;31mThis script will monitor your traffic and stop torrent clients if traffic limit set by you is reached it will help you to save your traffic.\033[0m\n"
printf "\033[0;31mDisclaimer: This installer is unofficial and Ultra.cc staff will not support any issues with it.\033[0m\n"
read -rp "Type confirm if you wish to continue: " input
if [ ! "$input" = "confirm" ]; then
  exit
fi

printf "Select 1 to install the script\n"
printf "Select 2 to uninstall the script\n"

read -rp "Please select option 1 or 2: " choice

# Installer function

installer(){

if [ ! -d "$HOME/scripts/traffic_monitor" ]; then
  mkdir -p "$HOME/scripts/traffic_monitor"
fi

wget -P $HOME/scripts/traffic_monitor/ https://raw.githubusercontent.com/yashgupta-112/Ultra-Script/master/Traffic%20monitor/Traffic_monitor.py

clear

croncmd="/usr/bin/python3 $HOME/scripts/traffic_monitor/Traffic_monitor.py > /dev/null 2>&1"
cronjob="*/$1 * * * * $croncmd"
(
    crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
    echo "$cronjob"
) | crontab -


/usr/bin/python3 $HOME/scripts/traffic_monitor/Traffic_monitor.py
}

#uninstall function

uninstall(){
    rm -rf $HOME/scripts/traffic_monitor
    crontab -l | grep -v traffic_monitor | crontab -
    echo "Your script has been uninstalled completely."
    sleep 2
    clear
}

if [ "$choice" = "1" ]; then
read -rp "Please enter how frequent you want script to check your traffic in mins example if you want to run it in every 5 mins just write 5 and press enter: " time
installer $time
fi

if [ "$choice" = "2" ]; then
uninstall
fi

if [ ! "$choice" = "1" ] && [ ! "$choice" = "2" ]; then
  echo "Wrong choice"
fi