import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNDWTdSM0o2VlIifQ.eyJpc3MiOiI2NkFWUUsyVEY5IiwiZXhwIjoxNjM4NDUyNjE4LCJpYXQiOjE2Mzg0MDk0MTh9.azz_d8mrUArEZJ1U6z-6GW9IlFlHNGQTBKBwBsoUFWKaxPN0LhvWvJn-qawzeNdoA-q0qeRFltx_8JqQ1NgkMQ',
}
input = input("Song name: ").replace(" ", "+")
params = (
    ('term', input),
    ('types', 'songs'),
)

response = requests.get(
    'https://api.music.apple.com/v1/catalog/us/search', headers=headers, params=params)
id = response.json()['results']['songs']['data'][0]['id']
print(id)

headers = {
    'Content-Type': 'application/json',
    'Music-User-Token': 'AiwFMOzjHh+6W/edDaw1b7YBv2/kodj+0Orp2sUpRCu4gml35ZRFmTfjPeNxShph5olp7GZ83OSQgwbrcWUmM9Gt8V+rZ2ZCi0KfNoVq6gNe80OfgpFtRvp2y5adEysVwEYwWQUz7Ck9Y7BmY7KorbvSz1RtkAV6DNwcCizRJMY1gdVOQaGQx1zeHMu0GiiN+PuqAa1KLFvQ1g9uQgUqUD0xvRFPgBm6+fV7fC4ZlZ5/eQjdBA==',
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNDWTdSM0o2VlIifQ.eyJpc3MiOiI2NkFWUUsyVEY5IiwiZXhwIjoxNjM4NDUyNjE4LCJpYXQiOjE2Mzg0MDk0MTh9.azz_d8mrUArEZJ1U6z-6GW9IlFlHNGQTBKBwBsoUFWKaxPN0LhvWvJn-qawzeNdoA-q0qeRFltx_8JqQ1NgkMQ',
}

data = '{"data": [{"id": "' + f"{id}" + '", "type": "songs"}]}'
response = requests.post(
    'https://api.music.apple.com/v1/me/library/playlists/p.gek1161ULXbLMGk/tracks', headers=headers, data=data)
print(response.status_code)

