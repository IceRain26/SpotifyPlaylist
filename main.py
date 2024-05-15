import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Input for year for top songs for playlist of the year
date = input("Which Year do you want to travel to? Type the date in format YYYY-MM-DD\n")

# Scraping from Billboard 100 top songs of input year
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
website = response.text

soup = BeautifulSoup(website, "html.parser")
songs = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in songs]

# Authentication of app
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URL"],
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"))

user_id = sp.current_user()["id"]

# Search for the songs on spotify
song_uri = []
year = date.split("-")[0]
for song in song_names:
    data = sp.search(q=f"tracks:{song} year:{year}", type="track")
    try:
        uri = data["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} does not exists in Spotify.")

# Create Playlist and add to spotify
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date} Billboard 100 FireSongs",
                                   public=False,
                                   description="Billboard Project")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
