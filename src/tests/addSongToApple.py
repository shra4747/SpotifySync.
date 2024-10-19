import requests
import datetime
import jwt

secret = """#APPLE_MUSIC_PRIVATE_KEY#"""
keyId = "#APPLE_MUSIC_KEY_ID#"
teamId = "#APPLE_MUSIC_TEAM_ID#"
alg = 'ES256'

time_now = datetime.datetime.now()
time_expired = datetime.datetime.now() + datetime.timedelta(hours=0.017)

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


headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': '#APPLE_MUSIC_USER_TOKEN#',
    'Authorization': f'Bearer {token}',
}
input = input("Song name: ").replace("feat. ", "").replace(" ", "+")

response = requests.get(
    f'https://api.music.apple.com/v1/catalog/us/search?term={input}&types=songs', headers=headers)

id = response.json()['results']['songs']['data'][0]['id']
print(id)

headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': '#APPLE_MUSIC_USER_TOKEN#',
    'Authorization': f'Bearer {token}',
}

data = '{"data": [{"id": "' + f"{id}" + '", "type": "songs"}]}'
response = requests.post(
    'https://api.music.apple.com/v1/me/library/playlists/p.gek1161ULXbLMGk/tracks', headers=headers, data=data)
print(response.status_code)
