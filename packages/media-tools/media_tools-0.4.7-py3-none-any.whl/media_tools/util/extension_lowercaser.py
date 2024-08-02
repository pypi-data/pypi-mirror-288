__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from pathlib import Path
from typing import List

from media_tools.util.base_filename_cleaner import BaseFilenameCleaner
from media_tools.util.command import Commands, Move


class ExtensionLowercaser(BaseFilenameCleaner):

    def fix_commands(self) -> Commands:
        return [
            Move(to_lower, self.lowercased_ext(to_lower), [])
            for to_lower in self.find_uppercase_extensions()
        ]

    def find_uppercase_extensions(self) -> List[Path]:
        return [
            with_uppercase
            for with_uppercase in self.get_music_files()
            if with_uppercase.suffix.lower() != with_uppercase.suffix
        ]

    @staticmethod
    def lowercased_ext(file: Path) -> Path:
        return file.parent / Path(file.stem).with_suffix(file.suffix.lower())
