import time
from slackclient import SlackClient
import os
import youtube_dl


#Initiliaze all slack client related things
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
identifier = "<@U6RMM5ZDW>"


def poll():
    if sc.rtm_connect():
        while True:

            for m in sc.rtm_read():
                if m['type'] == 'message' and identifier in m['text']:
                    interpret(m)

            time.sleep(1)


def interpret(message):

    words = message['text'].replace(identifier,'').split()

    for ind,word in enumerate(words):
        if word == "play" and len(words) > ind+1:
            play(words[ind+1][1:-1], message['channel'])

def play(toPlay,channel):
    print(channel)
    call = sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=toPlay + " added to queue!"
    )
    print(call)

def skip():
    pass


poll()



