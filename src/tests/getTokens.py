## Spotify
import spotify_token as st
data = st.start_session("AQAM7VaqhrmRjIQrz2enYyC0r0tK-X56eiJwU_mAbY8TlqS7D1iMWyGeEgnR2yIgWqGU6b5Du8NVEt-9joCHWhDDH-gWZjsSPYOUVte-kZPRhSuKdmbgURK6CJXUXjyf6uiTRioTNqBScjBhwRsGJqkXRn1bjcGC",
                        "db5da52b-8542-4950-beba-7e548b214b66")
access_token = data[0]
SPOTIFY_ACCESS_TOKEN = access_token

## Apple Music
import jwt
import datetime

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
time_expired = datetime.datetime.now() + datetime.timedelta(hours=0.17)

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

APPLE_MUSIC_ACCESS_TOKEN = token

print(SPOTIFY_ACCESS_TOKEN)
print(APPLE_MUSIC_ACCESS_TOKEN)