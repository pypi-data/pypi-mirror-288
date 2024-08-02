import logging
from pathlib import Path
from shutil import move
from typing import Any, List, NamedTuple

from .util import log_utf8_safe


class Command(NamedTuple):
    src: Path = None
    dest: Path = None
    info: List[Any] = []

    @property
    def source(self) -> str:
        return str(self.src.resolve())

    @property
    def destination(self) -> str:
        return str(self.dest.resolve())

    @property
    def tilde_src(self) -> str:
        return self.tilde(self.source)

    @property
    def tilde_dest(self) -> str:
        return self.tilde(self.destination)

    def execute(self, force: bool) -> None:
        if force:
            self.do_execute()
        self.print()

    def print(self) -> None:
        raise NotImplementedError()

    def do_execute(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def tilde(path: str) -> str:
        return path.replace(str(Path.home()), '~')


class Nothing(Command):
    def do_execute(self) -> None:
        pass

    def print(self) -> None:
        pass


class Move(Command):
    def do_execute(self) -> None:
        try:
            move(self.source, self.destination)
        except FileNotFoundError:
            log_utf8_safe('FAIL:', self.tilde_src, '->', self.tilde_dest)

    def print(self) -> None:
        logging.info('mv %s %s # %s', self.tilde_src, self.tilde_dest, self.info)


class Relink(Command):
    @property
    def new_symlink(self) -> Path:
        return self.src.parent.joinpath(self.dest.name)

    @property
    def tilde_new_symlink(self) -> str:
        return self.tilde(str(self.new_symlink))

    def do_execute(self) -> None:
        self.src.unlink()
        self.new_symlink.symlink_to(self.dest)

    def print(self) -> None:
        logging.info('rm -f %s', self.tilde_src)
        logging.info('ln -s %s %s', self.tilde_dest, self.tilde_new_symlink)


Commands = List[Command]
