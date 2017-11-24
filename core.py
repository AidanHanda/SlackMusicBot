import _thread
import json
import logging
import pprint
import time

import requests

import settings
from settings import getSC
from settings import identifier
from settings import mpdClient


def sendMessage(msg,channel):
    call = getSC().api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )

def sendPrivateMessage(Request, msg):
    getSC().api_call(
        "chat.postEphemeral",
        channel=Request.channel,
        text=msg,
        user=Request.raw_message['user']
    )


# Wrapper for all the commands to add them to the command dictionary
def command(word):
    def dec(func):
        settings.commands[word] = func
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return dec


def poll():
    if getSC().rtm_connect():
        while True:
            mpdClient.ping()
            for m in getSC().rtm_read():
                if m['type'] == 'message' and m.get("text") and identifier in m['text']:
                    interpret(m)
            time.sleep(1)
    else:
        logging.critical("Could not connect to slack - exiting!")


def interpret(message):
    words = message['text'].replace(identifier, '').split()
    channel = message['channel']
    for ind, word in enumerate(words):
        if word in settings.commands:
            #DEBUGGING
            logging.log(logging.ERROR, "Recieved Command: " + word)
            _thread.start_new_thread(settings.commands[word](Message(message, words, ind, channel)))


class Message:
    def __init__(self, raw_message, words, ind, channel):
        self.raw_message = raw_message
        self.user = raw_message['user']
        self.words = words
        self.ind = ind
        self.channel = channel

def addSong(url):
    url = str(url)
    finalurl = "yt:"+url
    print(finalurl)
    data = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uri": finalurl}}
    pprint.pprint(data)
    r = requests.post('http://localhost:6680/mopidy/rpc',data = json.dumps(data))

    print(r.json())