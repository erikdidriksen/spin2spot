import os


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
