#!/bin/bash

printf "\033[0;31mThis script will monitor your app and restart your installated.\033[0m\n"
printf "\033[0;31mDisclaimer: This installer is unofficial and Ultra.cc staff will not support any issues with it.\033[0m\n"
read -rp "Type confirm if you wish to continue: " input
if [ ! "$input" = "confirm" ]; then
    exit
fi

yes_no() {
    select choice in "Yes" "No"; do
        case ${choice} in
            Yes)
                break
            ;;
            No)
                exit 0
            ;;
            *)
                echo "Invalid option $REPLY."
            ;;
        esac
    done
    echo
}

# install function

installer() {
    if [ ! -d "$HOME/scripts/app_monitor" ]; then
        mkdir -p "$HOME/scripts/app_monitor"
    fi
    
    wget -q -P "${HOME}/scripts/app_monitor/" https://scripts.usbx.me/util/All_app_monitor/all_appmonitor.py
    wget -q -P "${HOME}/scripts/app_monitor/" https://scripts.usbx.me/util/All_app_monitor/all_torrent_client.py
    
    clear
    
    croncmd="/usr/bin/python3 $HOME/scripts/app_monitor/all_appmonitor.py > /dev/null 2>&1"
    cronjob="*/30 * * * * $croncmd"
    (
        crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
        echo "$cronjob"
    ) | crontab -
    
    croncmd1="/usr/bin/python3 $HOME/scripts/app_monitor/all_torrent_client.py > /dev/null 2>&1"
    cronjob="*/5 * * * * $croncmd1"
    (
        crontab -l 2>/dev/null | grep -v -F "$croncmd1" || :
        echo "$cronjob"
    ) | crontab -
}

uninstall() {
    rm -rf "${HOME}/scripts/app_monitor"
    crontab -l | grep -v app_monitor | crontab -
    echo "The script has been uninstalled."
    sleep 2
    clear
}

docker_installer(){
    if [ ! -d "$HOME/scripts/app_monitor" ]; then
        mkdir -p "$HOME/scripts/app_monitor"
    fi
    
    #update python packages
    "$HOME"/scripts/app_monitor/bin/pip3 install --ignore-installed --no-cache-dir pip
    "$HOME"/scripts/app_monitor/bin/pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 "$HOME"/scripts/app_monitor/bin/pip install -U
    "$HOME"/scripts/app_monitor/bin/pip install --no-cache-dir wheel --upgrade
    #install external packages
    "$HOME"/scripts/app_monitor/bin/pip3 --no-cache-dir install discord-webhook
    
    
    wget -q -P "${HOME}/scripts/app_monitor/" https://scripts.usbx.me/util/All_app_monitor/all_app_discord.py
    wget -q -P "${HOME}/scripts/app_monitor/" https://scripts.usbx.me/util/All_app_monitor/all_torrent_discord.py
    
    clear
    
    croncmd="/usr/bin/python3 $HOME/scripts/app_monitor/all_app_discord.py > /dev/null 2>&1"
    cronjob="*/30 * * * * $croncmd"
    (
        crontab -l 2>/dev/null | grep -v -F "$croncmd" || :
        echo "$cronjob"
    ) | crontab -
    
    croncmd1="/usr/bin/python3 $HOME/scripts/app_monitor/all_torrent_discord.py > /dev/null 2>&1"
    cronjob="*/5 * * * * $croncmd1"
    (
        crontab -l 2>/dev/null | grep -v -F "$croncmd1" || :
        echo "$cronjob"
    ) | crontab -
}

printf "Please choose option from below if you want notification on discord or info as a log file on your service\n"
printf "1. Store Applications status on your service at {~/script/app_monitor}\n"
printf "2. To get application status on your Discord(You need Discord Webhook for it)\n"

if [ ! -d "$HOME/scripts/app_monitor" ]; then
    if [ "$choice" = "1" ]; then
        installer
    fi
    
    if [ "$choice" = "2" ]; then
        docker_installer
    fi
    
else
    echo "The script is already installed. Do you wish to uninstall it?"
    yes_no
    uninstall
fi

exit 0
