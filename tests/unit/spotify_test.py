import pytest
import fixtures
from spin2spot import parsers
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


class TestFormatQuery:
    @pytest.mark.parametrize('string, expected', [
        ('1 Samuel 15:23', '1 Samuel 15:23'),
        ('5-4=Unity', '5-4=Unity'),
        ('Avenues & Alleyways', 'Avenues  Alleyways'),
        ('Earth A.D.', 'Earth A.D.'),
        ('Kiwi Maddog 20/20', 'Kiwi Maddog 20/20'),
        ('Neighborhood #1 (Tunnels)', 'Neighborhood #1 Tunnels'),
        ('One last "Whoo-hoo!" for the Pullman', 'One last Whoo-hoo for the Pullman'),
        ("Scott Get the Van, I'm Moving", 'Scott Get the Van, Im Moving'),
        ("Scott Get the Van, I’m Moving", 'Scott Get the Van, Im Moving'),
        ('Two-Headed Boy', 'Two-Headed Boy'),
        ("What's My Sign Again?", 'Whats My Sign Again'),
        ])
    def test_reformats_strings_correctly(self, string, expected):
        assert spotify._format_query(string) == expected


class TestGetTrackID:
    @pytest.fixture
    def track(self):
        return {
            'artist': 'The Courtneys',
            'title': 'Lost Boys',
            'album': 'Lost Boys',
            }

    @pytest.mark.parametrize('keywords, expected', [
        (
            {'artist': 'Future Teens', 'title': "What's My Sign Again?"},
            'artist:"Future Teens" track:"Whats My Sign Again"',
        ),
        ])
    def test_queries_spotify_correctly(self, mock_client, keywords, expected):
        spotify.get_track_id(mock_client, **keywords)
        mock_client.search.assert_called_with(q=expected)

    def test_returns_none_if_no_match(self, track, mock_client):
        mock_client.search.return_value = fixtures.json('search_empty.json')
        assert spotify.get_track_id(mock_client, **track) is None

    def test_searches_covered_artist_if_necessary(self, mock_client):
        first_search = fixtures.json('search_empty.json')
        second_search = fixtures.json('search_track.json')
        mock_client.search.side_effect = [first_search, second_search]
        track = {
            'artist': 'Runk',
            'title': 'Lost Boys',
            'cover_of': 'The Courtneys',
            }
        expected_id = '6Ck7eSqoon2ZHIQZuYAlLf'
        expected_query = 'artist:"The Courtneys" track:"Lost Boys"'
        assert spotify.get_track_id(mock_client, **track) == expected_id
        mock_client.search.assert_called_with(q=expected_query)

    def test_prefers_exact_title_match(self, mock_client):
        mock_client.search.return_value = fixtures.json('search_title.json')
        track = {'artist': 'Beach Slang', 'title': 'Kids'}
        expected = '68npV3EWVTeDjL2gEL2eq9'
        assert spotify.get_track_id(mock_client, **track) == expected

    def test_returns_matching_album(self, track, mock_client):
        expected = '4IssUgVW7mVUedc4agB4iW'
        assert spotify.get_track_id(mock_client, **track) == expected

    def test_returns_first_if_no_matching_album(self, track, mock_client):
        track['album'] = 'Live @ Warsaw, 2018/12/01'
        expected = '6Ck7eSqoon2ZHIQZuYAlLf'
        assert spotify.get_track_id(mock_client, **track) == expected


class TestCreatePlaylistFromParser:
    @pytest.fixture(scope='class')
    def parser(self, html):
        return parsers.SpinitronParser(html)

    @pytest.fixture
    def track_ids(self):
        return [
            '4A09DIPRjs4wFdfD95XhxX', '1CWYaudOeTqf6lqq0uWQ2V', None,
            '2wDcUFUBXVW52wy72cRgJk', '5HBPyQaZwIgyFKJRMYHvPH', None,
            '7pgzBbAZf04VaQVy2v0kXe', '4amS5u0OaWRC9n5XPVznsr',
            '3LueS3mbuB1yaJNN0Ale6U', '3nomqzyImYpSIycH2QdsBm',
            '2ZXsEn0metMwsRWvFdQCst', None, '2C0dQVPQ5LKNf0vq5eHKlp',
            '5dhsJkGogwoNTsINvrYhWK', '6YgBglEYdfmeY2EiX22nQO', None,
            None, '0x4bMpm2reDCqnUSPJqjA0',
            ]

    @pytest.fixture(autouse=True)
    def mock_get(self, mocker, track_ids):
        patch = mocker.patch('spin2spot.spotify.get_track_id')
        patch.side_effect = track_ids
        return patch

    def test_creates_spotify_playlist_correctly(self, mock_client, parser):
        spotify.create_playlist_from_parser(mock_client, parser)
        mock_client.user_playlist_create.assert_called_with(
            user='username',
            name='Ruckus Radio: November 10, 2015',
            public=False,
            description='Tuesday at 11:00am on KWVA with Ruckus the Red',
            )

    def test_adds_tracks_correctly(self, mock_client, parser, track_ids):
        spotify.create_playlist_from_parser(mock_client, parser)
        expected_tracks = [track for track in track_ids if track]
        mock_client.user_playlist_add_tracks.assert_called_with(
            user='username',
            playlist_id='407JxJeVQyNxgqy8hC1vTl',
            tracks=expected_tracks,
            )


class TestCreatePlaylist:
    @pytest.fixture(autouse=True)
    def mock_parse(self, mocker):
        patch = mocker.patch('spin2spot.spotify.parse_episode')
        return patch

    @pytest.fixture(autouse=True)
    def mock_create(self, mocker):
        patch = mocker.patch('spin2spot.spotify.create_playlist_from_parser')
        return patch

    @pytest.fixture(autouse=True)
    def create_playlist(self, mock_client, mock_parse, mock_create):
        spotify.create_playlist(mock_client, 'http://spinitron.com')

    def test_retrieves_episode(self, mock_requests):
        mock_requests.get.assert_called_with('http://spinitron.com')

    def test_parses_episode(self, mock_parse, html):
        mock_parse.assert_called_with('spinitron.com', html)

    def test_builds_playlist(self, mock_create, mock_client, mock_parse):
        parser = mock_parse.return_value
        mock_create.assert_called_with(mock_client, parser, public=False)
