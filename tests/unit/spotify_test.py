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
