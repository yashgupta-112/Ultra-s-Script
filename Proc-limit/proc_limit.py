import os 
from discord_webhook import DiscordWebhook, DiscordEmbed

## get all users###
user_path = "/etc/seedbox/user/"
users = os.listdir(user_path)


# define variable 
valid_users = []
proc_users = []
thres = 5
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/974625937863897088/bc1NpcXvtCPEud6e36bS85Z3U-PnV5ut_20AVQyYsCFK7zCiHtvu1qC95Zp-oEA4oLaj', username="Proc Limit Report")

class Proc_Limit():
    
    def get_valid_users(self,users):
        for i in users:
            valid = os.system("id -u {user} >/dev/null 2>&1".format(user=i))
            if valid == 0:
                valid_users.append(i)
        return True
    
    def user_process(self,user):
        return os.popen("ps -u {user} | wc -l".format(user=user)).read()
    
    def discord_notfication(self,user,count):
        embed = DiscordEmbed(title='Proc limit warning', color='03b2f8')
        embed.set_author(name='Gojo', icon_url='https://i.pinimg.com/474x/bf/69/79/bf697929534868e7bb5172f7affe5d8a.jpg')
        embed.set_timestamp()
        embed.add_embed_field(name="User: " + str(user), value="Number of process: " + str(count))
        webhook.add_embed(embed)
        response = webhook.execute()



proc = Proc_Limit()

if __name__ == '__main__':
    proc.get_valid_users(users)
    for i in valid_users:
        count = proc.user_process(i)
        count = int(count)
        if count > thres:
            #proc.discord_notfication(i,count)
            proc_users.append([i,count])
        else:
            pass
        
    for i in proc_users:
        print(i[0])
        print(i[1])