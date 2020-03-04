import get_responses

import json

import argparse
import spotipy
import spotipy.util as util

with open('config.json') as config_file:
    data = json.load(config_file)
config_file.close()

client_id     = data['SPOTIFY']['CLIENT_ID']
client_secret = data['SPOTIFY']['CLIENT_SECRET']
username      = data['SPOTIFY']['USERNAME']
    
MONTHS = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='month', help='(numerical)', type=int)

args = parser.parse_args()

sheet = get_responses.DataRetriever()
sheet.setClassVars()
sheet.fetchCreds()
sheet.fetchResults()
responses = sheet.getResults()

song_list = []

for resp in responses:
    if int(resp[0][0]) == args.month:
        for field in resp:
            if "https://open.spotify.com/track/" in field and field not in song_list:
                song_list+=[field]

scope = 'playlist-modify-public'

token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id,
                                   client_secret,
                                   redirect_uri='http://localhost/')

if token:
    pl_name = f"{MONTHS[args.month-1]}_playlist"
    
    sp      = spotipy.Spotify(auth=token)
    pl_list = sp.user_playlists(username)
    names   = [pl['name'] for pl in pl_list['items']]
    if pl_name not in names:
        res = sp.user_playlist_create(username, pl_name, public=True)
        sp.user_playlist_add_tracks(username, res['external_urls']['spotify'],song_list)
        
else:
    print("Can't get token for", username)