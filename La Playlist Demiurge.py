import os
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


def pause():
    input("Press the <ENTER> key to continue...")


def connectToSpotify():
    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))


def retrieveSongsFromTxtFile(file):
    songs = []
    with open(file, "r", encoding="utf-8") as playlist_links:
        for link in playlist_links:
            songs.append(link)
    return songs


def getJsonConfig():
    with open('config.json') as conf:
        config = json.load(conf)
        return config


def getToken(user_link):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(user_link, scope)
    return token


if __name__ == "__main__":

    try:
        os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:8081/"

        print("Retrieving configuration...")
        config = getJsonConfig()

        user_link = config['user_link']
        playlist_link = config['playlist_link']

        print("Fetching required token...")
        token = getToken(user_link)

        print("Retrieving songs from txt file...")
        songs = retrieveSongsFromTxtFile('./PlaylistLinks.txt')

        if token:
            print("Adding songs to playlist...")
            spotify = spotipy.Spotify(auth=token)
            spotify.trace = False
            results = spotify.user_playlist_add_tracks(user_link, playlist_link, songs)
            print("Songs have been added to playlist successfully!")
        else:
            print("Failed to fetch token!")

        pause()
    except Exception as e:
        print(e)

