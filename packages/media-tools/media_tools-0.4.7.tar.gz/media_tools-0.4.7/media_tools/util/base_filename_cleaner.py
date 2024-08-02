from pathlib import Path
from typing import List

from media_tools.util.media_extensions import MEDIA_EXTENSIONS


class BaseFilenameCleaner:

    def __init__(self, basedir: Path) -> None:
        self._base_directory = basedir

    def get_music_files(self) -> List[Path]:
        return sorted(
            [
                f for f in Path(self._base_directory).iterdir()
                if f.is_file() and self.is_music_file(f)
            ]
        )

    @staticmethod
    def is_music_file(filename: Path) -> bool:
        return any(
            filename.name.upper().endswith(e.upper()) for e in MEDIA_EXTENSIONS
        )

    @staticmethod
    def filename_base(file: Path) -> str:
        return file.stem
