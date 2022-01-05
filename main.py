from mcstatus import MinecraftServer
import threading
import getpass
import os

countries = ['','.au','.eu','.ru']
filterVersion = None
minimumPlayers = 1
logpath = f"C:\\Users\\{getpass.getuser()}\\servers.log"

if not os.path.exists(logpath): open(logpath,'w').close()
def log(text):
    print(text)
    with open(logpath,'a') as f:
        f.write(text+"\n")
        f.close()

def check(c,n,p):
    ip = f'{n}.tcp{c}.ngrok.io:{p}'
    try:
        server = MinecraftServer.lookup(ip)
        ping = round(server.ping(),1)
        status = server.status()
    except: return
    vers = status.version.name
    count = status.players.online
    sample = status.players.sample
    if sample == None: sample = []
    names = [i.name for i in sample]
    players = ', '.join(names[:3])+\
    f' ({count}/{status.players.max})'
    if (filterVersion != None and vers != \
    filterVersion) or count < minimumPlayers: return
    log(f'(IP: {ip}) (Ping: {ping}ms) (Version:'\
    f' "{vers}") (Players: {players})')
for c in countries:
    for n in range(5):
        for p in range(65535):
            for i in range(15):
                try:
                    threading.Thread(
                    target=lambda:check(c,n,p),
                    daemon=True).start()
                    break
                except:pass
