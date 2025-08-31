import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


# Fill these with your Spotify app credentials
CLIENT_ID = os.getenv('spotify_ID')
CLIENT_SECRET = os.getenv('spotify_secret')
REDIRECT_URI = "http://127.0.0.1:8888/callback/"

# Scope to read playlists.
SCOPE = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Get current user's playlists
playlists = sp.current_user_playlists()

all_data = []

for playlist in playlists['items']:
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    
    results = sp.playlist_items(playlist_id)
    for item in results['items']:
        track = item['track']
        if track:
            all_data.append({
            "playlist": playlist_name,
            "track_name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "track_id": track['id'],       # Spotify track ID
            "album_id": track['album']['id']  # Spotify album ID
        })

# Save to CSV (best format for importing elsewhere)
df = pd.DataFrame(all_data)
df.to_csv("spotify_playlists.csv", index=False)
print("Exported playlists to spotify_playlists.csv")
