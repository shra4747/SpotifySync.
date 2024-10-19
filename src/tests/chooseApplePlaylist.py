import requests

headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': '#APPLE_MUSIC_USER_TOKEN#',
    'Authorization': '#APPLE_MUSIC_BEARER_TOKEN#',
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
print(f"{id}: {name}")
