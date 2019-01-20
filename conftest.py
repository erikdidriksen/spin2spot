import pytest
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


@pytest.fixture(autouse=True)
def mock_spotipy(mocker):
    patch = mocker.patch('spin2spot.spotify.spotipy.Spotify')
    return patch


@pytest.fixture(autouse=True)
def mock_util(mocker):
    patch = mocker.patch('spin2spot.spotify.util')
    return patch
