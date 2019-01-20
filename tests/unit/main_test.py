import pytest
from spin2spot import __main__ as main


class TestRunModule:
    @pytest.fixture(autouse=True)
    def mock_create(self, mocker):
        patch = mocker.patch('spin2spot.__main__.create_playlist')
        return patch

    @pytest.fixture(autouse=True)
    def mock_print(self, mocker):
        patch = mocker.patch('builtins.print')
        return patch

    def test_creates_playlists_correctly(self, mock_create, mock_client):
        main.run_module(['url'])
        mock_create.assert_called_with(mock_client, 'url', public=False)

    def test_creates_playlists_for_all_urls(self, mock_create):
        main.run_module(['url', 'url'])
        assert mock_create.call_count == 2

    def test_returns_stdout_message(self, mock_print):
        main.run_module(['url'])
        mock_print.assert_called_with('Created 1 playlist for user username.')
