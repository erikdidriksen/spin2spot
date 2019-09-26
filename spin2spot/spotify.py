import os
import spotipy
import spotipy.util as util
from .parsers import parse_episode
from .retrieval import retrieve_episode


def get_username(username=None):
    """Retrieves the username from environment variables if none specified."""
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


def _format_query(string):
    """Format the query string."""
    return string.replace("'", "")


def get_track_id(client, track):
    """Returns the Spotify track ID for the given track."""
    track = {k: _format_query(v) for k, v in track.items()}
    query = 'artist:"{artist}" track:"{title}"'.format(**track)
    results = client.search(q=query)
    if not results['tracks']['total']:
        return None
    results = results['tracks']['items']
    return next(
        (result['id'] for result in results if albums_match(result, track)),
        results[0]['id'],
        )


def create_playlist_from_parser(client, parser, public=False):
    """Creates a Spotify playlist for the given parsed episode."""
    tracks = [get_track_id(client, track) for track in parser.tracks]
    tracks = [track for track in tracks if track]
    user = client.current_user()['id']
    playlist = client.user_playlist_create(
        user=user,
        name=parser.title_with_date,
        public=public,
        description=parser.description,
        )
    client.user_playlist_add_tracks(
        user=user,
        playlist_id=playlist['id'],
        tracks=tracks,
        )


def create_playlist(client, url, public=False):
    """Creates a Spotify playlist for the given URL."""
    domain, html = retrieve_episode(url)
    parser = parse_episode(domain, html)
    create_playlist_from_parser(client, parser, public=public)
