'''
A program to convert a user's Spotify playlists to Google Play Music playlists.

Author: Scott Freeman
Date: July 2017
'''
import os
import sys
import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient
from dotenv import load_dotenv, find_dotenv


'''
Returns Google Play track ids for the given tracks from Spotify using the title and artist as search keyword.
'''
def find_tracks(tracks, mc):
    track_ids = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        query = track['name'] + " " + track['artists'][0]['name']
        result = mc.search(query)
        if len(result['song_hits']) > 0:
            print "Adding Track: " + query
            storeId = result['song_hits'][0]['track']['storeId']
            track_ids.append(storeId)

    return track_ids

'''
Main method to log in to Spotify and Google Play Music accounts to convert Spotify playlists to Google Play Music playlists.
'''
if __name__ == '__main__':
    
    # Load the environment variables:
    # The following enivronment variables should be placed in your .env file:
    # SPOTIPY_CLIENT_ID=''
    # SPOTIPY_CLIENT_SECRET=''
    # SPOTIPY_REDIRECT_URI=''
    # GPLAY_USERNAME= (no quotes)
    # GPLAY_PW= (no quotes)
    load_dotenv(find_dotenv())

    # Set up Google Play Music Mobile Client
    mc = Mobileclient()

    # Retrieve Google Play Music email and password from environment variables
    gplay_email = os.environ['GPLAY_USERNAME']
    gplay_password = os.environ['GPLAY_PW']

    logged_in = mc.login(gplay_email, gplay_password, Mobileclient.FROM_MAC_ADDRESS)

    if logged_in:
        # Save list of current playlists to not add duplicates
        current_playlists = [d['name'] for d in mc.get_all_playlists()]

        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            print "usage: python music_conversion.py [spotify_username]"
            sys.exit()
        scope = 'user-library-read'
        token = util.prompt_for_user_token(username, scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)
            for playlist in playlists['items']:
                if playlist['owner']['id'] == username and playlist['name'] not in current_playlists:
                    print
                    playlist_name = playlist['name']
                    print "Creating playlist: " + playlist_name

                    # Create new Google Play Music playlist with the same name as the Spotify playlist
                    playlist_id = mc.create_playlist(playlist_name)

                    # Extract the tracks from the Spotify playlist
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']

                    # Obtain the Google Play Music track IDs and add them to the new playlist
                    track_ids = find_tracks(tracks, mc)
                    mc.add_songs_to_playlist(playlist_id, track_ids)

                    # Loop for playlists that are longer than 100 tracks
                    while tracks['next']:
                        tracks = sp.next(tracks)
                        track_ids = find_tracks(tracks, mc)
                        print track_ids
                        mc.add_songs_to_playlist(playlist_id, track_ids)
        else:
            print "Cannot get valid token for Spotify"
    else:
        print "Cannot login to Google Play Music"