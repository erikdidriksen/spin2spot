import sys
from .cli import parse_args
from .spotify import build_client, create_playlist


def run_module(urls, username=None, public=False):
    """Creates Spotify playlists from the given URLs."""
    client = build_client(username)
    for url in urls:
        create_playlist(client, url, public=public)
    print('Created {count} playlist{s} for user {user}.'.format(
        count=len(urls),
        s='' if len(urls) == 1 else 's',
        user=client.current_user()['id'],
        ))


if __name__ == '__main__':
    params = parse_args(sys.argv[1:])
    run_module(**params)
