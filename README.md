# Music Conversion
A small python script used to convert Spotify Playlists to Google Play Music playlists.

# Running the Program
`python music_conversion.py [spotify_username]`

# Environment Variables
Since this program uses account info, you will need to store your info in a .env file. The file should look as follows:
```
SPOTIPY_CLIENT_ID='example-client-id'
SPOTIPY_CLIENT_SECRET='example-client-secret'
SPOTIPY_REDIRECT_URI='http://localhost:8080/callback/'
GPLAY_USERNAME=example@gmail.com (no quotes)
GPLAY_PW=example_pw (no quotes)
```

# Spotify API Access
You will need to register for Spotify API access in order to generate a client ID and client Secret.
