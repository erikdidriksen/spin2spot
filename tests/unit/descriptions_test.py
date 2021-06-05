import pytest
import fixtures
from spin2spot import descriptions, parsers


setlist_fm = parsers.SetlistFMParser(fixtures.soup('setlist_fm.html'))
spinitron = parsers.SpinitronParser(fixtures.soup('spinitron_v2.html'))
wkdu = parsers.WKDUParser(fixtures.soup('wkdu.html'))
wprb = parsers.WPRBParser(fixtures.soup('wprb.html'))


@pytest.mark.parametrize('parser, expected', [
    (setlist_fm, 'At Brooklyn Bowl, Brooklyn, NY, USA'),
    (spinitron, 'Tuesday at 2:00pm on WZBC 90.3 FM Newton with Nick'),
    (wkdu, 'Tuesday on WKDU with Matt'),
    (wprb, 'Tuesday at 2:00pm on WPRB with Bad Newz'),
    ])
def test_builds_playlist_description_from_parser(parser, expected):
    assert descriptions.playlist_description(parser) == expected


@pytest.mark.parametrize('parser, expected', [
    (setlist_fm, 'The Lemonheads: May 04, 2019'),
    (spinitron, '7DayWknd: August 02, 2016'),
    (wkdu, 'The New Matt Show: October 01, 2013'),
    (wprb, 'Ruckus Radio: November 10, 2015'),
    ])
def test_builds_playlist_title_from_parser(parser, expected):
    return descriptions.playlist_title(parser) == expected
