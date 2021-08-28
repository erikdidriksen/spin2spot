import dateutil.parser
from bs4 import BeautifulSoup as Soup


def ensure_is_soup(html):
    """Ensure the incoming HTML is parsed as a BeautifulSoup object."""
    return html if isinstance(html, Soup) else Soup(html, 'html.parser')


class RadioParser:
    """The base class for episode-page parsers."""

    def __new__(cls, html):
        soup = ensure_is_soup(html)
        return {
            'title': cls._parse_title(soup).strip(),
            'station': cls._parse_station(soup).strip(),
            'dj': cls._parse_dj(soup).strip(),
            'datetime': cls._parse_datetime(soup),
            'tracks': cls._parse_tracks(soup),
            }


class SetlistFMParser:
    """Parse a Setlist.FM page."""

    def __new__(cls, html):
        soup = ensure_is_soup(html)
        artist = cls._parse_artist(soup)
        return {
            'title': artist,
            'venue': cls._parse_venue(soup),
            'datetime': cls._parse_datetime(soup),
            'tracks': cls._parse_tracks(soup, artist),
            }

    @staticmethod
    def _parse_artist(soup):
        return soup.find('h1').find('a').text.strip()

    @staticmethod
    def _parse_venue(soup):
        return soup.find('h1').findAll('a')[1].text.strip()

    @staticmethod
    def _parse_datetime(soup):
        date = soup.find('div', class_='dateBlock').text
        return dateutil.parser.parse(date)

    @classmethod
    def _parse_tracks(cls, soup, artist):
        tracks = soup.findAll('li', class_='song')
        tracks = [cls._parse_track(track, artist) for track in tracks]
        return [track for track in tracks if track is not None]

    @staticmethod
    def _parse_track(track, artist):
        if track.find('span', class_='unknownSong'):
            return None
        title = track.find('a').text
        payload = {'artist': artist, 'title': title}
        links = track.findAll('a')
        if len(links) < 3:
            return payload
        cover_of = links[1].text
        payload['cover_of'] = cover_of
        return payload


class SpinitronV1Parser(RadioParser):
    """Parse an old-style Spinitron episode page."""

    @staticmethod
    def _parse_title(soup):
        return soup.find('p', class_='plhead').find('a').text

    @staticmethod
    def _parse_station(soup):
        return soup.find('p', id='feeds').find('a').text

    @staticmethod
    def _parse_dj(soup):
        return soup.find('div', class_='infoblock').find('a').text

    @staticmethod
    def _parse_datetime(soup):
        date = soup.find('p', class_='plheadsub').text
        date = date[:date.find('–')]  # remove ending time
        date = date.replace('.', ':')
        return dateutil.parser.parse(date)

    @classmethod
    def _parse_tracks(cls, soup):
        tracks = soup.findAll('div', class_='f2row')
        return [cls._parse_track(track) for track in tracks]

    @staticmethod
    def _parse_track(track):
        artist = track.find('span', class_='aw').text
        title = track.find('span', class_='sn').text[1:-1]  # quotes
        album = track.find('span', class_='dn')
        album = album.text if album else ''
        return {'artist': artist, 'title': title, 'album': album}


class SpinitronV2Parser(RadioParser):
    """Parse a new-style Spinitron episode page."""

    @staticmethod
    def _parse_title(soup):
        return soup.find('h3', class_='show-title').text

    @staticmethod
    def _parse_station(soup):
        return soup.find('h1').text

    @staticmethod
    def _parse_dj(soup):
        return soup.find('p', class_='dj-name').find('a').text

    @staticmethod
    def _parse_datetime(soup):
        date = soup.find('p', class_='timeslot').text
        date = date[:date.find('–')]  # remove ending time
        return dateutil.parser.parse(date)

    @classmethod
    def _parse_tracks(cls, soup):
        tracks = soup.findAll('tr', class_='spin-item')
        return [cls._parse_track(track) for track in tracks]

    @staticmethod
    def _parse_track(track):
        artist = track.find('span', class_='artist').text
        title = track.find('span', class_='song').text
        album = track.find('span', class_='release')
        album = album.text if album else ''
        return {'artist': artist, 'title': title, 'album': album}


class WKDUParser(RadioParser):
    """Parse a WKDU episode page."""

    @staticmethod
    def _parse_title(soup):
        sidebar = soup.find('div', class_='panel-col-last')
        return sidebar.find('h2', class_='pane-title').text

    @staticmethod
    def _parse_station(soup):
        return 'WKDU'

    @staticmethod
    def _parse_dj(soup):
        div = soup.find('div', class_='field-field-station-program-dj')
        return div.find('a').text

    @staticmethod
    def _parse_datetime(soup):
        panel = soup.find('div', class_='pane-node-content')
        title = panel.find('h2').text
        date = title.split(' ')[-1]
        return dateutil.parser.parse(date)

    @classmethod
    def _parse_tracks(cls, soup):
        table = soup.find('table', class_='views-table').find('tbody')
        tracks = table.findAll('tr')
        return [cls._parse_track(track) for track in tracks]

    @staticmethod
    def _parse_track(track):
        artist = track.find('td', class_='views-field-artist').text.strip()
        title = track.find('td', class_='views-field-title').text.strip()
        album = track.find('td', class_='views-field-album').text.strip()
        return {'artist': artist, 'title': title, 'album': album}


class WPRBParser(RadioParser):
    """Parse a WPRB episode page."""

    @staticmethod
    def _parse_title(soup):
        return soup.find('h2', class_='playlist-title-text').text

    @staticmethod
    def _parse_station(soup):
        return 'WPRB'

    @staticmethod
    def _parse_dj(soup):
        dj = soup.find('h3', class_='dj-name').text.strip()
        return dj[5:]  # "with "

    @staticmethod
    def _parse_datetime(soup):
        date = soup.find('span', class_='playlist-time').text
        date = ' '.join(date.split('\n')[:2])  # one line
        date = date.split(' to ')[0]  # remove ending time
        return dateutil.parser.parse(date)

    @classmethod
    def _parse_tracks(cls, soup):
        tracks = soup.findAll('tr', class_='playlist-row')
        return [cls._parse_track(track) for track in tracks]

    @staticmethod
    def _parse_track(track):
        artist = track.find('td', class_='playlist-artist').text
        title = track.find('td', class_='playlist-song').text
        album = track.find('td', class_='playlist-album').text
        return {'artist': artist, 'title': title, 'album': album}


class BaseMultiparser:
    """The base class for a parser with subparsers."""
    def __new__(cls, html):
        soup = ensure_is_soup(html)
        for subparser in cls._SUBPARSERS:
            try:
                return subparser(soup)
            except Exception:
                pass
        raise ValueError(f'Cannot parse non-{cls._NAME} content.')


class SpinitronParser(BaseMultiparser):
    _NAME = 'Spinitron'
    _SUBPARSERS = [SpinitronV2Parser, SpinitronV1Parser]


DOMAIN_TO_PARSER = {
    'setlist.fm': SetlistFMParser,
    'spinitron.com': SpinitronParser,
    'wkdu.org': WKDUParser,
    'wprb.com': WPRBParser,
    }


def parse_episode(domain, html):
    """Parse the given episode HTML."""
    try:
        parser = DOMAIN_TO_PARSER[domain]
    except KeyError:
        raise KeyError('Cannot parse content from {domain}.')
    return parser(html)
