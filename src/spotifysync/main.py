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
    data = st.start_session("##",
                            "##")
    access_token = data[0]
    return access_token


SPOTIFY_ACCESS_TOKEN = getSpotifyToken()


def getAppleMusicToken():
    textfile = open("AUTHKEYFILE", "r")

    secret = str(textfile.read())
    keyId = "###"
    teamId = "###"
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
    print(APPLE_MUSIC_ACCESS_TOKEN)
    headers = {
        'Content-Type': 'application/json',
        'Music-User-Token': 'APPLEMUSICMUSICUSERTOKEN',
        'Authorization': f'Bearer {APPLE_MUSIC_ACCESS_TOKEN}',
    }
    response = requests.get(
        'https://api.music.apple.com/v1/me/library/playlists', headers=headers)
    print(response.json())
    sys.exit()
    playlists = (response.json()['data'])
    for idx, playlist in enumerate(playlists):
        print(f"{idx}: {playlist['attributes']['name']}")
    print(f'{len(playlists)+1}. New Playlist*')

    chosenPlaylistIndex = int(input("Type Index of Playlist to Convert To: "))
    if chosenPlaylistIndex == len(playlists)+1:
        pn = str(input("\nPlaylist Name: "))
        headers = {
            'Content-Type': 'application/json',
            'Music-User-Token': 'APPLEMUSICMUSICUSERTOKEN',
            'Authorization': f'Bearer {APPLE_MUSIC_ACCESS_TOKEN}'
        }

        data = '{"attributes": {"name": "'+pn+'", "description": ""}}'
        response = requests.post(
            'https://api.music.apple.com/v1/me/library/playlists', headers=headers, data=data)
        print(response.status_code)
        newid = (response.json()['data'][0]['id'])
        APPLE_MUSIC_PLAYLIST_ID = newid
        PLAYLIST_NAME = pn
        return

    chosenPlaylist = playlists[chosenPlaylistIndex]
    name = chosenPlaylist['attributes']['name']
    id = chosenPlaylist['id']
    APPLE_MUSIC_PLAYLIST_ID = f"{id}"
    PLAYLIST_NAME = name


chooseApplePlaylist()
print(PLAYLIST_NAME)
print(APPLE_MUSIC_PLAYLIST_ID)

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

    id = 0
    try:
        id = response.json()['results']['songs']['data'][0]['id']
    except:
        return

    headers = {
        'Content-Type': 'application/json',
        'Music-User-Token': 'APPLEMUSICMUSICUSERTOKEN',
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


while True and (INTERVAL != 0):
    try:
        if checkIfUpdated():
            print("----------------------------------------------------------------")
            getDifference()
        print("---")
        time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping Periodic Updates...")
        sys.exit("Connection closed.")
else:
    if INTERVAL == 0:
        if checkIfUpdated():
            print("----------------------------------------------------------------")
            getDifference()
