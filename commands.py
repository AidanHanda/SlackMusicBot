import logging
import subprocess
import traceback

import settings
from core import sendMessage, sendPrivateMessage, addSong, getUserInfo, resumeSong
from settings import mpdClient, VERSION_STRING, song_master

def command(word):
    """
    The general command structure that is used to decorate all commands within commands.py
    :param word: The word that should be looked for to call the function when it is mentioned
    :return: 
    """
    def dec(func):
        print(word)
        settings.commands[word] = func
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return dec


@command("ping")
def ping(Request):
    """
    Allows one to test the music bot
    
    :param Request: General context of the command given
    :return: Sends a private message to the user that sent ping
    """

    sendPrivateMessage(Request, "Pong!")


@command("play")
def play(Request, toPlay=None):
    """
    Plays the song from youtube
    
    :param Request: General context of command given
    :param toPlay: Optional param that is passed if the song that is being played was found using search rather than directly
    :return: Adds the song to the mopidy queue
    """
    if not toPlay:
        try:
            toPlay = Request.words[Request.ind + 1][1:-1]
        except:
            sendPrivateMessage(Request, "Maybe you meant resume?")
            return
    if "youtube" in toPlay:
        try:
            addSong(toPlay)
            all = mpdClient.playlistinfo()
            song = all[-1]
            sendMessage('"' + song['title'] + '"' + " -  added to playlist!", Request.channel)
            settings.redis_db.set(song['id'], Request.user)
            settings.redis_db.set(Request.user, getUserInfo(Request.raw_message['user']))
        except Exception as e:
            sendMessage(traceback.format_exc() + "Link: " + toPlay, Request.channel)
            mpdClient.consume(1)


@command("skip")
def skip(Request):
    """
    Skips the current song playing
    
    :param Request: The general context of the command given
    """
    try:
        if settings.redis_db.get(
                mpdClient.currentsong()['id']).decode('utf-8') == Request.user:
            mpdClient.next()
            sendMessage("Song Skipped!", Request.channel)
        else:
            sendPrivateMessage(Request, "I don't think you're the one who requested this song! It looks like it was: " +
                               settings.redis_db.get(settings.redis_db.get(mpdClient.currentsong()['id'])))
    except Exception as e:
        sendMessage(traceback.format_exc(), Request.channel)
        logging.error(e)


@command("pause")
def pause(Request):
    """
    Pauses the song that is currently playing
    
    :param Request: The general context of the command given
    :return: 
    """

    try:
        mpdClient.pause()
        sendMessage("Paused!", Request.channel)
    except Exception as e:
        logging.error(e)


@command("resume")
def resume(Request):
    """
    Resumes the song that is currently playing
    
    :param Request: The general context of the command given
    :return: 
    """
    try:
        mpdClient.play()
        sendMessage("Resumed!!", Request.channel)
    except Exception as e:
        logging.error(e)


@command("currentsong")
def current(Request):
    """
    Sends an announcment telling the current song the current song 
    :param Request: The general context of the command given
    :return: 
    """
    try:
        currentSong = mpdClient.currentsong()
        sendMessage(currentSong["title"] +
                    "\nRequested by: " +
                    settings.redis_db.get(settings.redis_db.get(currentSong['id'])).decode("utf-8"),
                    channel=Request.channel)
    except Exception as e:

        logging.error(e)


@command("playlist")
def playlist(Request):
    """
    Sends an announcement to the channel about the next 5 songs in the queue
    :param Request: The general context of the command given
    :return: 
    """
    try:
        songs = mpdClient.playlistinfo()
        builder = "First 5: \n"
        for count, i in enumerate(songs):
            builder += str(count + 1) + ". " + i["title"] + \
                       "\nRequested by: " + (settings.redis_db.get(settings.redis_db.get(i['id']))).decode("utf-8") + "\n"
            if count >= 5:
                break
        sendMessage(builder, Request.channel)
    except:
        sendMessage("Oops, nothing here!", Request.channel)


@command("search")
def search(Request):
    """
    Uses youtube-dl to search youtube for a song given paramters
    :param Request: The general context of the command given; also in this case holds the search terms in message
    :return: 
    """
    sendPrivateMessage(Request, "Searching!")
    id = subprocess.check_output('youtube-dl "ytsearch:' + ' '.join(Request.words[Request.ind:]) + '" --get-id',
                                 shell=True).decode("UTF-8").strip()
    play(Request, toPlay="https://youtube.com/watch?v=" + id)


@command("version")
def version(Request):
    """
    Sends the version of the bot in the chat
    
    :param Request: The general context of the command given
    :return:  
    """
    sendMessage(VERSION_STRING, Request.channel)



