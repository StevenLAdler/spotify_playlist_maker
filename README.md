# spotify_playlist_maker
pulls song links from google sheets (from a google form) and makes spotify playlist.

### 0. Google Sheet Setup

The sheet should be setup such that: 

column A -> timestamps

column B -> names (optional)

column C-?? -> spotify song links (https://open.spotify.com/track/ format)


### 1. Config File Setup

**config.json**
```
{
    "SHEETS"  :
        {
            "SPREADSHEET_ID" : "",
            "SCOPES"         : ["https://www.googleapis.com/auth/spreadsheets.readonly"],
            "RANGE_NAME"     : "Form Responses 1!A2:E"
        },
    "SPOTIFY" :
        {
            "CLIENT_ID"      : "",
            "CLIENT_SECRET"  : "",
            "USERNAME"       : ""
        }
}
```
First, create this file in the spotify_playlist_maker folder.

Right now, you can fill in the SPREADSHEET_ID value and leave the spotify section blank.

Also the RANGE_NAME may have to be tweaked based on the spreadsheet setup.

Here is the spreadsheet that this RANGE_NAME conforms to.

![image](https://user-images.githubusercontent.com/8782132/120356735-e3210200-c2c1-11eb-87a9-ffc284689c4f.png)


### 2. Google Sheets API Setup

Run the quickstart.py file to generate a token.json file and place it in this folder.

More Details here:
https://developers.google.com/sheets/api/quickstart/python

(Note: the quickstart.py file can be deleted after token creation)

Create a Google Cloud project, generate a key, and place it in this folder.

Then set the GOOGLE_APPLICATION_CREDENTIALS environmental variable.

More Details here:
https://cloud.google.com/docs/authentication/getting-started#windows

### 3. Spotify API Setup

Log in to https://developer.spotify.com/dashboard/

Create a new app

Fill in the CLIENT_ID, CLIENT_SECRET, and USERNAME fields in config.json

The 

### 4. Usage

```
python make_playlist.py -c [config] -m [month] -y [year]
```

config: json file created above

month:  MM

year:   YYYY

### Notes:
The script determines month by timestamp

If there are late responses then the date in the Google Sheet must be changed to that of the correct month.

Currently the format of generated playlist names is hardcoded, going to fix this soon

