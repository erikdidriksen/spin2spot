import os
import spotipy
import spotipy.util as util


def get_username(username=None):
    """Retrieves the usrename from environment variables if none specified."""
    username = username or os.environ.get('SPIN2SPOT_USERNAME')
    if username:
        return username
    raise ValueError('No username specified or configured.')


def build_client(username=None):
    """Builds a Spotipy client scoped for use."""
    username = get_username(username)
    auth = util.prompt_for_user_token(
        username,
        scope='playlist-modify-private playlist-modify-public',
        )
    return spotipy.Spotify(auth=auth)


def albums_match(spotify_track, parsed_track):
    """Returns True if the tracks' album titles match."""
    spotify_album = spotify_track['album']['name']
    parsed_album = parsed_track['album']
    return spotify_album.lower() == parsed_album.lower()


def get_track_id(client, track):
    """Returns the Spotify track ID for the given track."""
    query = 'artist:"{artist}" track:"{title}"'.format(**track)
    results = client.search(q=query)
    if not results['tracks']['total']:
        return None
    results = results['tracks']['items']
    return next(
        (result['id'] for result in results if albums_match(result, track)),
        results[0]['id'],
        )
