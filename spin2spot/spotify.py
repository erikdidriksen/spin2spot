import os


def get_username(username=None):
    """Retrieves the usrename from environment variables if none specified."""
    username = username or os.environ.get('SPIN2SPOT_USERNAME')
    if username:
        return username
    raise ValueError('No username specified or configured.')
