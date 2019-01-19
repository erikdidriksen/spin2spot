from bs4 import BeautifulSoup


def ensure_is_soup(html):
    """Ensures the incoming HTML is parsed as a BeautifulSoup object."""
    if isinstance(html, BeautifulSoup):
        return html
    return BeautifulSoup(html, 'html.parser')
