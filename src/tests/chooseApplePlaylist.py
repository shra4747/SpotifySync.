import requests

headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': 'AiwFMOzjHh+6W/edDaw1b7YBv2/kodj+0Orp2sUpRCu4gml35ZRFmTfjPeNxShph5olp7GZ83OSQgwbrcWUmM9Gt8V+rZ2ZCi0KfNoVq6gNe80OfgpFtRvp2y5adEysVwEYwWQUz7Ck9Y7BmY7KorbvSz1RtkAV6DNwcCizRJMY1gdVOQaGQx1zeHMu0GiiN+PuqAa1KLFvQ1g9uQgUqUD0xvRFPgBm6+fV7fC4ZlZ5/eQjdBA==',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjNDWTdSM0o2VlIifQ.eyJpc3MiOiI2NkFWUUsyVEY5IiwiZXhwIjoxNjM4NTMyOTk4LCJpYXQiOjE2Mzg0ODk3OTh9.lJhCDjnPFOz4YUqHiurlrUI1akqalTCyMIPBke3Wu1B6Mh1JKWYLlUj-LLuIDqDJp988aTdAIIAOLhxECte29g',
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