import sys
import spotify_token as st
import jwt
import datetime
import requests
import time
import json
from deepdiff import DeepDiff

INTERVAL = int(input("Check Interval: "))
SPOTIFY_PLAYLIST_ID = str(input("What is the Spotify Playlist ID: "))
APPLE_MUSIC_PLAYLIST_ID = ""
PLAYLIST_NAME = ""


def getSpotifyToken():
    data = st.start_session("AQAM7VaqhrmRjIQrz2enYyC0r0tK-X56eiJwU_mAbY8TlqS7D1iMWyGeEgnR2yIgWqGU6b5Du8NVEt-9joCHWhDDH-gWZjsSPYOUVte-kZPRhSuKdmbgURK6CJXUXjyf6uiTRioTNqBScjBhwRsGJqkXRn1bjcGC",
                            "db5da52b-8542-4950-beba-7e548b214b66")
    access_token = data[0]
    return access_token
SPOTIFY_ACCESS_TOKEN = getSpotifyToken()


def getAppleMusicToken():
    textfile = open("AuthKey_3CY7R3J6VR.p8", "r")

    secret = str(textfile.read())
    keyId = "3CY7R3J6VR"
    teamId = "66AVQK2TF9"
    alg = 'ES256'

    time_now = datetime.datetime.now()
    time_expired = datetime.datetime.now() + datetime.timedelta(hours=0.3)

    headers = {
        "alg": alg,
        "kid": keyId
    }

    payload = {
        "iss": teamId,
        "exp": int(time_expired.strftime("%s")),
        "iat": int(time_now.strftime("%s"))
    }

    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)
    return token
APPLE_MUSIC_ACCESS_TOKEN = getAppleMusicToken()
APPLE_SECOND_ACCESS = False


def chooseApplePlaylist():
    global APPLE_MUSIC_PLAYLIST_ID
    global PLAYLIST_NAME
    headers = {
        'Content-Type': 'application/json',
        'Music-User-Token': 'AiwFMOzjHh+6W/edDaw1b7YBv2/kodj+0Orp2sUpRCu4gml35ZRFmTfjPeNxShph5olp7GZ83OSQgwbrcWUmM9Gt8V+rZ2ZCi0KfNoVq6gNe80OfgpFtRvp2y5adEysVwEYwWQUz7Ck9Y7BmY7KorbvSz1RtkAV6DNwcCizRJMY1gdVOQaGQx1zeHMu0GiiN+PuqAa1KLFvQ1g9uQgUqUD0xvRFPgBm6+fV7fC4ZlZ5/eQjdBA==',
        'Authorization': f'Bearer {APPLE_MUSIC_ACCESS_TOKEN}',
    }
    response = requests.get(
        'https://api.music.apple.com/v1/me/library/playlists', headers=headers)
    playlists = (response.json()['data'])
    for idx, playlist in enumerate(playlists):
        print(f"{idx}: {playlist['attributes']['name']}")

    chosenPlaylistIndex = int(input("Type Index of Playlist to Convert To: "))
    chosenPlaylist = playlists[chosenPlaylistIndex]
    name = chosenPlaylist['attributes']['name']
    id = chosenPlaylist['id']
    APPLE_MUSIC_PLAYLIST_ID = f"{id}"
    PLAYLIST_NAME = name
chooseApplePlaylist()


try:
    with open(f"playlists/{PLAYLIST_NAME}|count.txt", "x") as f:
        f.write("0")
except:
    pass

try:
    with open(f"playlists/{PLAYLIST_NAME}|playlist.json", "x") as f:
        f.write("[]")
except:
    pass

def checkPlaylistCount():
    global SPOTIFY_ACCESS_TOKEN
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}',
    }

    response = requests.get(
        f'https://api.spotify.com/v1/playlists/{SPOTIFY_PLAYLIST_ID}', headers=headers)
    if response.status_code == 401:
        if response.json()['error']['message'] == "The access token expired":
            SPOTIFY_ACCESS_TOKEN = getSpotifyToken()
            return checkPlaylistCount(id)
    return response.json()['tracks']['total']


def checkIfUpdated():
    previousPlaylistCount = 0

    with open(f'playlists/{PLAYLIST_NAME}|count.txt', 'r+') as countTextFile:
        data = countTextFile.read()
        if data != "":
            previousPlaylistCount = int(data)
        countTextFile.truncate(0)
        countTextFile.seek(0)
        currentPlaylistCount = checkPlaylistCount()
        countTextFile.write(f"{currentPlaylistCount}")
        countTextFile.close()

        if currentPlaylistCount == previousPlaylistCount:
            return False
        else:
            return True


