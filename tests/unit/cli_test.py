import pytest
from spin2spot import cli


class TestParseArgs:
    @pytest.fixture
    def parse(self):
        return cli.parse_args

    @pytest.mark.parametrize('urls', [
        ['url'],
        ['url1', 'url2', 'url3'],
        ])
    def test_parses_urls(self, parse, urls):
        args = urls
        assert parse(args)['urls'] == urls

    def test_requires_urls(self, parse):
        with pytest.raises(SystemExit):
            parse([])

    @pytest.mark.parametrize('flag', ['-p', '--public'])
    def test_parses_public(self, parse, flag):
        args = ['url', flag]
        assert parse(args)['public'] is True

    def test_defaults_as_private(self, parse):
        args = ['url']
        assert parse(args)['public'] is False

    @pytest.mark.parametrize('flag', ['-u', '--user'])
    def test_parses_username(self, parse, flag):
        args = [flag, 'username', 'url']
        assert parse(args)['username'] == 'username'

    def test_defaults_username_as_none(self, parse):
        args = ['url']
        assert parse(args)['username'] is None
