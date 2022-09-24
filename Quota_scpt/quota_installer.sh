#!/bin/bash

printf "\033[0;31mThis script will monitor your Disk Quota and stop torrent clients if disk quota is hit.\033[0m\n"
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

#create virtual env
if [ ! -d "$HOME/scripts/quota_check" ]; then
   mkdir -p "$HOME/scripts/quota_check"
  /usr/bin/python3 -m venv "$HOME/scripts/quota_check"
fi

#update python packages
"$HOME"/scripts/quota_check/bin/pip3 install --ignore-installed --no-cache-dir pip
"$HOME"/scripts/quota_check/bin/pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 "$HOME"/scripts/quota_check/bin/pip install -U
"$HOME"/scripts/quota_check/bin/pip install --no-cache-dir wheel --upgrade
#install external packages
"$HOME"/scripts/quota_check/bin/pip3 --no-cache-dir install requests
"$HOME"/scripts/quota_check/bin/pip3 --no-cache-dir install configparser



wget -P $HOME/scripts/quota_check/  https://scripts.usbx.me/util/quota_check/quota_check.py


clear

croncmd="$HOME/scripts/quota_check/bin/python3 $HOME/scripts/quota_check/quota_check.py > /dev/null 2>&1"
cronjob="*/1 * * * * $croncmd"
(
    crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
    echo "$cronjob"
) | crontab -



}

#uninstall function

uninstall(){
    rm -rf $HOME/scripts/quota_check
    crontab -l | grep -v quota_check | crontab -
    echo "Your script has been uninstalled completely."
    sleep 2
    clear
}



if [ "$choice" = "1" ]; then
read -rp "Please enter how frequent you want script to check your traffic in mins example if you want to run it in every 5 mins just write 5 and press enter: " time
installer 
fi

if [ "$choice" = "2" ]; then
uninstall
fi

if [ ! "$choice" = "1" ] && [ ! "$choice" = "2" ] then
  echo "Wrong choice"
fi