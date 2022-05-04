import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import credLib
import configlib
def auth():
    os.environ["SPOTIPY_CLIENT_ID"] = credLib.returnbykey('spotify','SPOTIPY_CLIENT_ID')
    os.environ["SPOTIPY_CLIENT_SECRET"] = credLib.returnbykey('spotify','SPOTIPY_CLIENT_SECRET')
    os.environ["SPOTIPY_REDIRECT_URI"] =  credLib.returnbykey('spotify','"SPOTIPY_REDIRECT_URI"')
    scope = "user-read-playback-state", "user-modify-playback-state", "playlist-read-private "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return(sp)
def read_current_song():
    return(auth().current_playback())

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def pausemusic():
    auth().pause_playback()
def skipmusic():
    auth().next_track()
def backmusic():
    auth().previous_track()
def resume():
    auth().start_playback()
def selectplaylist(text, device):
    device = '121f1c72bf10d92aa9e555d7c6119ff9386eadf4'
    max = 0
    maxuri = ""
    max_name = ""
    query = listplaylists()
    for x in range(0, len(query["items"])):
        score = jaccard(text, str(query["items"][x]["name"]))
        if(score > max):
            maxuri = str(query["items"][x]["uri"])
            max = score
            max_name = str(query["items"][x]["name"])
    print(score)
    print(max_name)
    auth().start_playback(device_id= device, context_uri=maxuri)

def selectsong(text, device):
    device = '121f1c72bf10d92aa9e555d7c6119ff9386eadf4'
    q = text
    query = auth().search(q, limit=1, offset=0, type='track', market=None)
    for key in query.keys():
        for x in range(0 , len(query["tracks"]["items"])):
            muri= query["tracks"]["items"][x]["uri"]
    auth().start_playback(device_id= device, uris=[muri])
def get_devices():
    return(auth().devices())
def listplaylists():
    return(auth().current_user_playlists(limit=50, offset=0))






#start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
