import setuptools


setuptools.setup(
    name='spin2spot',
    version='1.0.0',
    description='Creates Spotify playlists from Spinitron playlists',
    author='Erik Didriksen',
    packages=setuptools.find_packages(exclude=['ez_setup', 't', 't.*']),
    dependency_links=[
        'git+https://git@github.com/plamere/spotipy.git@master#egg=spotipy'
        ],
    install_requires=[
        'bs4',
        'python-dateutil',
        'requests',
        'spotipy',
        ],
    )
