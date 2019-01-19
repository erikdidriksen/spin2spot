import datetime
import dateutil.parser
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


def ensure_is_soup(html):
    """Ensures the incoming HTML is parsed as a BeautifulSoup object."""
    if isinstance(html, BeautifulSoup):
        return html
    return BeautifulSoup(html, 'html.parser')


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

    @property
    def description(self):
        """Returns a brief description of the episode."""
        day = self.datetime.strftime('%A')
        time = self.datetime.time()
        if not time == datetime.time(0, 0):
            time = self.datetime.strftime('%I:%M%p').lower()
            time = time[1:] if time.startswith('0') else time
            time = ' at {time}'.format(time=time)
        else:
            time = ''
        return '{day}{time} on {station} with {dj}'.format(
            day=day,
            time=time,
            station=self.station,
            dj=self.dj,
            )

    @property
    def title_with_date(self):
        """Returns the title and date of the episode."""
        return '{title}: {date}'.format(
            title=self.title,
            date=self.datetime.strftime('%B %d, %Y'),
            )


class SpinitronV1Parser(BaseParser):
    """Parses an old-style Spinitron episode page."""
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
    """Parses a new-style Spinitron episode page."""
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
        tracks = soup.find('div', class_='spins').findAll('tr')
        return [self._parse_track(track) for track in tracks]

    def _parse_track(self, track):
        artist = track.find('span', class_='artist').text
        title = track.find('span', class_='song').text
        album = track.find('span', class_='release')
        album = album.text if album else ''
        return {'artist': artist, 'title': title, 'album': album}


class WKDUParser(BaseParser):
    """Parses a WKDU episode page."""
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
    """Parses a WPRB episode page."""
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
