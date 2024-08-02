__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import List, Dict, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter, Retry
from pydub import AudioSegment
from tinytag import TinyTag

from media_tools.util.mixcloud.constants import (
    DEFAULT_CROSSFADE_MS, DEFAULT_MAX_RETRY, MP3_KBIT_RATE, MIXCLOUD_API_UPLOAD_URL,
    MIXCLOUD_MAX_TAGS, ALLOWED_TRACKS_PER_ARTIST
)
from media_tools.util.mixcloud.mix_path import MixPath


@dataclass
class RetryOptions:
    max_retry: int = DEFAULT_MAX_RETRY
    backoff_factor: float = 0.5
    status_codes: Tuple[int, ...] = (504, 503, 502, 429, 400, 403)


class Mix:  # pylint: disable=too-many-instance-attributes

    def __init__(
            self, mix_path: MixPath, strict: bool = False, crossfade_ms: int = DEFAULT_CROSSFADE_MS,
            part: Optional[int] = None
    ) -> None:
        self._mix_path = mix_path
        self._strict = strict
        self._crossfade_ms = crossfade_ms
        self._incomplete = False
        self._track_info: List[Dict] = []
        self._title: Optional[str] = None
        self._access_token: Optional[str] = None
        self._part: Optional[int] = part
        if self._strict and not self._mix_path.audio_files:
            raise ValueError(f'no audio files in {self._mix_path.basedir}')
        self._audio = self._import_audio(self._mix_path.audio_files)

    def with_access_token(self, access_token: str) -> 'Mix':
        self._access_token = access_token
        return self

    def with_title(self, title: str) -> 'Mix':
        self._title = title
        return self

    @property
    def valid(self):
        return not self._incomplete

    @property
    def tags(self) -> List[str]:
        tags = self._mix_path.tags
        error = self.check_tag_validity(tags)
        if error:
            self.raise_error(error)
        return tags

    def raise_error(self, error: str) -> None:
        self._incomplete = True
        if self._strict:
            raise ValueError(error)
        logging.warning(error)

    @staticmethod
    def check_tag_validity(tags: List[str]) -> str:
        if len(tags) > MIXCLOUD_MAX_TAGS:
            return f'Max. {MIXCLOUD_MAX_TAGS} tags allowed, found {len(tags)}: {tags}'
        if not tags:
            return 'No tags found'
        return ''

    @property
    def title(self) -> str:
        if self._title:
            return self._title
        title = self._mix_path.title
        return f"Test - don't bother playing ({title})" if self._incomplete else title

    @property
    def description(self) -> str:
        description = self._mix_path.description
        if description:
            return description
        self.raise_error('No description found')
        return ''

    @property
    def picture(self) -> Optional[Path]:
        """Currently just returns the first JPEG or PNG. Room for improvement!"""
        try:
            return self._mix_path.picture
        except StopIteration:
            self.raise_error(f'No picture in {self._mix_path.basedir}')
            return None

    def _import_audio(self, audio_files: List[Path]) -> AudioSegment:
        part_name = '' if self._part is None else f'_{self._part}'
        mix_file = self._mix_path.file(Path(f'mix{part_name}.mp3'))
        self._track_info = [self._get_track_info(audio_file) for audio_file in audio_files]
        self._check_tracks_per_artist_limit()
        if mix_file.exists():
            logging.info('Reading present %s', mix_file)
            return AudioSegment.from_file(mix_file)

        audio = AudioSegment.empty()
        for i, audio_file in enumerate(audio_files):
            logging.info(
                '%s: %s (%s - %s)',
                i + 1, audio_file.name, self._track_info[i]['artist'], self._track_info[i]['title']
            )
            audio = audio.append(
                self._read_track(audio_file),
                crossfade=self._crossfade_ms if len(audio) > self._crossfade_ms else len(audio)
            )

        return audio

    def _check_tracks_per_artist_limit(self) -> None:
        artists: Dict[str, int] = defaultdict(int)
        for track in self._track_info:
            artists[track['artist']] += 1
        if artists and max(artists.values()) > ALLOWED_TRACKS_PER_ARTIST:
            artists_with_too_many_tracks = ', '.join([
                a for a, num in artists.items() if num > ALLOWED_TRACKS_PER_ARTIST
            ])
            self.raise_error(
                f'More than {ALLOWED_TRACKS_PER_ARTIST} tracks by: {artists_with_too_many_tracks}')

    @staticmethod
    def _read_track(audio_file):
        track = AudioSegment.from_file(audio_file)
        if track.sample_width != 2:
            track = track.set_sample_width(2)
        if track.frame_rate != 44100:
            track = track.set_frame_rate(44100)
        return track.normalize()

    def _get_track_info(self, audio_file: Path) -> Dict:
        tags = TinyTag.get(str(audio_file))
        if tags.artist is None or tags.title is None:
            self.raise_error(f'Incomplete tags for {audio_file}')
            return {
                'artist': tags.artist or '???', 'title': tags.title or '???',
                'length': tags.duration
            }
        return {
            'artist': tags.artist, 'title': tags.title, 'length': tags.duration,
            'filename': audio_file.name
        }

    def export(self, name: Path = Path('mix.mp3')) -> None:
        mix_file = self._mix_path.file(name)
        if mix_file.exists():
            logging.info('Mix already exported as %s', mix_file)
            return
        audio_format = name.suffix[1:]
        logging.info(
            'Exporting %s audio to %s with bitrate %s kbps',
            self.mix_length(), mix_file, MP3_KBIT_RATE
        )
        self._audio.export(
            mix_file, format=audio_format, parameters=['-q:a', '0'], bitrate=f'{MP3_KBIT_RATE}k'
        )

    def upload(self, name: Path = Path('mix.mp3'), max_retry: int = DEFAULT_MAX_RETRY) -> None:
        mix_file = self._mix_path.file(name)
        if not mix_file.exists():
            raise FileNotFoundError(mix_file)
        files = {
            'mp3': (str(name), mix_file.open('rb'), 'audio/mpeg'),
        }
        if self.picture:
            picture_type = self.picture.suffix
            files['picture'] = (
                'picture' + picture_type, self.picture.open('rb'),
                f'image/{"png" if picture_type == ".png" else "jpeg"}'
            )

        data = {
            'name': self.title,
            'description': self.description,
            'percentage_music': 100
        }
        self._add_tags(data)
        self._add_track_info(data)
        size_bytes = mix_file.stat().st_size + self.picture.stat().st_size if self.picture else 0
        logging.info(
            'Uploading %s kBytes (%s) as %s',
            f'{size_bytes // 1024:,d}', self.mix_length(), self.title
        )
        self._do_upload(name, files, data, max_retry)

    def mix_length(self) -> str:
        return f'{len(self._audio) // 60000}:{len(self._audio) % 60000 // 1000:02}'

    def _do_upload(self, name: Path, files: Dict, data: Dict, max_retry: int):
        if max_retry < 0:
            logging.error('Out of retries, aborting upload attempt')
            sys.exit(1)

        url = MIXCLOUD_API_UPLOAD_URL + '/?access_token=' + self._access_token
        logging.info(
            'Uploading to %s, max. %s retries',
            url.replace(self._access_token, '<REDACTED>'), max_retry
        )
        try:
            response = self._send_request(
                url, files=files, data=data, retry_options=RetryOptions(max_retry=max_retry)
            )
        except requests.exceptions.ConnectionError as error:
            logging.error(error)
            sys.exit(1)
        else:
            if self.is_rate_limited(response):
                logging.info(self.response_message(response))
                sleep(int(response.json().get('error', {}).get('retry_after', 60)))
                self._do_upload(name, files=files, data=data, max_retry=max_retry - 1)
            elif response.status_code == 200:
                logging.info(self.response_message(response))
                sys.exit(0)
            else:
                logging.error(self.response_message(response))
                sys.exit(1)

    @staticmethod
    def _send_request(
            url: str, files: Dict, data: Dict, retry_options: RetryOptions = RetryOptions()
    ) -> requests.Response:
        sess = requests.Session()
        retries = Retry(
            total=retry_options.max_retry, backoff_factor=retry_options.backoff_factor,
            status_forcelist=retry_options.status_codes
        )
        sess.mount('https://', HTTPAdapter(max_retries=retries))
        return sess.post(url, data=data, files=files)

    @staticmethod
    def is_rate_limited(response: requests.Response) -> bool:
        return (response.status_code == 403 and
                response.json().get('error', {}).get('type') == 'RateLimitException')

    @staticmethod
    def response_message(response: requests.Response) -> str:
        if response.status_code == 200:
            return f"{response.status_code}: {response.json()['result']['message']}"
        return f"{response.status_code}: {response.json()['error']}"

    @staticmethod
    def connection_error_message(error: requests.exceptions.ConnectionError, max_retry: int) -> str:
        message = Mix.error_args_message(error)
        if max_retry > 0:
            return f"{message} Retrying {max_retry} time{'s' if max_retry > 1 else ''}."
        return f'{message} Giving up.'

    @staticmethod
    def error_args_message(error: requests.exceptions.ConnectionError) -> str:
        if not error.args:
            return ''
        if error.args[0].args and len(error.args[0].args) > 1:
            return f'{error.args[0].args[1].args[1]}: {error.args[0].args[0]} '
        return ', '.join(str(arg) for arg in error.args)

    def _add_tags(self, data: Dict) -> None:
        for i, tag in enumerate(self.tags):
            data[f'tags-{i}-tag'] = tag

    def _add_track_info(self, data: Dict) -> None:
        start_time = 0
        for i, track_info in enumerate(self._track_info):
            data[f'sections-{i}-artist'] = track_info['artist']
            data[f'sections-{i}-song'] = track_info['title']
            data[f'sections-{i}-start_time'] = int(start_time)
            start_time += (track_info['length'] - self._crossfade_ms / 1000)
