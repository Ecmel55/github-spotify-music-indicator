from dotenv import load_dotenv
import requests
import json
import time
import os

load_dotenv()

github_headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
spotify_headers = {"Authorization": f"Bearer {os.getenv('SPOTIFY_TOKEN')}"}

current_bio = requests.get("https://api.github.com/user", headers=github_headers).json()["bio"]

while True:
    current_track = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=spotify_headers, params={"market": "TR"})
    if current_track.status_code == 204:
        requests.patch("https://api.github.com/user", headers=github_headers, data=f"{json.dumps({'bio': current_bio})}")
        time.sleep(5)
        continue
    elif current_track.status_code == 401:
        print("Invalid Spotify token")
        break
    current_track = current_track.json()
    if current_track["is_playing"]:
        song_name = f"{current_track['item']['name']} ({', '.join([artist['name'] for artist in current_track['item']['artists']])})"
        requests.patch("https://api.github.com/user", headers=github_headers, data=f"{json.dumps({'bio': f'Now listening: {song_name}'})}")
    else:   
        requests.patch("https://api.github.com/user", headers=github_headers, data=f"{json.dumps({'bio': current_bio})}")
    time.sleep(5)



    