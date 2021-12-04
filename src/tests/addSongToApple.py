import requests
import datetime
import jwt

secret = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgsKEXEpjm8r56xBxh
5vYKZQludszwGmC7TYIP57ZxydCgCgYIKoZIzj0DAQehRANCAASYqNk6VqSH6Kp3
b/gqCz2P/V2jtfMtDV/NsVgirfEmDx9xBFPJR77xW4rmq9rX63+stFIrb1QcO5FR
xyc16f43
-----END PRIVATE KEY-----"""
keyId = "3CY7R3J6VR"
teamId = "66AVQK2TF9"
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
    'Authorization': f'Bearer {token}',
}
input = input("Song name: ").replace("feat. ", "").replace(" ", "+")

response = requests.get(
    f'https://api.music.apple.com/v1/catalog/us/search?term={input}&types=songs', headers=headers)

id = response.json()['results']['songs']['data'][0]['id']
print(id)

headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': 'AiwFMOzjHh+6W/edDaw1b7YBv2/kodj+0Orp2sUpRCu4gml35ZRFmTfjPeNxShph5olp7GZ83OSQgwbrcWUmM9Gt8V+rZ2ZCi0KfNoVq6gNe80OfgpFtRvp2y5adEysVwEYwWQUz7Ck9Y7BmY7KorbvSz1RtkAV6DNwcCizRJMY1gdVOQaGQx1zeHMu0GiiN+PuqAa1KLFvQ1g9uQgUqUD0xvRFPgBm6+fV7fC4ZlZ5/eQjdBA==',
    'Authorization': f'Bearer {token}',
}

data = '{"data": [{"id": "' + f"{id}" + '", "type": "songs"}]}'
response = requests.post(
    'https://api.music.apple.com/v1/me/library/playlists/p.gek1161ULXbLMGk/tracks', headers=headers, data=data)
print(response.status_code)
