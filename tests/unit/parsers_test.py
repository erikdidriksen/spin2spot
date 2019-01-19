import datetime
import pytest
import fixtures
from spin2spot import parsers


@pytest.fixture(scope='module')
def spinitron_v1():
    return fixtures.soup('spinitron_v1.html')


class TestEnsureIsSoup:
    @pytest.fixture
    def soup(self, spinitron_v1):
        return spinitron_v1

    def test_returns_soup_for_soup(self, soup):
        assert parsers.ensure_is_soup(soup) == soup

    def test_returns_soup_for_raw_html(self, soup, html):
        assert parsers.ensure_is_soup(html) == soup


class TestSpinitronV1Parser:
    @pytest.fixture(scope='class')
    def parser(self, spinitron_v1):
        return parsers.SpinitronV1Parser(spinitron_v1)

    @pytest.mark.parametrize('attribute, value', [
        ('title', 'Ruckus Radio'),
        ('station', 'KWVA'),
        ('dj', 'Ruckus the Red'),
        ('datetime', datetime.datetime(2015, 11, 10, 11, 00)),
        ])
    def test_parses_flat_attributes(self, parser, attribute, value):
        assert getattr(parser, attribute) == value

    def test_parses_all_tracks(self, parser):
        assert len(parser.tracks) == 18

    @pytest.mark.parametrize('key, value', [
        ('artist', 'Fuzz'),
        ('title', 'Red Flag'),
        ('album', 'ii'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser.tracks[0][key] == value
