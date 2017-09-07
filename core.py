import time

import logging

import settings

from settings import identifier
from settings import getSC

def sendMessage(msg,channel):
    call = getSC().api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
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
            settings.commands[word](words, ind, channel)