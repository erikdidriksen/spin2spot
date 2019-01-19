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