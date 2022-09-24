import os
import time
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
"""
Data and time to store restart time of application
"""

now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
"""
Variable for location log files
"""
work_dir = os.getcwd()
log_file = '{}/scripts/app_monitor/apps_log.log'.format(work_dir)
torrent_client_list = ['deluge', 'transmission', 'qbittorrent', 'rtorrent']
apps_path = work_dir + '/.apps'
config_path = work_dir + '/bin'
systemd_path = work_dir + '/.config/systemd/user/'
Discord_WebHook_File = '{}/scripts/app_monitor/discord.txt'.format(work_dir)

"""
List of apps installed on user's service
"""

docker_app = []
torrent_client = []
mysql_apps = []
arr_apps = []
second_verify_app = []


"""
List of all application provide by us
"""
all_apps = ['airsonic', 'couchpotato', 'jackett', 'medusa', 'ombi', 'pydio', 'radarr', 'resilio', 'transmission', 'deluge',
            'jdownloader2','mylar3','pyload', 'rapidleech', 'rtorrent', 'ubooquity', 'autodl', 'deluge',
            'jellyfin', 'nextcloud', 'overseerr', 'sonarr', 'znc', 'bazarr', 'emby', 'lazylibrarian', 'plex', 'rapidleech',
            'sabnzbd', 'syncthing', 'btsync', 'filebot', 'lidarr', 'nzbget', 'readarr', 'sickbeard', 'tautulli',
            'filebrowser', 'mariadb', 'nzbhydra2', 'prowlarr', 'qbittorrent', 'requestrr', 'sickchill', ]

sql_apps = ['mariadb', 'filebrowser', 'nextcloud', 'thelounge']

second_instance = ['radarr2', 'sonarr2', 'lidarr2', 'prowlarr2',
                   'whisparr2', 'bazarr2', 'readarr2', 'autobrr', 'navidrome']

second_instance_service = ['autobrr.service', 'navidrome.service', 'prowlarr.service', 'rclone-vfs.service', 'xteve.service',
                           'lidarr.service', 'radarr.service','bazarr.service', 'whisparr.service', 'sonarr.service', 'rclone-normal.service', 'mergerfs.service', 'proftpd.service']

arr_apps_list = ['readarr', 'prowlarr', 'radarr', 'sonarr', 'bazarr', 'lidarr']

"""
Class app_monitor is decalared below with all its functions
"""


