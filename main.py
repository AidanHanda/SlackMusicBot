import time
from slackclient import SlackClient
from mpd import MPDClient,CommandError
import logging

#initilize mpd related things
mpdClient = MPDClient()
hostname = None
port = None

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
    else:
        logging.critical("Could not connect to slack - exiting!")


def interpret(message):

    words = message['text'].replace(identifier,'').split()
    channel = message['channel']
    for ind, word in enumerate(words):
        if word == "play" and len(words) > ind+1:
            play(words[ind+1][1:-1], channel)
        elif word == "skip":
            skip()
        elif word == "pause":
            pause()
        elif word == "play":
            resume()
        elif word == "playlist":
            playlist(channel)
        elif word == "current":
            current(channel)
        elif word == "ping":
            ping(channel)

def ping(channel):
    sendMessage("Pong!",channel)


def play(toPlay,channel):

    if "youtube" in toPlay:
        try:
            mpdClient.add(("yt:" + toPlay))
            sendMessage(toPlay + " added to playlist!", channel)
        except Exception as e:
            sendMessage(toPlay + " added to playlist... Probably!", channel)
            logging.critical(e)
            mpdClient.connect(host=hostname, port=port)
            mpdClient.consume(1)

def skip():

    try:
        mpdClient.next()
    except Exception as e:
        logging.error(e)

def pause():
    try:
        mpdClient.pause()
    except Exception as e:
        logging.error(e)

def resume():
    try:
        mpdClient.play()
    except Exception as e:
        logging.error(e)

def current(channel):

    logging.warning(mpdClient.status())

    try:
        sendMessage(mpdClient.currentsong()["title"],channel=channel)
    except Exception as e:
        logging.error(e)

def playlist(channel):
    try:
        songs = mpdClient.playlistinfo()
        builder = "First 5: \n"
        for ind,i in enumerate(songs):
            builder += i["pos"] + ". " + i["title"] + "\n"
            if ind > 5:
                break
        sendMessage(builder,channel)
    except:
        pass


def run(data):
    #Slack
    global mpdClient
    global sc
    global hostname
    global port
    sc = SlackClient(data["slack"]["api-key"])

    #MPD
    mpdClient.timeout = 10
    mpdClient.idletimeout = None
    hostname = data["mopidy"]["host"]
    port = data["mopidy"]["port"]
    mpdClient.connect(host=hostname, port=port)
    mpdClient.consume(1)

    #Start polling
    poll()



