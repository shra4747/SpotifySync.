## Spotify
import spotify_token as st
data = st.start_session("#SPOTIFY_REFRESH_TOKEN#",
                        "#SPOTIFY_CLIENT_ID#")
access_token = data[0]
SPOTIFY_ACCESS_TOKEN = access_token

## Apple Music
import jwt
import datetime

secret = """#APPLE_MUSIC_PRIVATE_KEY#"""
keyId = "#APPLE_MUSIC_KEY_ID#"
teamId = "#APPLE_MUSIC_TEAM_ID#"

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