def getCurrentPlaylist():
    global SPOTIFY_ACCESS_TOKEN
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}',
    }

    response = requests.get(
        f'https://api.spotify.com/v1/playlists/{SPOTIFY_PLAYLIST_ID}', headers=headers)
    if response.status_code == 401:
        if response.json()['error']['message'] == "The access token expired":
            SPOTIFY_ACCESS_TOKEN = getSpotifyToken()
            return checkPlaylistCount(id)
    playlist = response.json()['tracks']['items']
    current = []
    for track in playlist:
        current.append(
            {"name": track['track']['name'], "addedBy": track['added_by']['id']})

    SPOTIFY_ACCESS_TOKEN = getSpotifyToken()
    
    if (response.json()['tracks']['total']) > 100:
        next_link = str(response.json()['tracks']['next'])
        for _ in range(((int(response.json()['tracks']['total'])//100))):
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}',
            }

            response = requests.get(next_link, headers=headers)
            playlist = response.json()['items']
            for track in playlist:
                current.append(
                    {"name": track['track']['name'], "addedBy": track['added_by']['id']})

            if (response.json()['next']) is not None:
                next_link = response.json()['next']
    return current


def addToAppleMusic(songName):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {APPLE_MUSIC_ACCESS_TOKEN}',
    }

    params = (
        ('term', songName.replace("feat. ", "").replace(" ", "+")),
        ('types', 'songs'),
    )
    response = requests.get(
        f'https://api.music.apple.com/v1/catalog/us/search?term={songName.replace("feat. ", "").replace(" ", "+")}&types=songs', headers=headers)
    
    id=0
    try:
        id = response.json()['results']['songs']['data'][0]['id']
    except:
        return
    

    headers = {
        'Content-Type': 'application/json',
        'Music-User-Token': 'AiwFMOzjHh+6W/edDaw1b7YBv2/kodj+0Orp2sUpRCu4gml35ZRFmTfjPeNxShph5olp7GZ83OSQgwbrcWUmM9Gt8V+rZ2ZCi0KfNoVq6gNe80OfgpFtRvp2y5adEysVwEYwWQUz7Ck9Y7BmY7KorbvSz1RtkAV6DNwcCizRJMY1gdVOQaGQx1zeHMu0GiiN+PuqAa1KLFvQ1g9uQgUqUD0xvRFPgBm6+fV7fC4ZlZ5/eQjdBA==',
        'Authorization': f'Bearer {APPLE_MUSIC_ACCESS_TOKEN}',
    }


    data = '{"data": [{"id": "' + f"{id}" + '", "type": "songs"}]}'
    time.sleep(3)
    response = requests.post(
        f'https://api.music.apple.com/v1/me/library/playlists/{APPLE_MUSIC_PLAYLIST_ID}/tracks', headers=headers, data=data)

    global APPLE_SECOND_ACCESS
    if response.status_code != 204:
        print("Error")
        if APPLE_SECOND_ACCESS:
            sys.exit(f"{response.status_code}")
        APPLE_SECOND_ACCESS = True
        addToAppleMusic(songName)
    else:
        print("Added", (songName))

def getDifference():
    # print(APPLE_MUSIC_PLAYLIST_ID)
    currentPlaylist = getCurrentPlaylist()
    previousPlaylist = []
    with open(f"playlists/{PLAYLIST_NAME}|playlist.json", 'r+') as previousPlaylistFile:
        playlist = json.load(previousPlaylistFile)
        previousPlaylist = playlist
    difference = DeepDiff(
        currentPlaylist, previousPlaylist, ignore_order=False)
    differences = (list(difference['iterable_item_removed'].values()))
    # All Differences in New not Old - Add to Playlist

    with open(f"playlists/{PLAYLIST_NAME}|playlist.json", 'r+') as previousPlaylistFile:
        previousPlaylistFile.truncate(0)
        previousPlaylistFile.seek(0)
        json.dump(currentPlaylist, previousPlaylistFile)
    
    for track in differences:
        addToAppleMusic(track['name'])

    
    # second_difference = DeepDiff(previousPlaylist, currentPlaylist, ignore_order=False)
    # second_differences = (list(second_difference['iterable_item_added'].values()))
    # All Differences in Old not New - Remove from Playlist


while True:
    if checkIfUpdated():
        print("----------------------------------------------------------------")
        getDifference()
    print("---")
    time.sleep(INTERVAL)