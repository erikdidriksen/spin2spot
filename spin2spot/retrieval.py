import requests
import urllib.parse


def parse_domain(url):
    """Returns the domain name for the given URL."""
    parsed_url = urllib.parse.urlparse(url)
    if not parsed_url.netloc:
        parsed_url = urllib.parse.urlparse('http://' + url)
    domain = parsed_url.netloc
    domain = domain.split('.')[-2:]  # remove subdomains
    return '.'.join(domain)


def retrieve_episode_html(url):
    """Retrieves the HTML for the given episode playlist URL."""
    response = requests.get(url)
    return response.content


def retrieve_episode(url):
    """Returns the domain and HTML for the given playlist URL."""
    domain = parse_domain(url)
    html = retrieve_episode_html(url)
    return domain, html