class app_monitor():
    
    """
    Discord related functions
    
    """
    
    def discord_notfication(self,webhook,appname,status,color,fail=False):
        webhook = DiscordWebhook(url=webhook, username="App monitor")
        embed = DiscordEmbed(title='Application Name - Status',description="Talk about what app monitor did restart or upgrade the app and mention if it failed", color=color)
        embed.set_author(name='OptimusPrime', icon_url='https://i.pinimg.com/564x/2c/b7/c1/2cb7c1890090030f4b59c12f4b3880f5--optimus-prime-wallpaper-transformers-prime-optimus.jpg')
        embed.set_timestamp()
        embed.add_embed_field(name="Application Name:", value=appname)
        embed.add_embed_field(name="Application Status:", value=status,inline=False)
        if fail:
            embed.add_embed_field(name="Script unable to restart application {}".format(appname), value="https://my.ultraseedbox.com/supporttickets.php",inline=False)
        webhook.add_embed(embed)
        response = webhook.execute()
    
    def Discord_Notifications_Accepter(self):
        Web_Url = input("Please enter your Discord Web Hook Url Here:")
        with open(Discord_WebHook_File, '+w') as f:
            f.write(Web_Url)
        f.close()

    def Discord_WebHook_Reader(self):
        with open(Discord_WebHook_File, 'r') as f:
            return f.read()

    """
    SystemD verification and monitor
    """

    def system_check(self, apps):
        status1 = os.popen("systemctl --user status | grep 'State:'").read()
        status1 = status1.split(":")[1].replace(' ', '').replace("\n","")
        if status1 == "running":
            pass
        else:
            os.system("systemctl --user reset-failed")
        if apps in second_verify_app:
            status = os.popen(
                "systemctl --user is-failed {}.service".format(apps)).read()
            staus = status.replace("\n", "")
            if staus == "inactive":
                return False
            if staus == "active":
                return True
            else:
                pass

    def systemD_verify_list(self):
        second_arr_apps = []
        all_systemd_files = os.listdir(systemd_path)
        for i in all_systemd_files:
            second_verify_app.append(i.split(".")[0])

    def system_monitor(self):
        all_systemd_files = os.listdir(systemd_path)
        for i in all_systemd_files:
            if i in second_instance_service:
                status = os.popen(
                    "systemctl --user is-failed {}".format(i)).read()
                staus = status.replace("\n", "")
                if staus == "inactive":
                    os.system("systemctl --user restart {}".format(i))
                if staus == "active":
                    pass
            else:
                pass

    """
    ##################################################################
    #These below given function will get all apps intalled on service#
    ##################################################################
    """

    def get_docker_apps(self, path):
        docker_app = []
        special_app = []
        remove_apps = ['backup', 'nginx']
        all_apps = os.listdir(path)
        installed_apps = list(set(all_apps).difference(remove_apps))
        docker_app = list(set(all_apps).intersection(installed_apps))
        for s in sql_apps:
            if s in docker_app:
                docker_app.remove(s)
            else:
                pass
        for j in second_instance:
            if j in docker_app:
                docker_app.remove(j)
            else:
                pass
        for w in arr_apps_list:
            if w in docker_app:
                docker_app.remove(w)
            else:
                pass
        if "wireguard" in all_apps:
            docker_app.remove("wireguard")
        if "overseerr" in all_apps:
            docker_app.remove("overseerr")
            special_app.append("overseerr")
        if "jdownloader2" in all_apps:
            docker_app.remove("jdownloader2")
            special_app.append("jdownloader2")
        if "syncthing" in all_apps:
            docker_app.remove("syncthing")
            special_app.append("syncthing")
        if "resilio" in all_apps:
            docker_app.remove("resilio")
            special_app.append("resilio")
        return docker_app,special_app

    def sql_based_apps(self, path):
        remove_apps = ['backup', 'nginx']
        all_apps = os.listdir(path)
        installed_apps = list(set(all_apps).difference(remove_apps))
        for i in sql_apps:
            if i in installed_apps:
                mysql_apps.append(i)

    def get_torrent_clients(self, path):
        remove_config = ['systemd']
        all_configs = os.listdir(path)
        all_torrent_clients = list(set(all_configs).difference(remove_config))
        if "rtorrent" in all_torrent_clients:
            torrent_client.append('rtorrent')
        if "deluge" in all_torrent_clients:
            torrent_client.append('deluge')
        if "qbittorrent-nox" in all_torrent_clients:
            torrent_client.append('qbittorrent')
        if "transmission-daemon" in all_torrent_clients:
            torrent_client.append('transmission')

    def get_arr_apps(self, path):
        remove_apps = ['backup', 'nginx']
        all_apps = os.listdir(path)
        installed_apps = list(set(all_apps).difference(remove_apps))
        for i in arr_apps_list:
            if i in installed_apps:
                arr_apps.append(i)

    """
    
    ############################################
    #Below given function will monitor the apps#
    ############################################
    
    """

    def Monitor_Webserver(self):
        status = os.popen("ps aux | grep -i nginx |grep -v grep")
        count = len(status.readlines())
        if count <= 0:
            os.system("app-nginx restart")

    def dockerized_app(self, apps,webhook):
        for i in apps:
            status = os.popen("ps aux | grep -i {}| grep -v grep".format(i)).read()
            count = len(status.splitlines())
            if count == 0:
                os.system("app-{} upgrade".format(i))
                self.discord_notfication(webhook,i,"App Restarted","50C878")
                time.sleep(120)
                status = os.popen(
                    "ps aux | grep -i {} | grep -v grep".format(i)).read()
                count = len(status.splitlines())
                if count == 0:
                    os.system("app-{} upgrade".format(i))
                    self.discord_notfication(webhook,i,"App Restarted 2nd attempt","50C878")
                    time.sleep(60)
                    status = os.popen("ps aux | grep -i {} | grep -v grep".format(i)).read()
                    count = len(status.splitlines())
                    if count <= 0:
                        self.discord_notfication(webhook,i,"Failed","C70039",True)
                else:
                    pass            
            else:
                pass


        for i in apps:
            status = os.popen("ps aux | grep -i {}".format(i)).read()
            count = len(status.splitlines())
            if count <= 2:
                os.system("app-{} restart".format(i))
                self.discord_notfication(webhook,i,"App Restarted","50C878")
            else:
                pass
            time.sleep(2)
            status = os.popen("ps aux | grep -i {}".format(i)).read()
            count = len(status.splitlines())
            if count <= 2:
                os.system("app-{} repair".format(i))
                with open(log_file, "a") as f:
                    f.write("\nTIME: "+current_time+"\n")
                    f.write('{} was down and has been repair'.format(i) + "\n")
                    os.system("clear")
            time.sleep(2)
            status = os.popen("ps aux | grep -i {}".format(i)).read()
            count = len(status.splitlines())
            if count <= 2:
                with open(log_file, "a") as f:
                    f.write(
                        "\nScript is unable to FIX your {} so please open a support ticket from here - https://my.ultraseedbox.com/submitticket.php\n".format(i))

    def sql_app_monitor(self, apps,webhook):
        for i in apps:
            if i == "nextlcoud":
                status = os.popen("ps aux | grep -i '/usr/local/bin/supercronic /etc/crontabs/abc' | grep -v grep".format(i)).read()
                count = len(status.splitlines())    
            else:
                status = os.popen("ps aux | grep -i {} | grep -v grep".format(i)).read()
                count = len(status.splitlines())
            if count <= 0:
                os.system("app-{} restart".format(i))
                self.discord_notfication(webhook,i,"App Restarted","50C878")

                time.sleep(30)
                if i == "nextlcoud":
                    status = os.popen("ps aux | grep -i '/usr/local/bin/supercronic /etc/crontabs/abc' | grep -v grep".format(i)).read()
                    count = len(status.splitlines())    
                else:
                    status = os.popen("ps aux | grep -i {} | grep -v grep".format(i)).read()
                    count = len(status.splitlines())
                if count <= 0:
                    with open(log_file, "a") as f:
                        self.discord_notfication(webhook,i,"Failed","C70039",True)

            else:
                pass

    def monitor_arr_apps(self,webhook):
        all_systemd_files = os.listdir(systemd_path)
        for i in arr_apps:
            status = os.popen(
                "ps aux | grep -i {}| grep -v grep".format(i)).read()
            count = len(status.splitlines())
            checker = self.system_check(i)
            if checker:
                thres = 1
            else:
                thres = 0
            if count <= thres:
                os.system("app-{} upgrade".format(i))
                print("{} app upgrade".format(i))
                self.discord_notfication(webhook,i,"App Restarted","50C878")
                time.sleep(180)
                status = os.popen(
                    "ps aux | grep -i {} | grep -v grep".format(i)).read()
                count = len(status.splitlines())
                if count <= thres:
                    os.system("app-{} upgrade".format(i))
                    self.discord_notfication(webhook,i,"App Restarted 2nd attempt","50C878")
                    time.sleep(50)
                    status = os.popen("ps aux | grep -i {} | grep -v grep".format(i)).read()
                    count = len(status.splitlines())
                    if count <= thres:
                        self.discord_notfication(webhook,i,"Failed","C70039",True)
                else:
                    pass
            else:
                pass

    """
    Bazarr monitor function:
    : it have 2 process by default
    """

    def bazarr_monitor(self,webhook):
        checker = self.system_check("bazarr")
        if checker:
            thres = 2
        else:
            thres = 0
        if "bazarr" in arr_apps:
            all_systemd_files = os.listdir(systemd_path)
            if "bazarr.service" in all_systemd_files:
                status = os.popen(
                    "ps aux | grep -i bazarr| grep -v grep").read()
                count = len(status.splitlines())
                if count <= thres:
                    os.system("app-bazarr upgrade")
                    self.discord_notfication(webhook,"bazarr","App Restarted","50C878")
                    time.sleep(180)
                    status = os.popen(
                        "ps aux | grep -i bazarr | grep -v grep").read()
                    count = len(status.splitlines())
                    if count <= thres:
                        os.system("app-bazarr upgrade")
                        self.discord_notfication(webhook,"bazarr","App Restarted 2nd attempt","50C878")
                        time.sleep(50)
                        status = os.popen(
                        "ps aux | grep -i bazarr | grep -v grep").read()
                        count = len(status.splitlines())
                        if count <= thres:
                            self.discord_notfication(webhook,"bazarr","Failed","C70039",True)
                    else:
                        pass
                else:
                    pass
        else:
            pass
    """
    Syncthing function
    :Seprate function because it have 2 process by default
    
    """

    def monitor_syncthing(self, apps,webhook):
        if "syncthing" in apps:
            status = os.popen(
                "ps aux | grep -i syncthing | grep -v grep").read()
            count = len(status.splitlines())
            if count <= 0:
                os.system("app-syncthing upgrade")
                self.discord_notfication(webhook,"syncthing","App Restarted","50C878")
                time.sleep(180)
                status = os.popen(
                    "ps aux | grep -i syncthing | grep -v grep").read()
                count = len(status.splitlines())
                if count <= 0:
                    os.system("app-syncthing upgrade")
                    self.discord_notfication(webhook,"syncthing","App Restarted 2nd attempt","50C878")

                time.sleep(50)
                status = os.popen(
                    "ps aux | grep -i syncthing | grep -v grep").read()
                count = len(status.splitlines())
                if count <= 1:
                    self.discord_notfication(webhook,"syncthing","Failed","C70039",True)
            else:
                pass
        else:
            pass

        """
        Jdownloader2 monitor function 
        : To grep unique process of jdownloader2
        """

    def monitor_jdownloader(self, apps,webhook):
        if "jdownloader2" in apps:
            status = os.popen(
                "ps aux | grep /usr/bin/openbox | grep -v grep ").read()
            count = len(status.splitlines())
            if count == 0:
                os.system("app-jdownloader2 upgrade")
                self.discord_notfication(webhook,"jdownloader2","App Restarted","50C878")
                time.sleep(180)
                status = os.popen(
                    "ps aux | grep /usr/bin/openbox | grep -v grep ").read()
                count = len(status.splitlines())
                if count <= 0:
                    os.system("app-jdownloader2 upgrade")
                    self.discord_notfication(webhook,"jdownloader2","App Restarted 2nd attempt","50C878")
                    time.sleep(50)
                    status = os.popen(
                        "ps aux | grep /usr/bin/openbox | grep -v grep ").read()
                    count = len(status.splitlines())
                    if count <= 0:
                        self.discord_notfication(webhook,"jdownloader2","Failed","C70039",True)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def monitor_resilio(self, apps,webhook):
        if "resilio" in apps:
            status = os.popen("ps aux | grep 'rslsync --nodaemon --config /config/sync.conf' | grep -v grep ").read()
            count = len(status.splitlines())
            if count == 0:
                os.system("app-resilio upgrade")
                self.discord_notfication(webhook,"resilio","App Restarted","50C878")
                time.sleep(180)
                status = os.popen(
                    "ps aux | grep 'rslsync --nodaemon --config /config/sync.conf'| grep -v grep ").read()
                count = len(status.splitlines())
                if count <= 0:
                    os.system("app-resilio upgrade")
                    self.discord_notfication(webhook,"resilio","App Restarted 2nd attempt","50C878")
                    time.sleep(50)
                    status = os.popen(
                        "ps aux | grep 'rslsync --nodaemon --config /config/sync.conf'| grep -v grep ").read()
                    count = len(status.splitlines())
                    if count <= 0:
                        self.discord_notfication(webhook,"resilio","Failed","C70039",True)
                else:
                    pass           
            else:
                pass
        else:
            pass

    """
    Overseerr monitor function
    
    """

    def monitor_overserr(self, apps,webhook):
        if "overseerr" in apps:
            status = os.popen(
                "ps aux | grep '/usr/bin/node dist/index.js' | grep -v grep ").read()
            count = len(status.splitlines())
            if count == 0:
                os.system("app-overseerr upgrade")
                self.discord_notfication(webhook,"overseerr","App Restarted","50C878")
                time.sleep(180)
                status = os.popen(
                    "ps aux | grep '/usr/bin/node dist/index.js'| grep -v grep ").read()
                count = len(status.splitlines())
                if count <= 0:
                    os.system("app-overseerr upgrade")
                    self.discord_notfication(webhook,"overseerr","App Restarted 2nd attempt","50C878")
                    time.sleep(50)
                    status = os.popen(
                        "ps aux | grep '/usr/bin/node dist/index.js'| grep -v grep ").read()
                    count = len(status.splitlines())
                    if count <= 0:
                        self.discord_notfication(webhook,"overseerr","Failed","C70039",True)
                else:
                    pass
            else:
                pass
        else:
            pass


monitor = app_monitor()
if __name__ == '__main__':
    # check if discord wehbhook file is exist return true if yes false if no
    check = os.path.exists(Discord_WebHook_File)
    if check:
        # get discord hook
        webhook = monitor.Discord_WebHook_Reader()
        # check webserver is running or not
        monitor.Monitor_Webserver()
        # Function call will get alls systems installed on service and monitor them
        monitor.systemD_verify_list()
        monitor.system_monitor()
        # get all docker apps and insatalled apps on service
        apps ,apps2 = monitor.get_docker_apps(apps_path)
        monitor.get_arr_apps(apps_path)
        monitor.sql_based_apps(apps_path)
        # monitor torrent client
        monitor.dockerized_app(apps,webhook)
        monitor.monitor_arr_apps(webhook)
        monitor.sql_app_monitor(mysql_apps,webhook)
        monitor.monitor_overserr(apps2,webhook)
        monitor.monitor_syncthing(apps2,webhook)
        monitor.monitor_jdownloader(apps2,webhook)
        monitor.bazarr_monitor(webhook)
        monitor.monitor_resilio(apps2,webhook)
    else:
        monitor.Discord_Notifications_Accepter()