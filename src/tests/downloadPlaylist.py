import requests
import sys

## Check Number of Items in Playlist
def checkPlaylistCount():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer #SPOTIFY_ACCESS_TOKEN#',
    }

    response = requests.get(
        'https://api.spotify.com/v1/playlists/2UFkonEBjCjq8Va4sLFylQ', headers=headers)
    return response.json()['tracks']['total']


previousPlaylistCount = 0
with open('previousPlaylistCount.txt', 'r+') as countTextFile:
    data = countTextFile.read()
    print(data)
    previousPlaylistCount = int(data)
    
    countTextFile.truncate(0)
    countTextFile.seek(0)
    countTextFile.write(f"{checkPlaylistCount()}")
    countTextFile.close()
    
if checkPlaylistCount() == previousPlaylistCount:
    ## BREAK
    pass

sys.exit(0)


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer #SPOTIFY_ACCESS_TOKEN#',
}
params = (
    ('offset', '0'),
)
response = requests.get(
    'https://api.spotify.com/v1/playlists/2UFkonEBjCjq8Va4sLFylQ/tracks', headers=headers, params=params)

items = response.json()['items']
print(len(items))
print(items[0]['track']['name'])


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer #SPOTIFY_ACCESS_TOKEN#',
}
params = (
    ('offset', '100'),
)
response = requests.get(
    'https://api.spotify.com/v1/playlists/44wSUeN6x6GFdz0xYzxN5n/tracks', headers=headers, params=params)

items = response.json()['items']
print(len(items))
print(items[-1]['track']['name'])
