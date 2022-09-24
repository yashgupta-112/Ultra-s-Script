import os
from subprocess import check_output, check_call
import requests
from datetime import datetime
# variables
path = os.getcwd()
# threshold = 20.0 # homex/username
base_dir = '{}/scripts/traffic_monitor'.format(path)
Discord_WebHook_File = '{}/scripts/traffic_monitor/discord.txt'.format(path)
traffic_file = '{}/scripts/traffic_monitor/warning.txt'.format(path)
threshold_file = '{}/scripts/traffic_monitor/threshold.txt'.format(path)
option_file = '{}/scripts/traffic_monitor/option.txt'.format(path)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


class traffic_monitor():

    def get_traffic_percent(self):
        traffic_percent = check_output(f"app-traffic info", shell=True)
        traffic_percent = traffic_percent.decode("utf-8")
        traffic_percent = traffic_percent.split()
        traffic_percent = float(traffic_percent[18].replace("%", ""))
        return traffic_percent

    def check_traffic(self, traffic_percent, threshold):
        if traffic_percent <= threshold:
            return True
        else:
            return False

    def check_installed_torrent_client(self):
        installed_torrent_client = ['qBittorrent',
                                    'rtorrent', 'deluge', 'transmission-daemon']
        torrent_client = []
        optimize_client = []
        for i in installed_torrent_client:
            status = os.path.exists(
                "{home_dir}/.config/{i}".format(home_dir=path, i=i))
            if status:
                optimize_client.append(i)

        if 'rtorrent' in optimize_client:
            torrent_client.append('rtorrent')
        if 'deluge' in optimize_client:
            torrent_client.append('deluge')
        if 'qBittorrent' in optimize_client:
            torrent_client.append('qbittorrent')
        if 'transmission-daemon' in optimize_client:
            torrent_client.append('transmission')

        for i in torrent_client:
            os.system("app-{} stop".format(i))
        return True

    def stop_torrent_client(self, client):
        os.system("app-{} stop".format(client))

    def Discord_Notifications_Accepter(self):
        Web_Url = input("Please enter your Discord Web Hook Url Here:")
        with open(Discord_WebHook_File, '+w') as f:
            f.write(Web_Url)
        f.close()

    def Discord_WebHook_Reader(self):
        with open(Discord_WebHook_File, 'r') as f:
            return f.read()

    def Discord_notification_(self, webhook):
        data = {
            "content": '**You have hit your traffic limit** :)'}
        response = requests.post(webhook, json=data)

    def write_warning_intextfile(self, traffic_file):
        with open(traffic_file, "a") as f:
            f.write("\n\nTIME: "+current_time+"\n")
            f.write('You have hit your traffic limit')

    def create_threshold_file(self, threshold):
        with open(threshold_file, '+w') as f:
            f.write(threshold)
        f.close()

    def read_threshold_file(self):
        with open(threshold_file, 'r') as f:
            return f.read()

    def create_option_file(self, option):
        with open(option_file, '+w') as f:
            f.write(option)
        f.close()

    def read_option_file(self):
        with open(option_file, 'r') as f:
            return f.read()


traffic = traffic_monitor()
if __name__ == '__main__':
    check = os.path.exists(threshold_file)
    if check == False:
        print("Please select the desired option from below\n")
        print("1. If you need notication on discord when you hit traffic limit")
        print("2. If you need notication in text file at ~/scripts/traffic_monitor/")
        choice = input("Please enter your choice: ")
        if choice == "1":
            traffic.Discord_Notifications_Accepter()
        if choice == "2":
            pass
        threshold = input(
            "Please enter at what percentage you want a notication enter value in float value example `20.0` or `35.0`: ")
        traffic.create_threshold_file(threshold)
        option = input(
            "Want to stop torrent client if hit traffic threshold(yes/no)")
        traffic.create_option_file(option.lower())
    else:
        status = os.path.exists(Discord_WebHook_File)
        if status:
            traffic_percent = traffic.get_traffic_percent()
            thres = traffic.read_threshold_file()
            thres = float(thres)
            val = traffic.check_traffic(traffic_percent, thres)
            if val:
                webhook = traffic.Discord_WebHook_Reader()
                traffic.Discord_notification_(webhook)
                C = traffic.read_option_file()
                if C == "yes":
                    traffic.check_installed_torrent_client()
                else:
                    pass
            else:
                pass
        else:
            traffic_percent = traffic.get_traffic_percent()
            thres = traffic.read_threshold_file()
            thres = float(thres)
            val = traffic.check_traffic(traffic_percent, thres)
            if val:
                traffic.write_warning_intextfile(traffic_file)
                C = traffic.read_option_file()
                if C == "yes":
                    traffic.check_installed_torrent_client()
                else:
                    pass
