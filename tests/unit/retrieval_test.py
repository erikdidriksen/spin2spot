import pytest
from spin2spot import retrieval


@pytest.fixture
def url():
    return 'http://spinitron.com/radio/playlist.php?station=kwva&playlist=20955'


class TestParseDomain:
    @pytest.mark.parametrize('url', [
        'spinitron.com',
        'sub.domains.spinitron.com',
        'http://www.spinitron.com',
        'https://spinitron.com/WZBC/pl/50067/7DayWknd',
        'spinitron.com/radio/playlist.php?station=kwva&playlist=20955#here',
        ])
    def test_returns_domain(self, url):
        assert retrieval.parse_domain(url) == 'spinitron.com'


class TestRetrieveEpisodeHTML:
    @pytest.fixture
    def retrieve(self, url):
        return retrieval.retrieve_episode_html(url)

    def test_calls_requests_correctly(self, retrieve, mock_requests, url):
        mock_requests.get.assert_called_with(url)

    def test_returns_html(self, retrieve, html):
        assert retrieve == html
