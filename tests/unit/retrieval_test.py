import pytest
from spin2spot import retrieval


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
