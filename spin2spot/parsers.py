import dateutil.parser
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as Soup


def ensure_is_soup(html):
    """Ensure the incoming HTML is parsed as a BeautifulSoup object."""
    return html if isinstance(html, Soup) else Soup(html, 'html.parser')


class BaseParser(ABC):
    """The base class for episode-page parsers."""
    def __init__(self, html):
        soup = ensure_is_soup(html)
        self.title = self._parse_title(soup).strip()
        self.station = self._parse_station(soup).strip()
        self.dj = self._parse_dj(soup).strip()
        self.datetime = self._parse_datetime(soup)
        self.tracks = self._parse_tracks(soup)

    @abstractmethod
    def _parse_title(self):
        """Parse the show's title."""
        raise NotImplementedError

    @abstractmethod
    def _parse_station(self):
        """Parse the show's radio station."""
        raise NotImplementedError

    @abstractmethod
    def _parse_dj(self):
        """Parse the name of the  show's DJ."""
        raise NotImplementedError

    @abstractmethod
    def _parse_datetime(self):
        """Parse the show's air date and time."""
        raise NotImplementedError

    @abstractmethod
    def _parse_tracks(self):
        """Parse the show's tracks."""
        raise NotImplementedError


class SetlistFMParser(BaseParser):
    """Parse a Setlist.FM page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.venue = self.station
        self.station = ''

    def _parse_title(self, soup):
        return soup.find('h1').find('a').text.strip()

    def _parse_station(self, soup):
        """Capture the venue name; later overriden in __init__."""
        return soup.find('h1').findAll('a')[1].text.strip()

    def _parse_dj(self, soup):
        return ''

    def _parse_datetime(self, soup):
        date = soup.find('div', class_='dateBlock').text
        return dateutil.parser.parse(date)

    def _parse_tracks(self, soup):
        tracks = soup.findAll('li', class_='song')
        tracks = [self._parse_track(track) for track in tracks]
        return [track for track in tracks if track is not None]

    def _parse_track(self, track):
        if track.find('span', class_='unknownSong'):
            return None
        artist = self.title
        title = track.find('a').text
        payload = {'artist': artist, 'title': title}
        links = track.findAll('a')
        if len(links) < 3:
            return payload
        cover_of = links[1].text
        payload['cover_of'] = cover_of
        return payload


class SpinitronV1Parser(BaseParser):
    """Parse an old-style Spinitron episode page."""
    def _parse_title(self, soup):
        return soup.find('p', class_='plhead').find('a').text

    def _parse_station(self, soup):
        return soup.find('p', id='feeds').find('a').text

    def _parse_dj(self, soup):
        return soup.find('div', class_='infoblock').find('a').text

    def _parse_datetime(self, soup):
        date = soup.find('p', class_='plheadsub').text
        date = date[:date.find('–')]  # remove ending time
        date = date.replace('.', ':')
        return dateutil.parser.parse(date)

    def _parse_tracks(self, soup):
        tracks = soup.findAll('div', class_='f2row')
        return [self._parse_track(track) for track in tracks]

    def _parse_track(self, track):
        artist = track.find('span', class_='aw').text
        title = track.find('span', class_='sn').text[1:-1]  # quotes
        album = track.find('span', class_='dn')
        album = album.text if album else ''
        return {'artist': artist, 'title': title, 'album': album}


class SpinitronV2Parser(BaseParser):
    """Parse a new-style Spinitron episode page."""
    def _parse_title(self, soup):
        return soup.find('h3', class_='show-title').text

    def _parse_station(self, soup):
        return soup.find('h1').text

    def _parse_dj(self, soup):
        return soup.find('p', class_='dj-name').find('a').text

    def _parse_datetime(self, soup):
        date = soup.find('p', class_='timeslot').text
        date = date[:date.find('–')]  # remove ending time
        return dateutil.parser.parse(date)

    def _parse_tracks(self, soup):
        tracks = soup.findAll('tr', class_='spin-item')
        return [self._parse_track(track) for track in tracks]

    def _parse_track(self, track):
        artist = track.find('span', class_='artist').text
        title = track.find('span', class_='song').text
        album = track.find('span', class_='release')
        album = album.text if album else ''
        return {'artist': artist, 'title': title, 'album': album}


class WKDUParser(BaseParser):
    """Parse a WKDU episode page."""
    def _parse_title(self, soup):
        sidebar = soup.find('div', class_='panel-col-last')
        return sidebar.find('h2', class_='pane-title').text

    def _parse_station(self, soup):
        return 'WKDU'

    def _parse_dj(self, soup):
        div = soup.find('div', class_='field-field-station-program-dj')
        return div.find('a').text

    def _parse_datetime(self, soup):
        panel = soup.find('div', class_='pane-node-content')
        title = panel.find('h2').text
        date = title.split(' ')[-1]
        return dateutil.parser.parse(date)

    def _parse_tracks(self, soup):
        table = soup.find('table', class_='views-table').find('tbody')
        tracks = table.findAll('tr')
        return [self._parse_track(track) for track in tracks]

    def _parse_track(self, track):
        artist = track.find('td', class_='views-field-artist').text.strip()
        title = track.find('td', class_='views-field-title').text.strip()
        album = track.find('td', class_='views-field-album').text.strip()
        return {'artist': artist, 'title': title, 'album': album}


class WPRBParser(BaseParser):
    """Parse a WPRB episode page."""
    def _parse_title(self, soup):
        return soup.find('h2', class_='playlist-title-text').text

    def _parse_station(self, soup):
        return 'WPRB'

    def _parse_dj(self, soup):
        dj = soup.find('h3', class_='dj-name').text.strip()
        return dj[5:]  # "with "

    def _parse_datetime(self, soup):
        date = soup.find('span', class_='playlist-time').text
        date = ' '.join(date.split('\n')[:2])  # one line
        date = date.split(' to ')[0]  # remove ending time
        return dateutil.parser.parse(date)

    def _parse_tracks(self, soup):
        tracks = soup.findAll('tr', class_='playlist-row')
        return [self._parse_track(track) for track in tracks]

    def _parse_track(self, track):
        artist = track.find('td', class_='playlist-artist').text
        title = track.find('td', class_='playlist-song').text
        album = track.find('td', class_='playlist-album').text
        return {'artist': artist, 'title': title, 'album': album}


class BaseMultiparser(ABC):
    """The base class for a parser with subparsers."""
    def __init__(self, html):
        soup = ensure_is_soup(html)
        for subparser in self._SUBPARSERS:
            try:
                self._parser = subparser(soup)
                break
            except Exception:
                pass
        if '_parser' not in self.__dict__:
            raise ValueError('Cannot parse non-{name} content.'.format(
                name=self._NAME,
                ))

    def __getattr__(self, attribute):
        return getattr(self._parser, attribute)


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
        raise KeyError('Cannot parse content from {domain}.'.format(
            domain=domain,
            ))
    return parser(html)
