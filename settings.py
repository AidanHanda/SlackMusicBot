
# initilize mpd related things
from mpd import MPDClient
from slackclient import SlackClient

mpdClient = MPDClient()
hostname = None
port = None

# Initiliaze all slack client related things
sc = None
identifier = "<@U6RMM5ZDW>"
VERSION_STRING = "0.1.0"

#initiliaze youtube-dl options
ydl_opts = {"simulate":True,"quiet":True,"forceid":True}

commands = {}
# END INIT AREA
# --------------------------------------------------------------#

def init(data):
    # Slack
    global mpdClient
    global sc
    global hostname
    global port
    sc = SlackClient(data["slack"]["api-key"])

    # MPD
    mpdClient.timeout = 10
    mpdClient.idletimeout = None
    hostname = data["mopidy"]["host"]
    port = data["mopidy"]["port"]
    mpdClient.connect(host=hostname, port=port)
    mpdClient.consume(1)

def getSC():
    return sc

def getCommands():
    return commands
