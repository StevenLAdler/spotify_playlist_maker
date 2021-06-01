import get_responses

import json
import datetime

import argparse
import spotipy
import spotipy.util as util

#TODO make the date arguments cleaner

parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='month', help='(numerical)', type=int)
parser.add_argument('-y', dest='year', help='(numerical)', type=int)
parser.add_argument('-c', dest='config', help='(string)', type=str)

args = parser.parse_args()

with open(args.config) as config_file:
    data = json.load(config_file)
config_file.close()

client_id     = data['SPOTIFY']['CLIENT_ID']
client_secret = data['SPOTIFY']['CLIENT_SECRET']
username      = data['SPOTIFY']['USERNAME']
pl_format     = data['SPOTIFY']['PL_FORMAT']
pl_desc       = data['SPOTIFY']['PL_DESC']
    
MONTHS = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

MONTH = MONTHS[args.month-1]

YEAR = datetime.datetime.now().year

if(args.year is not None):
    YEAR = args.year

sheet = get_responses.DataRetriever()
sheet.setConfig(args.config)
sheet.setClassVars()
sheet.fetchCreds()
sheet.fetchResults()
responses = sheet.getResults()

song_list = []

for resp in responses:

    #TODO use datetime to determine if date falls in range

    if resp == []:
        continue
    month = resp[0].split('/')[0]
    year = resp[0].split('/')[2].split(' ')[0]
    if not (month.isnumeric() and int(month) == args.month) or not (year.isnumeric() and int(year) == YEAR):
        continue
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
    pl_name = pl_format.format(MONTH=MONTH, YEAR=YEAR)
    
    sp      = spotipy.Spotify(auth=token)
    pl_list = sp.user_playlists(username)
    names   = [pl['name'] for pl in pl_list['items']]
    if pl_name not in names:
        res = sp.user_playlist_create(username, 
                                      pl_name, 
                                      public=True, 
                                      description=pl_desc)
        sp.user_playlist_add_tracks(username, 
                                    res['external_urls']['spotify'],
                                    song_list)
        
else:
    print("Can't get token for", username)