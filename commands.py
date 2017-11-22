import logging
import subprocess
import traceback

# import alsaudio
from core import command, sendMessage, sendPrivateMessage
from settings import mpdClient, hostname, port, VERSION_STRING, song_master


@command("ping")
def ping(Request):
    sendPrivateMessage(Request, "Pong!")
    
@command("play")
def play(Request, toPlay=None):
    if not toPlay:
        try:
            toPlay = Request.words[Request.ind + 1][1:-1]
        except:
            sendPrivateMessage(Request, "Maybe you meant resume?")
            return
    if "youtube" in toPlay:
        try:
            id = mpdClient.add(("yt:" + toPlay))
            all = mpdClient.playlistinfo()
            song = all[-1]
            sendMessage('"' + song['title'] + '"' + " -  added to playlist!", Request.channel)
            song_master[id] = Request.user
            keep = [b['id'] for b in all]
            for key in song_master:
                if key not in keep:
                    del song_master[key]
            print(song_master)
        except Exception as e:
            sendMessage(traceback.format_exc() + "Link: " + toPlay, Request.channel)
            mpdClient.connect(host=hostname, port=port)
            mpdClient.consume(1)


@command("skip")
def skip(Request):
    print(mpdClient.currentsong())
    try:
        if song_master.get(mpdClient.currentsong()['id']) == Request.user or True: #Enabled for now until redis is configured
            mpdClient.next()
            sendMessage("Song Skipped!", Request.channel)
        else:
            sendPrivateMessage(Request, "I don't think you're the one who requested this song!")
    except Exception as e:
        logging.error(e)


@command("pause")
def pause(Request):
    try:
        mpdClient.pause()
        sendMessage("Paused!", Request.channel)
    except Exception as e:
        logging.error(e)


@command("resume")
def resume(Request):
    try:
        mpdClient.play()
        sendMessage("Resumed!!", Request.channel)
    except Exception as e:
        logging.error(e)


@command("currentsong")
def current(Request):
    try:
        sendMessage(mpdClient.currentsong()["title"], channel=Request.channel)
    except Exception as e:
        logging.error(e)


@command("playlist")
def playlist(Request):
    try:
        songs = mpdClient.playlistinfo()
        builder = "First 5: \n"
        for count, i in enumerate(songs):
            builder += str(count+1) + ". " + i["title"] + "\n"
            if count >= 5:
                break
        sendMessage(builder, Request.channel)
    except:
        sendMessage("Oops, nothing here!", Request.channel)


@command("search")
def search(Request):
    id = subprocess.check_output('youtube-dl "ytsearch:' + ' '.join(Request.words[Request.ind:]) + '" --get-id',
                                 shell=True).decode("UTF-8").strip()
    play(Request, toPlay="https://youtube.com/watch?v=" + id)


@command("reboot")
def reboot(Request):
    sendMessage("Raising Exception!", Request.channel)
    raise Exception("quit")


@command("version")
def version(Request):
    sendMessage(VERSION_STRING, Request.channel)
