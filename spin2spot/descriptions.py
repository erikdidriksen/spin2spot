import datetime


def playlist_description(parser):
    """Return a brief description for the playlist."""
    if hasattr(parser, 'venue'):
        return 'At {venue}'.format(venue=parser.venue)
    day = parser.datetime.strftime('%A')
    time = parser.datetime.time()
    if not time == datetime.time(0, 0):
        time = parser.datetime.strftime('%I:%M%p').lower()
        time = time[1:] if time.startswith('0') else time
        time = ' at {time}'.format(time=time)
    else:
        time = ''
    return '{day}{time} on {station} with {dj}'.format(
        day=day,
        time=time,
        station=parser.station,
        dj=parser.dj,
        )


def playlist_title(parser):
    """Return the title and date of the playlist."""
    return '{title}: {date}'.format(
        title=parser.title,
        date=parser.datetime.strftime('%B %d, %Y'),
        )
