import argparse


def parse_args(args):
    """Parse the CLI arguments for the script."""
    parser = argparse.ArgumentParser(
        description='Creates Spotify playlists from Spinitron pages',
        add_help=True,
        )
    parser.add_argument(
        'urls',
        action='store',
        nargs='+',
        help='The URLs of Spinitron episodes',
        )
    parser.add_argument(
        '-p', '--public',
        action='store_true',
        default=False,
        required=False,
        help='Makes the resulting playlists public',
        dest='public',
        )
    parser.add_argument(
        '-u', '--user',
        action='store',
        default=None,
        required=False,
        help='The Spotify username to create the playlist with',
        dest='username',
        )
    return vars(parser.parse_args(args))
