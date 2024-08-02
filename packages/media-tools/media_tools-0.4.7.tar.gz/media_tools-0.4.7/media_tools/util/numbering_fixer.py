import re
from pathlib import Path
from typing import Optional

from media_tools.util.base_filename_cleaner import BaseFilenameCleaner
from media_tools.util.command import Command, Commands, Move, Nothing
from media_tools.util.media_extensions import MEDIA_EXTENSIONS
from media_tools.util.util import find_files, log_utf8_safe


class NumberingFixer(BaseFilenameCleaner):

    # Note: The order of patterns matters. Patterns with more specific matches must come first.
    # Note: Regex will be prefixed by group for path
    PATTERNS_TO_FIX = [
        r'(\d\d)\2\s+-\s+([^/]+)',           # 0101 - blah
        r'\s*(\d{1,3}-\d)\s+([^-][^/]+)',    # 01-1 blah
        r'\s*(\d-\d{1,2})\s+([^-][^/]+)',    # 1-01 blah
        r'\s*(\d-\d{1,2})\.\s+([^-][^/]+)',  # 1-01. blah
        r'\s*(\d-\d{1,2})\.([^-][^/]+)',     # 1-01.blah
        r'\s*(\d\d-\d\d)\s+([^-][^/]+)',     # 01-01 blah
        r'\s*(\d{1,3}) – ([^/]+)',           # 01 – blah (en dash)
        r'\s*(\d{1,3})–([^/]+)',             # 01–blah (en dash)
        r'\s*(\d{1,3}) — ([^/]+)',           # 01 — blah (em dash)
        r'\s*(\d{1,3})—([^/]+)',             # 01—blah (em dash)
        r'\s*(\d{1,4})\s+([^/]+)',           # 01 blah
        r'\s*(\d{1,3})\.\s+([^/]+)',         # 01. blah
        r'\s*(\d{1,3})\.([^/]+)',            # 01.blah
        r'\s*(\d{1,3})--([^/]+)',            # 01--blah
        r'\s*(\d{1,3})-\s*(\D[^/]+)',        # 01-blah or 01- blah
        r'\s*-(\d{1,3})-([^/]+)',            # -01-blah
        r'\s*-\s*(\d{1,3})\.\s*([^/]+)',     # - 01. blah
        r'\s*(\d{1,3})_([^/]+)',             # 01_blah
        r'\s*\[(\d{1,3})\]-([^/]+)',         # [01]-blah
        r'\s*\[(\d{1,3})\]\s+([^/]+)',       # [01] blah, [01]  blah, ...
        r'\s*\[(\d{1,3})\]([^/]+)',          # [01]blah
        r'\s*(\d{1,3})\]-([^/]+)',           # 01]-blah
        r'\s*(\d{1,3})\]([^/]+)',            # 01]blah
        r'\s*\((\d{1,3})\)\s*([^/]+)',       # (01)blah
        r'\s*(\d{1,4})(\D[^/]*)',            # 01blah
        r'\s*([a-z]\d{1,2})\s+([^/]+)',      # a1 blah
        r'\s*([a-z]\d)-([^/]+)',             # a1-blah
        r'\s*([a-z]\d)\.([^/]+)',            # a1.blah
        r'\s*\[([a-z]\d)\]-([^/]+)',         # [a1]-blah
        r'\s*\[([a-z]\d)\]([^/]+)',          # [a1]blah
        r'\s*([a-z]\d)\]-([^/]+)',            # a1]-blah
        r'\s*([a-z]\d)\]([^/]+)',            # a1]blah
        r'\s*\(([a-z]\d)\)([^/]+)',          # (a1)blah
        r'\s*([a-z]\d{1,2})(\D[^/]+)',       # a1blah
    ]
    PATTERNS_TO_FIX_2 = [
        r'\s*(\d) - (\d{1,2})\.\s*([^-][^/]+)',    # 1 - 01. blah, 1 - 01.blah
        r'\s*(\d) - (\d{1,2})\s*-\s*([^-][^/]+)',  # 1 - 01-blah, 1 - 01 - blah
        r'\s*(\d)\.(\d{1,2})\s*-*\s*([^-][^/]+)',  # 1.01 blah, 1.01-blah, 1.01 - blah,
        r'\s*(\d)-(\d{1,2})\.\s*([^-][^/]+)',      # 1-01.blah, 1-01. blah
        r'\s*(\d)-(\d{1,2})\s*-*\s*([^-][^/]+)',   # 1-01-blah, 1-01 - blah
    ]

    def fix_commands(self) -> Commands:
        def has_screwy_numbering(filename: Path) -> bool:
            base = self.filename_base(filename)
            return self.is_music_file(filename) and bool(
                re.search(r'\d+', base) and
                not re.search(r'^\d{1,4} - [^/]+', base, flags=re.IGNORECASE) and
                not re.search(r'^\d{1,4}$', base, flags=re.IGNORECASE) and
                not re.search(r'^\d{1,2}-\d{1,2}$', base, flags=re.IGNORECASE) and
                not re.search(r'^\d{1,2}-\d{1,2} - [^/]+', base, flags=re.IGNORECASE) and
                not re.search(r'^[a-z]\d{1,2} - [^/]+', base, flags=re.IGNORECASE) or
                re.search(r'^(\d\d)\1 - [^/]+', base, flags=re.IGNORECASE) or
                re.search(r'^\d - \d\d.\s*[^/]+', base, flags=re.IGNORECASE) or
                re.search(r'^\d - \d\d\s*-\s*[^/]+', base, flags=re.IGNORECASE) or
                re.search(r'\d{1,4}\s?–', base, flags=re.IGNORECASE) or
                re.search(r'\d{1,4}\s?—', base, flags=re.IGNORECASE)
            )

        mismatches = sorted(find_files(self._base_directory, has_screwy_numbering))
        return [self._fix_numbering_for_file(file) for file in mismatches]

    def _fix_numbering_for_file(self, file: Path) -> Command:
        for extension in MEDIA_EXTENSIONS:
            result = self._may_fix_numbering_for_file_and_extension(str(file), extension)
            if result is not None:
                return result
        log_utf8_safe('-' * 8, file)
        return Nothing()

    def _may_fix_numbering_for_file_and_extension(
            self, filename: str, extension: str
    ) -> Optional[Command]:
        # just a number - do not change
        if re.match(r'(.*)/(\d{1,4})\.' + extension, filename, flags=re.IGNORECASE):
            return Nothing()
        # CD id, track number and track name
        for pattern in self.PATTERNS_TO_FIX_2:
            match = re.search(
                '(.*)/' + pattern + r'\.' + extension, filename, flags=re.IGNORECASE
            )
            if match:
                return Move(
                    Path(filename),
                    Path(match.group(1)) /
                    Path(f'{match.group(2)}-{match.group(3)} - {match.group(4)}.{extension}'),
                    [pattern]
                )
        # track number and track name
        for pattern in self.PATTERNS_TO_FIX:
            match = re.search(
                '(.*)/' + pattern + r'\.' + extension, filename, flags=re.IGNORECASE
            )
            if match:
                print(match.groups(), pattern)
                return Move(
                    Path(filename),
                    Path(f'{match.group(1)}/{match.group(2)} - {match.group(3)}.{extension}'),
                    [pattern]
                )
        return None
