import pytest
import fixtures
from spin2spot import parsers


@pytest.fixture(scope='module')
def spinitron_v1():
    return fixtures.soup('spinitron_v1.html')


class TestEnsureIsSoup:
    @pytest.fixture
    def soup(self, spinitron_v1):
        return spinitron_v1

    def test_returns_soup_for_soup(self, soup):
        assert parsers.ensure_is_soup(soup) == soup

    def test_returns_soup_for_raw_html(self, soup, html):
        assert parsers.ensure_is_soup(html) == soup
