import pandas as pd
import re
import json

# Load the CSV you already created
df = pd.read_csv("spotify_playlists.csv")

# Function to clean text (remove emojis / special characters)
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Remove emojis & weird symbols, keep letters/numbers/punctuation
    text = re.sub(r'[^\w\s.,!?\-:&()\'"]', '', text)
    return text.strip()

# Apply cleaning
for col in ["playlist"]: #, "track_name", "artist", "album"]:
    df[col] = df[col].apply(clean_text)

# New structure: store tracks grouped by playlist
playlists = {}

for _, row in df.iterrows():
    playlist_name = row["playlist"]

    # Keep track + album IDs if they exist in the CSV (optional fallback)
    track_info = {
        "track_name": row["track_name"],
        "artist": row["artist"],
        "album": row["album"],
        "track_id": row.get("track_id", ""),   # will be filled if present
        "album_id": row.get("album_id", "")    # will be filled if present
    }

    playlists.setdefault(playlist_name, []).append(track_info)

# Save JSON
with open("spotify_playlists.json", "w", encoding="utf-8") as f:
    json.dump(playlists, f, indent=2, ensure_ascii=False)

print("✅ Cleaned data with track_id + album_id exported to spotify_playlists.json")
