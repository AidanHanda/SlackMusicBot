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
    """
    Sends a message in the given channel
    
    :param msg: The message to send
    :param channel: The channel to send it in
    :return: 
    """
    call = getSC().api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
    )

def sendPrivateMessage(Request, msg):
    """
    Sends a private message to the user given by request
    
    :param Request: The general context of the command given
    :param msg: The message to send
    :return: 
    """
    getSC().api_call(
        "chat.postEphemeral",
        channel=Request.channel,
        text=msg,
        user=Request.raw_message['user']
    )


def getUserInfo(userid):
    """
    Gets information about the user
    :param userid: The id of the user to get info about
    :return: 
    """
    payload = {'token': settings.slackkey, 'user': userid, 'pretty':1}
    return json.loads(requests.get('https://slack.com/api/users.info', params=payload).text).get('user').get('name')

def poll():
    """
    The keep-alive with mopidy server as well as the searcher for command words in the chat
    :return: 
    """
    if getSC().rtm_connect():
        while True:
            mpdClient.ping()
            for m in getSC().rtm_read():
                if m['type'] == 'message' and m.get("text") and identifier in m['text']:
                    print(m)
                    interpret(m)
            time.sleep(1)
    else:
        logging.critical("Could not connect to slack - exiting!")


def interpret(message):
    """
    Checks a message to see what command if any are within it
    :param message: The message to be checked for commands
    :return: 
    """
    words = message['text'].replace(identifier, '').split()
    channel = message['channel']
    for ind, word in enumerate(words):
        if word in settings.commands:
            #DEBUGGING
            logging.log(logging.ERROR, "~Recieved Command: " + word)
            _thread.start_new_thread(settings.commands[word], (Message(message, words, ind, channel),))


class Message:
    """
    General wrapper for messages
    """
    def __init__(self, raw_message, words, ind, channel):
        self.raw_message = raw_message
        self.user = raw_message['user']
        self.words = words
        self.ind = ind
        self.channel = channel

def addSong(url):
    """
    Interfaces with mopidy to add a song to the queue -- Built because the mpd library was malfunctioning
    :param url: The url of the song to be added 
    :return: 
    """
    url = str(url)
    finalurl = "yt:"+url
    print(finalurl)
    data = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params": {"uri": finalurl}}
    pprint.pprint(data)
    r = requests.post('http://localhost:6680/mopidy/rpc',data = json.dumps(data))

    print(r.json())

def resumeSong():
    data = {"jsonrpc": "2.0", "id": 1, "method": "core.playbackcontroller.play", "params": {}}
    pprint.pprint(data)
    r = requests.post('http://localhost:6680/mopidy/rpc', data=json.dumps(data))
