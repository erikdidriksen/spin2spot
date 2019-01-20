import pytest
from unittest.mock import MagicMock
from tests.unit import fixtures


@pytest.fixture(scope='session')
def html():
    return fixtures.contents('spinitron_v1.html')


@pytest.fixture(autouse=True)
def mock_requests(mocker, html):
    patch = mocker.patch('spin2spot.retrieval.requests')
    patch.get.return_value.content = html
    return patch


@pytest.fixture(autouse=True)
def mock_os(mocker):
    patch = mocker.patch('spin2spot.spotify.os.environ')
    patch.get.return_value = 'username'
    return patch


@pytest.fixture(scope='session')
def playlist_create():
    return fixtures.json('playlist_create.json')


@pytest.fixture(scope='session')
def search_track():
    return fixtures.json('search_track.json')


@pytest.fixture
def mock_client(playlist_create, search_track):
    client = MagicMock()
    client.current_user.return_value = {'id': 'username'}
    client.search.return_value = search_track
    client.user_playlist_create.return_value = playlist_create
    return client


@pytest.fixture(autouse=True)
def mock_spotipy(mocker, mock_client):
    patch = mocker.patch('spin2spot.spotify.spotipy.Spotify')
    patch.return_value = mock_client
    return patch


@pytest.fixture(autouse=True)
def mock_util(mocker):
    patch = mocker.patch('spin2spot.spotify.util')
    return patch
