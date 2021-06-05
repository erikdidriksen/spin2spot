import datetime


def playlist_description(parser):
    """Return a brief description for the playlist."""
    if 'venue' in parser:
        return f'At {parser["venue"]}'
    day = parser['datetime'].strftime('%A')
    time = parser['datetime'].time()
    if not time == datetime.time(0, 0):
        time = parser['datetime'].strftime('%I:%M%p').lower()
        time = time[1:] if time.startswith('0') else time
        time = f' at {time}'
    else:
        time = ''
    return f'{day}{time} on {parser["station"]} with {parser["dj"]}'


def playlist_title(parser):
    """Return the title and date of the playlist."""
    return f'{parser["title"]}: {parser["datetime"].strftime("%B %d, %Y")}'
