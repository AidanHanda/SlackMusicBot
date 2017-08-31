import subprocess
import time
from slackclient import SlackClient
from mpd import MPDClient, CommandError
import logging

# initilize mpd related things
mpdClient = MPDClient()
hostname = None
port = None

# Initiliaze all slack client related things
sc = None
identifier = "<@U6RMM5ZDW>"


# commands
commands = {}


# END INIT AREA
# --------------------------------------------------------------#

#Send message utility used to communicate with slack
def sendMessage(msg,channel):
    call = sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )



# Wrapper for all the commands to add them to the command dictionary
def command(word):
    def dec(func):
        commands[word] = func

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return dec


@command("ping")
def ping(words, ind, channel):
    sendMessage("Pong!", channel)


@command("play")
def play(words, ind, channel, toPlay=None):
    if not toPlay:
        try:
            toPlay = words[ind + 1][1:-1]
        except:
            sendMessage("Incorrect use of play!",channel)
            return
    if "youtube" in toPlay:
        try:
            mpdClient.add(("yt:" + toPlay))
            sendMessage(toPlay + " added to playlist!", channel)
        except Exception as e:
            sendMessage(toPlay + " added to playlist... Probably!", channel)
            logging.error(e)
            mpdClient.connect(host=hostname, port=port)
            mpdClient.consume(1)


@command("skip")
def skip(words, ind, channel):
    try:
        mpdClient.next()
    except Exception as e:
        logging.error(e)


@command("pause")
def pause(words, ind, channel):
    try:
        mpdClient.pause()
    except Exception as e:
        logging.error(e)


@command("resume")
def resume(words, ind, channel):
    try:
        mpdClient.play()
    except Exception as e:
        logging.error(e)


@command("currentsong")
def current(words, ind, channel):
    logging.warning(mpdClient.status())

    try:
        sendMessage(mpdClient.currentsong()["title"], channel=channel)
    except Exception as e:
        logging.error(e)


@command("playlist")
def playlist(words, ind, channel):
    try:
        songs = mpdClient.playlistinfo()
        builder = "First 5: \n"
        for ind, i in enumerate(songs):
            builder += i["pos"] + ". " + i["title"] + "\n"
            if ind > 5:
                break
        sendMessage(builder, channel)
    except:
        sendMessage("Oops, nothing here!")

@command("search")
def search(words, ind, channel):
    id = subprocess.check_output('youtube-dl "ytsearch:' + ' '.join(words[ind:]) + '" --get-id', shell=True).decode("UTF-8").strip()
    play(words,ind,channel,toPlay="https://youtube.com/watch?v=" + id)

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
    words = message['text'].replace(identifier, '').split()
    channel = message['channel']
    for ind, word in enumerate(words):
        if word in commands:
            commands[word](words, ind, channel)


def run(data):
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

    # Start polling
    poll()
