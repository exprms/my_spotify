import pandas as pd
import re
import json

# Load the CSV
df = pd.read_csv("spotify_playlists.csv")

# Function to remove emojis and unwanted characters
def clean_text(text):
    if pd.isna(text):
        return ""
    # Remove emojis & non-alphanumeric symbols (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?\-:&()]', '', text)
    # Remove extra spaces
    text = text.strip()
    return text

# Apply cleaning to all text columns
for col in ["playlist"]: #, "track_name", "artist", "album"]:
    df[col] = df[col].astype(str).apply(clean_text)

# Group by playlist, collect tracks
playlists = {}
for _, row in df.iterrows():
    playlist_name = row["playlist"]
    track_info = {
        "track_name": row["track_name"],
        "artist": row["artist"],
        "album": row["album"]
    }
    playlists.setdefault(playlist_name, []).append(track_info)

# Save as JSON
with open("spotify_playlists.json", "w", encoding="utf-8") as f:
    json.dump(playlists, f, indent=2, ensure_ascii=False)

print("✅ Cleaned data exported to spotify_playlists.json")
