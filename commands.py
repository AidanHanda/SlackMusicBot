import logging
import subprocess

from core import command, sendMessage
from settings import mpdClient, hostname, port

@command("ping")
def ping(words, ind, channel):
    sendMessage("Pong!", channel)


@command("play")
def play(words, ind, channel, toPlay=None):
    if not toPlay:
        toPlay = words[ind + 1][1:-1]
    if "youtube" in toPlay:
        try:
            print(mpdClient.add(("yt:" + toPlay)))
            sendMessage(toPlay + " added to playlist!", channel)
        except Exception as e:
            sendMessage(str(e), channel)
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

@command("reboot")
def reboot(words, ind, channel):
    sendMessage("Raising Exception!", channel)
    raise Exception("quit")
