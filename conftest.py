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
