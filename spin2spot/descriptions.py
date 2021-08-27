import datetime


def today():
    """Return the current datetime."""
    return datetime.datetime.now()  # pragma: no cover


def format_date(dt):
    """Format the datetime as a string."""
    if not isinstance(dt, datetime.datetime):
        return None
    else:
        return dt.strftime('%B %d, %Y')


def format_day_of_week_and_time(dt):
    """Format the datetime as the day of the week & time."""
    if not isinstance(dt, datetime.datetime):
        return ''
    day = dt.strftime('%A')
    time = dt.time()
    if time == datetime.time(0, 0):
        return day
    else:
        time = dt.strftime('%I:%M%p').lower()
        time = time[1:] if time.startswith('0') else time
        return f'{day} at {time}'


def format_station(station):
    """Format the station for a playlist description."""
    return '' if not station else f'on {station}'


def format_dj(dj):
    """Format the DJ's name for a playlist description."""
    return '' if not dj else f'with {dj}'


def playlist_description(parser):
    """Return a brief description for the playlist."""
    if 'venue' in parser:
        return f'At {parser["venue"]}'
    description = [
        format_day_of_week_and_time(parser.get('datetime')),
        format_station(parser.get('station')),
        format_dj(parser.get('dj'))
        ]
    description = ' '.join(phrase for phrase in description if phrase)
    if not description:
        return description
    description = description.split()
    description[0] = description[0].capitalize()
    return ' '.join(description)


def playlist_title_from_parser(parser):
    """Return a formatted title for the playlist, based on the parser data."""
    title = [
        parser.get('title'),
        format_date(parser.get('datetime')),
        ]
    return ': '.join(phrase for phrase in title if phrase)


def playlist_title(parser):
    """Return a title for the playlist.

    Spotify requires a title for new playlists, so if no title can be
    generated, we'll default to today's date."""
    title = playlist_title_from_parser(parser)
    return title if title else format_date(today())
