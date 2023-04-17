#   GitHub-Spotify Music Indicator - Changes GitHub bio with currently playing music from Spotify.
#   Copyright (C) 2022  Ecmel(Ecmel55), Kerem(Kerem00) 

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
        requests.patch("https://api.github.com/user", headers=github_headers, data=json.dumps({"bio": current_bio}))
        time.sleep(5)
        continue
    elif current_track.status_code == 401:
        print("Invalid Spotify token")
        break
    current_track = current_track.json()
    if current_track["is_playing"]:
        song_name = f"{current_track['item']['name']} ({', '.join([artist['name'] for artist in current_track['item']['artists']])})"
        requests.patch("https://api.github.com/user", headers=github_headers, data=json.dumps({"bio": f"Now listening: {song_name}"}))
    else:   
        requests.patch("https://api.github.com/user", headers=github_headers, data=json.dumps({"bio": current_bio}))
    time.sleep(5)
