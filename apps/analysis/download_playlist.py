import json
import logging

import spotipy
from marshmallow import EXCLUDE
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from models.artist import Artist
from models.track import Track

scope = "user-library-read"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = spotify.current_user_playlists()

TARGET_PLAYLIST_NAME = "TARAKO PARTY MIX"

target_playlist_uri: str = None

for idx, item in enumerate(results['items']):
    playlist_name: str = item['name']
    if playlist_name == TARGET_PLAYLIST_NAME:
        target_playlist_uri: str = item['uri']
        break

if target_playlist_uri is None:
    logging.fatal('can not found target playlist %s'.format(TARGET_PLAYLIST_NAME))

target_playlist = spotify.playlist(playlist_id=target_playlist_uri)

with open("./files/target_playlist.json", "w") as outfile:
    json.dump(target_playlist, outfile, indent=2)

tracks: [Track] = []

playlist_items_offset = 0
playlist_item_count = 0
playlist_item_limit = 0
while True:
    playlist_items_result = spotify.playlist_items(playlist_id=target_playlist_uri, limit=50,
                                                   offset=playlist_items_offset)
    playlist_item_count += len(playlist_items_result['items'])
    print('playlist item count => {}'.format(playlist_item_count))
    print('playlist item offset => {}'.format(playlist_items_offset))
    print('playlist_items_result len => {}'.format(len(playlist_items_result['items'])))
    for idx, item in enumerate(playlist_items_result['items']):
        track_id: str = item['track']['id']
        track_uri: str = item['track']['uri']
        track_artists: [Artist] = Artist.schema().loads(
            json.dumps(item['track']['album']['artists']),
            many=True,
            unknown=EXCLUDE,
        )
        track_name: str = item['track']['name']
        track_link: str = item['track']['external_urls']['spotify']
        image_x64 = item['track']['album']['images'][2]
        tracks.append(Track(
            id=track_id,
            uri=track_uri,
            artists=track_artists,
            name=track_name,
            link=track_link
        ))
    # オフセットを求めたい
    # オフセット = 50×N
    # 全体 >
    if playlist_items_result['total'] > playlist_item_count:
        remain_item_count = playlist_items_result['total'] - playlist_item_count
        playlist_items_offset += 50
    else:
        break

print(len(tracks))
# print(Track.schema().dumps(tracks, many=True))

with open("./files/target_playlist_track.json", "w") as outfile:
    outfile.write(Track.schema().dumps(tracks, many=True, indent=2))

# print(tracks)
