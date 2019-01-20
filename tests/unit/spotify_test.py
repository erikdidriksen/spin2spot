import pytest
import fixtures
from spin2spot import spotify


class TestGetUsername:
    def test_returns_provided_username(self):
        assert spotify.get_username('provided') == 'provided'

    def test_returns_environment_username(self):
        assert spotify.get_username() == 'username'

    def test_raises_error_if_no_username_available(self, mock_os):
        mock_os.get.return_value = None
        with pytest.raises(ValueError):
            spotify.get_username()


class TestBuildClient:
    @pytest.fixture(autouse=True)
    def client(self):
        return spotify.build_client()

    def test_builds_auth_token_correctly(self, mock_util):
        mock_util.prompt_for_user_token.assert_called_with(
            'username',
            scope='playlist-modify-private playlist-modify-public',
            )

    def test_builds_spotipy_client_correctly(self, mock_spotipy, mock_util):
        auth = mock_util.prompt_for_user_token.return_value
        mock_spotipy.assert_called_with(auth=auth)

    def test_returns_spotipy_client(self, client, mock_spotipy):
        assert client == mock_spotipy.return_value


class TestGetTrackID:
    @pytest.fixture
    def track(self):
        return {
            'artist': 'The Courtneys',
            'title': 'Lost Boys',
            'album': 'Lost Boys',
            }

    def test_queries_spotify_correctly(self, mock_client, track):
        spotify.get_track_id(mock_client, track)
        mock_client.search.assert_called_with(
            q='artist:"The Courtneys" track:"Lost Boys"',
            )

    def test_returns_none_if_no_match(self, track, mock_client):
        mock_client.search.return_value = fixtures.json('search_empty.json')
        assert spotify.get_track_id(mock_client, track) is None

    def test_returns_matching_album(self, track, mock_client):
        expected = '4IssUgVW7mVUedc4agB4iW'
        assert spotify.get_track_id(mock_client, track) == expected

    def test_returns_first_if_no_matching_album(self, track, mock_client):
        track['album'] = 'Live @ Warsaw, 2018/12/01'
        expected = '6Ck7eSqoon2ZHIQZuYAlLf'
        assert spotify.get_track_id(mock_client, track) == expected
