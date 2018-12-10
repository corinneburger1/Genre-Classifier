import spotipy
from joblib import load
import spotipy.oauth2 as oauth2

def classifySong(trackID, sp):
    model = load("/home/corinneburger1/Genre-Classifier/app/static/RandomForestModel.joblib")
    # model = load("/Users/corinneburger/Dropbox/Junior Year/ML/Genre-Classifier/app/static/RandomForestModel.joblib")
    song = getTrackFeatures(trackID, sp)
    ret = model.predict([song])[0]
    return ret

def getTrackFeatures(trackID, sp):
    attributes = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    song_features = sp.audio_features(trackID)
    song_features = song_features[0]
    song_features_cleaned = []
    for attribute in attributes:
        song_features_cleaned.append(song_features[attribute])
    song_features_cleaned += getTimbrePitch(trackID, sp)
    return song_features_cleaned

def getTimbrePitch(trackId, sp):
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

def generateSpotifyObject():
    clientID = "1bb4ca2adbe14ec299ae000ec92fd78e"
    clientSecret = "51f6ca11380a425e95ae29b704ed5069"
    credentials = oauth2.SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
    token = credentials.get_access_token()
    return spotipy.Spotify(auth=token)

def classify(query):
    sp = generateSpotifyObject()
    id_header = "spotify:track:"
    result = sp.search(q='track:' + query, type='track')["tracks"]["items"][0]
    song_name = result["name"]
    song_artist = result["artists"][0]["name"]
    song_id = result["id"]
    return "We think " + song_name + " by " + song_artist + " is a " + classifySong(id_header + song_id, sp) + " song."