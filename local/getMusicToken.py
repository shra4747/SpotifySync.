
import datetime
import pyjwt


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
time_expired = datetime.datetime.now() + datetime.timedelta(hours=12)

headers = {
	"alg": alg,
	"kid": keyId
}

payload = {
	"iss": teamId,
	"exp": int(time_expired.strftime("%s")),
	"iat": int(time_now.strftime("%s"))
}


if __name__ == "__main__":
	"""Create an auth token"""
	token = jwt.encode(payload, secret, algorithm=alg, headers=headers)

	print("----TOKEN----")
	print(token)

	print("----CURL----")
	print("curl -v -H 'Authorization: Bearer %s' \"https://api.music.apple.com/v1/catalog/us/artists/36954\" " % (token))
