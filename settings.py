import os

import redis
# initilize mpd related things
from mpd import MPDClient
from slackclient import SlackClient

mpdClient = MPDClient()
hostname = None
port = None

# Initiliaze all slack client related things
sc = None
identifier = "<@U6RMM5ZDW>"
VERSION_STRING = "0.1.2"
slackkey = None

#initiliaze youtube-dl options
ydl_opts = {"simulate":True,"quiet":True,"forceid":True}

commands = {}
song_master = {} #Really should use redis for this

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)  # Redis
# END INIT AREA
# --------------------------------------------------------------#

def init(data):
    """
    Initializes the general state of the application
    
    :param data: The config data
    :return: 
    """
    # Slack
    global mpdClient
    global sc
    global hostname
    global port
    global slackkey
    possiblekey = os.environ.get('SLACKAPIKEY')
    slackkey = possiblekey if possiblekey else data["slack"]["api-key"]
    sc = SlackClient(slackkey)

    # MPD
    mpdClient.timeout = 10
    mpdClient.idletimeout = None
    hostname = data["mopidy"]["host"]
    port = data["mopidy"]["port"]
    mpdClient.connect(host=hostname, port=port)
    mpdClient.consume(1)
    import commands
    commands.init = 0  # Works because its initizializing all the commands into the registry

def getSC():
    """
    Get method for the slack-client instance
    :return: Slack Client instance
    """
    return sc

def getCommands():
    """
    Get method for the list of commands
    :return: List of commands
    """
    return commands

# Wrapper for all the commands to add them to the command dictionary
