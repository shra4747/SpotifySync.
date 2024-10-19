import requests
headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': '#APPLE_MUSIC_USER_TOKEN#',
    'Authorization': 'Bearer {APPLE_MUSIC_USER_TOKEN}'
}

data = '{"attributes": {"name": "Some Playlist", "description": ""}}'
response = requests.post(
    'https://api.music.apple.com/v1/me/library/playlists', headers=headers, data=data)
id = (response.json()['data'][0]['id'])
