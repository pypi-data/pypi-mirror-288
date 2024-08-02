-   [Installation](#installation)
-   [Usage](#usage)
    -   [`mixcloud`](#mixcloud)
        -   [Authorization](#authorization)
        -   [Configuration options](#configuration-options)
    -   [`clean_filenames`](#clean_filenames)
        -   [Checking results](#checking-results)
    -   [Audacious playlist tools](#audacious-playlist-tools)
        -   [`copy_from_playlist`](#copy_from_playlist)
    -   [`buy_most_played`](#buy_most_played)
    -   [`backup_lastfm_data`](#backup_lastfm_data)
    -   [`print_length`](#print_length)
-   [Development](#development)
    -   [Test suite](#test-suite)
    -   [Generating a Table of Contents to
        `README.md`](#generating-a-table-of-contents-to-readme.md)

Toolbox for helping creating and managing playlists, and managing the filenames and directory
structure for large numbers of music files.

This is mostly tailored to my own usage patterns, although it may be useful to others.

Home page: https://gitlab.com/lilacashes/music-library-tools

PyPI page: https://pypi.org/project/media-tools

Installation
============

``` {.bash}
$ pip install media-tools
```
This will install the commands `mixcloud`, `buy_most_played`, `clean_filenames`,
`backup_lastfm_data`, `copy_from_playlist` and `print_length`.

Usage
=====

`mixcloud`
-----------------

The `mixcloud` command enables you to use the Mixcloud API to publish mixes.

### `mixcloud upload`: Creating a mix

Generate a mix on [Mixcloud](mixcloud.com) from the contents of a local directory.

Assumes that the given directory contains a number of audio files as well as a picture file (JPEG or
PNG format), one file called `description.txt` which contains the description which is printed along
with the mix on Mixcloud, and a file called `tags.txt` which contains a newline-separated list of
tags for the mix. The mix is created as an audio file called `mix.mp3` in the given directory and
then uploaded to Mixcloud. The title of the mix on Mixcloud will be the name of the directory given,
minus any leading numbers.

**Example:** You have a directory structured like this:

    10 - My awesome mix
    |-- 01 - Awesome track.mp3
    |-- 02 - Also awesome track.ogg
    |-- 03 - Another pretty cool track.m4a
    |-- 04 - This track rocks.flac
    |-- cover.png
    |-- description.txt
    |-- tags.txt

``` {.shell}
$ mixcloud upload -d "10 - My awesome mix"
```
will upload this mix to Mixcloud under the name "My awesome mix" with track 01 to 04 in that order.
Prefixing the tracks with numbers is not necessary, but helpful to ensure the tracks are in the
desired order.

#### Options

- `-d DIRECTORY`, `--directory DIRECTORY`: Specify the folder containing the mix, as seen in the
    example above
- `-e EXTENSION [EXTENSION ...]`, `--extensions EXTENSION [EXTENSION ...]`: List of file extensions
    to consider as audio files for the mix. Per default, files ending in `.mp3`, `.MP3`, `.flac`,
    `.m4a` and `.ogg` are treated as audio and added to the mix. Change this list if any of your
    audio files have extensions that are not part of this list, or if you want to exclude any of
    these extensions.
- `-q`, `--quiet`: Only errors are printed. Usually you want to omit `-q`, since the entire
    generating and uploading process takes several minutes, so you want to be informed of what is
    going on.
- `-s`, `--strict`: Do not upload the mix if any of these conditions are met:
    -   There is no picture, no `descriptions.txt` or no `tags.txt` in the upload folder
    -   Any of the audio tracks in the folder is missing the ID3 tag for title or artist. These tags
        are needed to generate the tracklist for the mix.
- `-c CROSSFADE_MS`, `--crossfade-ms CROSSFADE_MS`: Number of milliseconds to use for crossfading
    between two tracks. Currently, there can only be one global value which is used between all
    tracks.
- `-r MAX_RETRY`, `--max-retry MAX_RETRY`: Maximum number of retries for failing uploads. Uploads
    can fail for a number of reasons, such as rate limiting on the Mixcloud side, or because of a
    bad internet connection. The default number of retries is set to 100, set this to a lower number
    if you want to give up earlier.
- `-a TOKEN_FILE`, `--auth-token-file TOKEN_FILE`: explicitly specify the file containing the
    Mixcloud authorization token.
- `-t TOKEN_STRING`, `--auth-token-string TOKEN_STRING`: explicitly specify the Mixcloud
    authorization token as a string.
- `--description-file DESCRIPTION_FILE` The description that goes with the mix on its Mixcloud page
-   in a file
- `--description DESCRIPTION_STRING` The description that goes with the mix on its Mixcloud page as
-   a string
- `--tags-file TAGS_FILE` Tags for the mix, in a newline-separated file
- `--tags TAG_STRING [TAG_STRING ...]` Tags for the mix, space-separated
- `--picture-file PICTURE_FILE` Picture for the mix

### `mixcloud create-auth`: Create authorization with the Mixcloud API

This process takes three steps. You will need to generate an application on Mixcloud for your
Mixcloud account, authorize it to get an OAuth token and ose the OAuth token get an API access
token, as described in the
[Mixcloud API Documentation](https://www.mixcloud.com/developers/#authorization). The
`mixcloud create-auth` command guides you through the process as follows:

#### Step 1: Create a Mixcloud app
Before you start this step, ensure that you are logged in to Mixcloud on your system browser,
because you need to fill in the form that is going to open in your browser.

Then enter:
``` {.shell}
$ mixcloud create-auth --create-app
```
A window will open in your browser. Follow the instructions printed in your terminal - click on the
app name in the browser and copy the client ID for steps 2 and 3 and the client secret for step 3.

#### Step 2: Create OAuth token
Use the client ID and secret from step 1 to run
``` {.shell}
$ mixcloud create-auth --create-code --client-id CLIENT_ID
```
Again a browser window will open with a page displaying an "Authorize" button. Click it and you will
be taken to a page displaying a so-called OAuth code. Copy the code to use it in step 3.

#### Step 3: Create the Mixcloud API token
Use the code from step 2 to run
``` {.shell}
$ mixcloud create-auth --create-token --client-id CLIENT_ID \
                                      --client-secret CLIENT_SECRET \
                                      --oauth-code OAUTH_CODE
```
This will open yet another browser window showing you a token (in JSON format). Copy only the string
inside the quotes to use as token - either directly (here called <TOKEN>) or written (without any
extra spaces or newlines) to a file (here called <TOKEN_FILE>).

Afterwards you can use the generated token to upload mixes to Mixcloud with:
``` {.shell}
$ mixcloud upload --auth-token-string <TOKEN> ...
$ mixcloud upload --auth-token-file <TOKEN_FILE> ...
```
If you store this access token as `.mixcloud_access_token` in either the current directory, your
user's `$HOME` directory or under `$HOME/.config/media-tools`, that token will be used without
specifying `--auth-token-string` or `--auth-token-file`.

### Configuration options

`clean_filenames`
-----------------

In general: run a script with the `-v` option first to see what it would change. If satisfied, then
re-run it with the `-f` option to effect those changes.

Removing useless duplicate strings from filenames:

``` {.bash}
$ clean_filenames -v clean-filenames --recurse .
$ clean_filenames -f clean-filenames --recurse .
```

Changing filenames from different numbering schemes to the scheme `01 - filename.ext`:

``` {.bash}
$ clean_filenames -v clean-numbering .
$ clean_filenames -f clean-numbering .
```

Removing stray junk, such as underscores, stray dashes, and stray `[]` and `()` from filenames:

``` {.bash}
$ clean_filenames -v clean-junk .
$ clean_filenames -f clean-junk .
```

Undoing renamings done with this script, limited to a specified directory and its subfolders, or a
single file name:

``` {.bash}
$ clean_filenames -v undo .
$ clean_filenames -f undo .
# OR
$ clean_filenames -f undo ./subdir/file_name.mp3
```

Fixing symlinks to files which have been renamed by any of the previous commands:

``` {.bash}
$ clean_filenames -v fix-symlinks .
$ clean_filenames -f fix-symlinks .
```

### Checking results

Finding mp3 files which do not conform to the numbering scheme in general:

``` {.bash}
$ find . -name \*.mp3 | grep -vE '[[:digit:]]+ - .+\.mp3'
```

Finding mp3 files which have a number in their filename but do not conform to the numbering scheme,
excluding some more common use cases:

``` {.bash}
$ find . -name \*.mp3 | \
    grep -E '[[:digit:]]+[^/]+\.mp3' | \
    grep -vE '[[:digit:]]+ - .+\.mp3' | \
    grep -vE '[[:digit:]]{2}\.mp3'
```

Audacious playlist tools
------------------------

Tools for making and repairing playlists containing physical music files from audacious playlists
and the latest music files. The argument to `--playlist` defaults to the playlist currently playing
in audacious.

### `copy_from_playlist`

Copying files from the current or specified playlist (as its name in the `playlists` subdir in the
audacious configuration folder) to a specified target folder, optionally limiting the number of
files to copy to the first NUM, and optionally renaming the files to reflect the position of the
song in the playlist:

``` {.bash}
$ copy_from_playlist [-v] copy \
    [--playlist PLAYLIST_ID] \
    [--number NUM] \
    [--renumber] \
    TARGET_DIR
```

Try to find files in the current playlist which are unavailable because they have been moved, and
move them back to the place in the filesystem which is noted on the playlist (does not appear to
work currently):

``` {.bash}
$ copy_from_playlist [-v] restore \
    [--playlist PLAYLIST_ID]
```

Copy the newest files to a specified target:

``` {.bash}
$ copy_from_playlist [-v] copy-newest \
    --max-age NUM_DAYS \
    --source SOURCE_DIR \
    --target TARGET_DIR
```


`buy_most_played`
-----------------

Attempt to buy your most played tracks (in a given period) from several platforms.

### Options
- `-u USER`, `--user USER`: Last.FM username
- `-k API_KEY`, `--api-key API_KEY`: Last.FM API key
- `-l LIMIT`, `--limit LIMIT`: Maximum number of tracks to display
- `-m MIN_PLAYS`, `--min-plays MIN_PLAYS`: Minimum number of plays per track to consider buying it
- `--buy-up-to BUY_UP_TO`: When specified, repeat until this may tracks have been bought
- `-p PERIOD`, `--period PERIOD`: Period (`{overall,7day,1month,3month,6month,12month}`) from which
  to choose favorite tracks
- `-f FROM_DATE`, `--from-date FROM_DATE`: Start date of period in which most played tracks are
  considered
- `-t TO_DATE`, `--to-date TO_DATE`: End date of period in which most played tracks are considered
- `-d TRACK_DB`, `--track-db TRACK_DB`: Name of the file storing already bought tracks


`backup_lastfm_data`
--------------------

Back up Last.FM scrobbles. Output is saved in JSON format.

### Options
- `--limit N`, `-l N`: maximum number of scrobbles (most recent scrobbles first) and other entities
  (top `N` items) to back up
- `--year YEAR`, `-y YEAR`: year the data is requested for (empty for all Last.FM scrobbles)
- `--output FILE`, `-o FILE`: output file name
- `--max-retry-wait SECS`, `-m SECS`: maximum seconds to wait between requests to avoid rate
  limiting
- `--lastfm-user USER`: Last.FM user name for scrobbles to be read (defaults to environment variable
  `$PYLAST_USERNAME`)
- `--lastfm-api-key`: Last.FM API key (defaults to environment variable `PYLAST_API_KEY`)
- `--lastfm-api-secret`: Last.FM API secret (defaults to environment variable `PYLAST_API_SECRET`)


`print_length`
--------------

Given a directory of audio files, print the total playing time of that directory, optionally broken
down by subdirectory.

```shell
$ print_length [OPTIONS] TARGET_DIRECTORY
```

### Options
- `-r`/`--recursive`: print the playing time of each subdirectory, recursively descending
  subdirectories, sorted by directory playing time
- `--debug`: print lots of internal info for debugging
- `--max-debug-items N`: limit debugging output to the `N` shortest items


Development
===========

After cloning, it is recommended to set up the git hook that runs the test suite before every
`git push`:

``` {.shell}
$ cd .git/hooks
$ ln -s ../../.git_hooks/pre-push .
```

Test suite
----------

Run all in one:

``` {.shell}
$ .git_hooks/pre-push
```

Run separately:

``` {.shell}
$ poetry run mypy .
$ poetry run flake8 .
$ poetry run pylint media_tools
$ poetry run nosetests --with-coverage --cover-package=media_tools.util tests/unit
$ poetry run nosetests tests/integration
```

Generating a Table of Contents to `README.md`
---------------------------------------------

``` {.shell}
$ git add README.md
$ git commit -m 'Before ToC generation'
$ pandoc -s --columns 100 --toc --toc-depth=4 README.md -o README_toc.md
$ mv README_toc.md README.md
$ git add README.md
$ git commit -m 'After ToC generation'
```
