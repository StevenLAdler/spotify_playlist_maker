from get_responses import DataRetriever, Config

import json
from datetime import datetime, timedelta

import argparse
import spotipy
import spotipy.util as util

def parse_date_string(date_string, date_format):
    if date_string is None:
        return None

    try:
        date = datetime.strptime(date_string, date_format)
    except ValueError as ve:
        print(f'Unable to parse date string: {date_string}. Date string expected to be in {date_format} format')
        return None

    return date

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='month', help='(numerical)', type=int)
    parser.add_argument('-y', dest='year', help='(numerical)', type=int)
    parser.add_argument('-c', dest='config', help='(string)', type=str)
    parser.add_argument('-st', dest='start_time', help='(sting)', type=str)
    parser.add_argument('-et', dest='end_time', help='(sting)', type=str)

    args = parser.parse_args()

    default_config_path = 'config.json'
    config = Config(args.config) if args.config is not None else Config(default_config_path)

    start_time_arg = parse_date_string(args.start_time, '%m/%d/%y')
    end_time_arg = parse_date_string(args.end_time, '%m/%d/%y')

    start_time = start_time_arg if start_time_arg is not None else datetime.now() - timedelta(days=28)
    end_time = end_time_arg if end_time_arg is not None else datetime.now()
        
    MONTHS = ('JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC')

    MONTH = MONTHS[args.month-1]

    YEAR = args.year if args.year is not None else datetime.now().year

    sheet = DataRetriever()
    sheet.fetchCreds(config)
    sheet.fetchResults(config)
    responses = sheet.results

    song_list = []

    for resp in responses:

        if resp == []:
            continue

        date = parse_date_string(resp[0], '%m/%d/%Y %H:%M:%S')

        if date is None or not (date >= start_time and date <= end_time):
            continue

        for field in resp:
            if "https://open.spotify.com/track/" in field and field not in song_list:
                song_list+=[field]

    scope = 'playlist-modify-public'

    token = util.prompt_for_user_token(config.username,
                                    scope,
                                    config.client_id,
                                    config.client_secret,
                                    redirect_uri='http://localhost/')

    if token:
        pl_name = config.pl_format.format(MONTH=MONTH, YEAR=YEAR)
        
        sp      = spotipy.Spotify(auth=token)
        pl_list = sp.user_playlists(config.username)
        names   = [pl['name'] for pl in pl_list['items']]
        if pl_name not in names:
            res = sp.user_playlist_create(config.username, 
                                        pl_name, 
                                        public=True, 
                                        description=config.pl_desc)
            sp.user_playlist_add_tracks(config.username, 
                                        res['external_urls']['spotify'],
                                        song_list)
            
    else:
        print("Can't get token for", config.username)


if __name__ == "__main__":
  main()