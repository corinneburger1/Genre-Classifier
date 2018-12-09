import spotipy
import sklearn
from joblib import load
import spotipy.util as util

username = "kchesner98"
clientID = "1bb4ca2adbe14ec299ae000ec92fd78e"
clientSecret = "51f6ca11380a425e95ae29b704ed5069"
redirectURI = "http://google.com/"
SCOPE = "playlist-modify-public"

# prompt for user permissions
token = util.prompt_for_user_token(username, scope = SCOPE, client_id=clientID, client_secret = clientSecret, redirect_uri = redirectURI)

# create spotify object
sp = spotipy.Spotify(auth=token)

def classifySong(trackID):
    model = load("RandomForestModel.joblib")
    song = getTrackFeatures(trackID)
    ret = model.predict([song])[0]
    return ret

def getTrackFeatures(trackID):
    attributes = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    song_features = sp.audio_features(trackID)
    song_features = song_features[0]
    song_features_cleaned = []
    for attribute in attributes:
        song_features_cleaned.append(song_features[attribute])
    song_features_cleaned += getTimbrePitch(trackID)
    return song_features_cleaned


def getTimbrePitch(trackId):
    audioAnalysis = sp.audio_analysis(trackId)
    audioSegments = audioAnalysis["segments"]
    timbreVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 12 timbre attributes
    for s in audioSegments:
        timbre = s["timbre"]
        for i in range(len(timbre)):
            timbreVector[i] += timbre[i]
    for i in range(len(timbreVector)):
        timbreVector[i] /= len(audioSegments)

    pitchVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 12 pitch attributes
    for s in audioSegments:
        pitch = s["pitches"]
        for i in range(len(pitch)):
            pitchVector[i] += pitch[i]
    for i in range(len(pitchVector)):
        pitchVector[i] /= len(audioSegments)
    return timbreVector + pitchVector

def classify(query):
    id_header = "spotify:track:"
    result = sp.search(q='track:' + query, type='track')["tracks"]["items"][0]
    song_name = result["name"]
    song_artist = result["artists"][0]["name"]
    song_id = result["id"]
    return "We think " + song_name + " by " + song_artist + " is a " + classifySong(id_header + song_id) + " song."