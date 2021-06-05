import os
import re
import spotipy
import spotipy.util as util
from .descriptions import playlist_description, playlist_title
from .parsers import parse_episode
from .retrieval import retrieve_episode

INVALID_CHARACTERS = re.compile(
    r'''
    [^        # ignore everything except
    \w\s      # words and whitespace
    \.\:\/    # periods, colons, slashes
    \-\=      # hyphens, equal signs
    ]''',
    re.VERBOSE,
    )


def get_username(username=None):
    """Retrieve the username from environment variables if none specified."""
    username = username or os.environ.get('SPIN2SPOT_USERNAME')
    if username:
        return username
    raise ValueError('No username specified or configured.')


def build_client(username=None):
    """Build a Spotipy client scoped for use."""
    username = get_username(username)
    auth = util.prompt_for_user_token(
        username,
        scope='playlist-modify-private playlist-modify-public',
        )
    return spotipy.Spotify(auth=auth)


def _format_query(string):
    """Format the query string."""
    return INVALID_CHARACTERS.sub('', string)


def _get_track_search_results(client, artist, title, album=None):
    """Return the Spotify track ID for the given track."""
    artist = _format_query(artist)
    title = _format_query(title)
    album = _format_query(album) if album is not None else ''
    query = 'artist:"{artist}" track:"{track}"'.format(
        artist=artist,
        track=title,
        )
    results = client.search(q=query)
    if not results['tracks']['total']:
        return []
    return results['tracks']['items']


def _result_sort_key(track, title, album):
    """Provide a sort key for the returned Spotify tracks.

    Orders by exact title match, then album matching."""
    title_match = track['name'].lower().startswith(title.lower())
    album = album if album is not None else ''
    album_match = track['album']['name'].lower() == album.lower()
    return (not title_match, not album_match)


def get_track_id(client, artist, title, album=None, cover_of=None):
    """Return the Spotify track ID for the given track."""
    results = _get_track_search_results(client, artist, title)
    if not results and cover_of is not None:
        results = _get_track_search_results(client, cover_of, title)
    if not results:
        return None
    results = sorted(
        results,
        key=lambda track: _result_sort_key(track, title, album),
        )
    return results[0]['id']


def create_playlist_from_parser(client, parser, public=False):
    """Create a Spotify playlist for the given parsed episode."""
    tracks = [get_track_id(client, **track) for track in parser.tracks]
    tracks = [track for track in tracks if track]
    user = client.current_user()['id']
    playlist = client.user_playlist_create(
        user=user,
        name=playlist_title(parser),
        public=public,
        description=playlist_description(parser),
        )
    client.user_playlist_add_tracks(
        user=user,
        playlist_id=playlist['id'],
        tracks=tracks,
        )


def create_playlist(client, url, public=False):
    """Create a Spotify playlist for the given URL."""
    domain, html = retrieve_episode(url)
    parser = parse_episode(domain, html)
    create_playlist_from_parser(client, parser, public=public)
