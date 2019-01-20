import pytest
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
