#!/usr/bin/env python3
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv
from typing import List, Dict, Type, Any

from media_tools.util import (
    Commands, DuplicateStringRemover, ExtensionLowercaser, JunkRemover, NumberingFixer,
    SymlinkFixer, UndoCommands
)
from media_tools.util.logging import setup_logging

UNDO_DATABASE_FILE = '~/.music-rename-undo.pickle'


class FilenameCleaner:

    def __init__(
            self, basedir: str, force: bool, undo_db: str = UNDO_DATABASE_FILE
    ) -> None:
        self._base_directory = Path(basedir)
        self._force = force
        self._undo_db = Path(undo_db).expanduser()
        self._undo_info = self._load_undo_info(self._undo_db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with open(self._undo_db, 'wb') as db_file:
            return pickle.dump(self._undo_info, db_file)

    def clean_filenames(self, min_length: int = 0, recurse: bool = False) -> None:
        self._execute_fix_commands(
            self._get_fix_commands(DuplicateStringRemover, min_length=min_length, recurse=recurse)
        )

    def clean_numbering(self) -> None:
        self._execute_fix_commands(self._get_fix_commands(NumberingFixer))

    def clean_junk(self) -> None:
        self._execute_fix_commands(self._get_fix_commands(JunkRemover))

    def undo(self) -> None:
        self._execute_fix_commands(self._get_fix_commands(UndoCommands, undo_info=self._undo_info))

    def fix_symlinks(self) -> None:
        self._execute_fix_commands(self._get_fix_commands(SymlinkFixer, undo_info=self._undo_info))

    def lowercase_exts(self) -> None:
        self._execute_fix_commands(
            self._get_fix_commands(ExtensionLowercaser)
        )

    def _get_fix_commands(self, cleaner_class: Type, **kwargs: Any) -> Commands:
        cleaner = cleaner_class(self._base_directory)
        return cleaner.fix_commands(**kwargs)

    def _execute_fix_commands(self, fix_commands: Commands) -> None:
        for fix_command in [f for f in fix_commands if f[0] is not None]:
            self._undo_info[fix_command.source] = fix_command.destination
            fix_command.execute(self._force)

        logging.info('%s fixed', len(fix_commands))

    @staticmethod
    def _load_undo_info(undo_db: Path) -> Dict[str, str]:
        try:
            with open(undo_db, 'rb') as db_file:
                return pickle.load(db_file)
        except (FileNotFoundError, EOFError):
            return {}


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description='Perform several operations to remove junk from music file names'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true'
    )
    parser.add_argument('-f', '--force', action='store_true', help='Force rename files')

    subparsers = parser.add_subparsers(help='Available subcommands:', required=True)

    parser_filenames = subparsers.add_parser(
        'clean-filenames', help='Remove longest common substring from music files in this dir'
    )
    parser_filenames.add_argument(
        '-r', '--recurse', action='store_true', help='Scan subdirectories recursively'
    )
    parser_filenames.add_argument(
        '--min-length', type=int, default=5, help='Minimum length for common substring'
    )
    parser_filenames.set_defaults(execute=clean_filenames)

    parser_numbering = subparsers.add_parser(
        'clean-numbering', help='Let music files start with "%%d - "'
    )
    parser_numbering.set_defaults(execute=clean_numbering)
    parser_junk = subparsers.add_parser('clean-junk', help='Remove junk from filenames')
    parser_junk.set_defaults(execute=clean_junk)
    parser_symlinks = subparsers.add_parser(
        'fix-symlinks', help='Fix symlinks broken by earlier cleaning steps'
    )
    parser_symlinks.set_defaults(execute=fix_symlinks)
    parser_lowercase = subparsers.add_parser('lowercase-exts', help='make all extensions lowercase')
    parser_lowercase.set_defaults(execute=lowercase_exts)
    parser_undo = subparsers.add_parser('undo', help='Undo a change on the target directory')
    parser_undo.set_defaults(execute=undo)

    parser.add_argument('target', type=str)
    return parser.parse_args(args)


def clean_filenames(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.clean_filenames(min_length=opts.min_length, recurse=opts.recurse)


def clean_numbering(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.clean_numbering()


def clean_junk(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.clean_junk()


def fix_symlinks(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.fix_symlinks()


def lowercase_exts(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.lowercase_exts()


def undo(opts: Namespace):
    with FilenameCleaner(opts.target, force=opts.force) as cleaner:
        cleaner.undo()


def main() -> None:
    opts = parse_commandline(argv[1:])
    setup_logging(opts)
    opts.execute(opts)


if __name__ == '__main__':
    main()
