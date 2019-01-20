# spin2spot
Creates Spotify playlists from Spinitron playlists.

## Quick Start
You can use `spin2spot` as a command-line tool:

```
erik@ubuntu:~$ python -m spin2spot https://spinitron.com/WZBC/pl/50067/7DayWknd https://wkdu.org/playlist/32880
Created 2 playlists for user erikcdidriksen.
```

You can also use `spin2spot` in Python directly:

```
from spin2spot import build_client, create_playlist

client = build_client('username')
create_playlist(client, 'http://spinitron.com/radio/playlist.php?station=kwva&playlist=20955')
```

## Prerequsities
In order to use `spin2spot`, you must have the [environment variables set up for `spotipy` as described in their documentation](https://spotipy.readthedocs.io/en/latest/#authorization-code-flow).

## Command-line flags
`spin2spot` accepts URLs as positional arguments. It also takes two optional arguments:

* `-p` or `--public` makes the new playlist public.
* `-u USERNAME` or `--user USERNAME` specifies the Spotify username to use. If it is not provided, it will default to the contents of the `SPIN2SPOT_USERNAME` environment variable.

## Dependencies
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Dateutil](https://github.com/dateutil/dateutil)
- [Requests](https://github.com/kennethreitz/requests)
- [Spotipy](https://github.com/plamere/spotipy)
