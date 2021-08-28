import datetime
import pytest
import fixtures
from spin2spot import parsers


@pytest.fixture(scope='module')
def setlist_fm():
    return fixtures.soup('setlist_fm.html')


@pytest.fixture(scope='module')
def spinitron_v1():
    return fixtures.soup('spinitron_v1.html')


@pytest.fixture(scope='module')
def spinitron_v2():
    return fixtures.soup('spinitron_v2.html')


@pytest.fixture(scope='module')
def wkdu():
    return fixtures.soup('wkdu.html')


@pytest.fixture(scope='module')
def wprb():
    return fixtures.soup('wprb.html')


class TestEnsureIsSoup:
    @pytest.fixture
    def soup(self, spinitron_v1):
        return spinitron_v1

    def test_returns_soup_for_soup(self, soup):
        assert parsers.ensure_is_soup(soup) == soup

    def test_returns_soup_for_raw_html(self, soup, html):
        assert parsers.ensure_is_soup(html) == soup


class TestSetlistFMParser:
    @pytest.fixture(scope='class')
    def parser(self, setlist_fm):
        return parsers.SetlistFMParser(setlist_fm)

    @pytest.mark.parametrize('attribute, value', [
        ('title', 'The Lemonheads'),
        ('datetime', datetime.datetime(2019, 5, 4)),
        ('venue', 'Brooklyn Bowl, Brooklyn, NY, USA'),
        ])
    def test_parses_flat_attributes(self, parser, attribute, value):
        assert parser[attribute] == value

    def test_parses_all_tracks(self, parser):
        assert len(parser['tracks']) == 23

    @pytest.mark.parametrize('key, value', [
        ('artist', 'The Lemonheads'),
        ('title', 'Being Around'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser['tracks'][1][key] == value

    @pytest.mark.parametrize('key, value', [
        ('artist', 'The Lemonheads'),
        ('title', 'The Outdoor Type'),
        ('cover_of', 'Smudge'),
        ])
    def test_parses_cover_track_attributes(self, parser, key, value):
        assert parser['tracks'][0][key] == value


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
        assert parser[attribute] == value

    def test_parses_all_tracks(self, parser):
        assert len(parser['tracks']) == 18

    @pytest.mark.parametrize('key, value', [
        ('artist', 'Fuzz'),
        ('title', 'Red Flag'),
        ('album', 'ii'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser['tracks'][0][key] == value


class TestSpinitronV2Parser:
    @pytest.fixture(scope='class')
    def parser(self, spinitron_v2):
        return parsers.SpinitronV2Parser(spinitron_v2)

    @pytest.mark.parametrize('attribute, value', [
        ('title', '7DayWknd'),
        ('station', 'WZBC 90.3 FM Newton'),
        ('dj', 'Nick'),
        ('datetime', datetime.datetime(2016, 8, 2, 14, 00)),
        ])
    def test_parses_flat_attributes(self, parser, attribute, value):
        assert parser[attribute] == value

    def test_parses_all_tracks(self, parser):
        assert len(parser['tracks']) == 16

    @pytest.mark.parametrize('key, value', [
        ('artist', 'Future Teens'),
        ('title', 'Action Potential'),
        ('album', 'Action Potential - Single'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser['tracks'][8][key] == value


class TestWKDUParser:
    @pytest.fixture(scope='class')
    def parser(self, wkdu):
        return parsers.WKDUParser(wkdu)

    @pytest.mark.parametrize('attribute, value', [
        ('title', 'The New Matt Show'),
        ('station', 'WKDU'),
        ('dj', 'Matt'),
        ('datetime', datetime.datetime(2013, 10, 1)),
        ])
    def test_parses_flat_attributes(self, parser, attribute, value):
        assert parser[attribute] == value

    def test_parses_all_tracks(self, parser):
        assert len(parser['tracks']) == 26

    @pytest.mark.parametrize('key, value', [
        ('artist', 'Big Star'),
        ('title', 'September Gurls'),
        ('album', 'Radio City'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser['tracks'][0][key] == value


class TestWPRBParser:
    @pytest.fixture(scope='class')
    def parser(self, wprb):
        return parsers.WPRBParser(wprb)

    @pytest.mark.parametrize('attribute, value', [
        ('title', 'Hometown Soundsystem'),
        ('station', 'WPRB'),
        ('dj', 'Bad Newz'),
        ('datetime', datetime.datetime(2015, 11, 10, 14, 00)),
        ])
    def test_parses_flat_attributes(self, parser, attribute, value):
        assert parser[attribute] == value

    def test_parses_all_tracks(self, parser):
        assert len(parser['tracks']) == 43

    @pytest.mark.parametrize('key, value', [
        ('artist', 'Built to Spill'),
        ('title', 'Carry the Zero'),
        ('album', 'Keep it Like A Secret'),
        ])
    def test_parses_track_attributes(self, parser, key, value):
        assert parser['tracks'][0][key] == value


class TestSpinitronParser:
    ATTRIBUTES = ['title', 'station', 'dj', 'datetime', 'tracks']

    @pytest.mark.parametrize('attribute', ATTRIBUTES)
    def test_parses_v1_page(self, spinitron_v1, attribute):
        parser = parsers.SpinitronParser(spinitron_v1)
        v1_parser = parsers.SpinitronV1Parser(spinitron_v1)
        assert parser[attribute] == v1_parser[attribute]

    @pytest.mark.parametrize('attribute', ATTRIBUTES)
    def test_parses_v2_page(self, spinitron_v2, attribute):
        parser = parsers.SpinitronParser(spinitron_v2)
        v2_parser = parsers.SpinitronV2Parser(spinitron_v2)
        assert parser[attribute] == v2_parser[attribute]

    def test_raises_error_for_non_spinitron_content(self, wkdu):
        with pytest.raises(ValueError):
            parsers.SpinitronParser(wkdu)


class TestParseEpisode:
    def test_parses_content(self, spinitron_v1):
        result = parsers.parse_episode('spinitron.com', spinitron_v1)
        assert result['title'] == 'Ruckus Radio'

    def test_refuses_unconfigured_domains(self):
        with pytest.raises(KeyError):
            parsers.parse_episode('unknown.com', '<html />')
