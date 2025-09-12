from ytmusicapi import YTMusic
import csv
import json

# to get brwoser.json:
# run ytmusicapi in console
# login in to yt music infirefox
# start developer tool in firefox
# got to a post request and copy the request header

# Initialize with your headers file
ytmusic = YTMusic('browser.json')

# get songs from json
# Open and read the JSON file
with open('spotify_playlists.json', 'r') as file:
    data = json.load(file)

# create dictionary
# {playlist_name: [list of songs]}
yt_dict = {}
for key, values in data.items():
    yt_dict.update({key: [f"{song['track_name']} {song['artist']}" for song in values]})


# custom playlist Filter:
# enter here the names you really want to convert
# leave it blank if you convert all
wanted_lists = []

# for each playlist search songs:
for playlist in yt_dict.keys():
    
    if (playlist in wanted_lists) or len(wanted_lists)==0:
        print(f"prepare {playlist}...")
        song_ids = []    
        for song in yt_dict[playlist]:
            results = ytmusic.search(song, filter='songs')
            if results:
                song_ids.append(results[0]['videoId'])

        # add to playlist
        playlist_id = ytmusic.create_playlist(
            playlist,
            "Playlist imported from my Spotify",
            privacy_status="PUBLIC"
        )

        # Add songs to the playlist
        ytmusic.add_playlist_items(playlist_id, song_ids)
