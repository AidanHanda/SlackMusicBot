import time
from slackclient import SlackClient
from mpd import MPDClient,CommandError

#initilize mpd related things
mpdClient = MPDClient()

#Initiliaze all slack client related things
sc = None
identifier = "<@U6RMM5ZDW>"

def sendMessage(msg,channel):
    call = sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )

def poll():
    if sc.rtm_connect():
        while True:

            for m in sc.rtm_read():
                if m['type'] == 'message' and m.get("text") and identifier in m['text']:
                    interpret(m)

            time.sleep(1)


def interpret(message):

    words = message['text'].replace(identifier,'').split()

    for ind,word in enumerate(words):
        if word == "play" and len(words) > ind+1:
            play(words[ind+1][1:-1], message['channel'])
        elif word == "skip":
            skip()
        elif word == "pause":
            pause()
        elif word == "play":
            play()

def play(toPlay,channel):
    if "youtube" in toPlay:
        mpdClient.add(("yt:" + toPlay))
        sendMessage(toPlay + " added to playlist!", channel)

def skip():

    try:
        mpdClient.next()
    except:
        pass

def play():
    try:
        mpdClient.play()
    except:
        pass

def pause():
    try:
        mpdClient.pause()
    except:
        pass

def run(data):
    #Slack
    global mpdClient
    global sc
    sc = SlackClient(data["slack"]["api-key"])
    #MPD
    mpdClient.timeout = 10
    mpdClient.idletimeout = None
    hostname = data["mopidy"]["host"]
    port = data["mopidy"]["port"]
    mpdClient.connect(host=hostname, port=port)
    poll()



