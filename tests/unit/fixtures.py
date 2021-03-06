import json as json_
import os
from bs4 import BeautifulSoup


def fixture_folder():
    """Returns the absolute path of the fixtures folder."""
    folder = os.path.dirname(__file__)
    return os.path.join(folder, os.pardir, 'fixtures')


def fixture_path(filename):
    """Returns the absolute path of the given fixture file."""
    folder = fixture_folder()
    return os.path.join(folder, filename)


def contents(filename):
    """Returns the contents of the given fixture file."""
    path = fixture_path(filename)
    with open(path, 'r') as fixture_file:
        return fixture_file.read()


def json(filename):
    """Returns the parsed contents of the given JSON fixture file."""
    content = contents(filename)
    return json_.loads(content)


def soup(filename):
    """Returns a BeautifulSoup object from the given fixture file."""
    content = contents(filename)
    return BeautifulSoup(content, 'html.parser')
