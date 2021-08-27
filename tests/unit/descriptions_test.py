import datetime
import pytest
from unittest.mock import patch
from spin2spot import descriptions

title = 'Spin Cycle'
dt = datetime.datetime(2021, 8, 27, 9)
date = datetime.datetime(2021, 8, 27)
station = 'WERA'
dj = 'Lauree'
venue = 'TV Eye'

today = datetime.datetime(2013, 10, 1)


@pytest.mark.parametrize('parser, expected', [
    ({'venue': venue}, 'At TV Eye'),
    ({'datetime': dt, 'station': station, 'dj': dj}, 'Friday at 9:00am on WERA with Lauree'),
    ({'datetime': date, 'station': station, 'dj': dj}, 'Friday on WERA with Lauree'),
    ({'datetime': dt, 'station': station}, 'Friday at 9:00am on WERA'),
    ({'datetime': dt, 'dj': dj}, 'Friday at 9:00am with Lauree'),
    ({'station': station, 'dj': dj}, 'On WERA with Lauree'),
    ({'station': station}, 'On WERA'),
    ({'dj': dj}, 'With Lauree'),
    ({}, ''),
    ])
def test_builds_playlist_description_from_parser(parser, expected):
    assert descriptions.playlist_description(parser) == expected


@patch('spin2spot.descriptions.today', lambda *args, **kwargs: today)
@pytest.mark.parametrize('parser, expected', [
    ({'title': title, 'datetime': dt}, 'Spin Cycle: August 27, 2021'),
    ({'title': title}, 'Spin Cycle'),
    ({'datetime': dt}, 'August 27, 2021'),
    ({}, 'October 01, 2013'),
    ])
def test_builds_playlist_title_from_parser(parser, expected):
    assert descriptions.playlist_title(parser) == expected
