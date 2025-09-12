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
wanted_lists = ['.Erinnerungen','BassLines','Silvester24','Summer 24','Dream Setlist by Winston','Nov2023','Meine Playlist Nr. 47','Cannibal corpse tour 2023','Div','Drum Practice','Krimis & Thriller','Spring 2022','My classic','Mallnitz','Shazam','OWRRB1','Real Metal','Austropop Schmankerl','Hey Good Morning','Emotional 2.0','On Tour','Party Bergwerk','Süvesta','Autofahren','gestolpert','Neu klassik','SW Live Vienna 2018','Hörbücher gehört','Weihnachten 2017','Crossfit 2016','Emotional','Collection 20172018','New 1017']

# for each playlist search songs:
for playlist in yt_dict.keys():
    
    if playlist in wanted_lists:
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
