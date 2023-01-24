import json

import spotipy
from spotipy import SpotifyOAuth

from models.track import Track
from models.track_feature import TrackFeature

scope = "user-library-read"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

with open('./files/target_playlist_track.json') as json_file:
  contents = json_file.read()

tracks = Track.schema().loads(contents, many=True)

track_uris: [str] = []

for track in tracks:
    track_uris.append(track.uri)

audio_features_result = []
# 100個ずつでリストを分割
n = 100
for i in range(0, len(track_uris), n):
    result = spotify.audio_features(tracks=track_uris[i: i+n])
    tmp_track_feature = TrackFeature.schema().loads(json.dumps(result), many=True)
    audio_features_result.extend(tmp_track_feature)

print(audio_features_result)

TrackFeature.schema().dumps(audio_features_result, many=True)

with open("./files/target_playlist_track_features.json", "w") as outfile:
    outfile.write(TrackFeature.schema().dumps(audio_features_result, many=True, indent=2))