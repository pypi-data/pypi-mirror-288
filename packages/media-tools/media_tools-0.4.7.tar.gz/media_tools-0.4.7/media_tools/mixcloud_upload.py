__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import sys
from argparse import ArgumentError, ArgumentParser, Namespace
from pathlib import Path
from shutil import copy
from typing import Callable, List

from media_tools.util.logging import setup_logging
from media_tools.util.mixcloud import (
    AuthorizationError, create_mix, get_access_token, DEFAULT_CROSSFADE_MS, DEFAULT_MAX_RETRY,
    DEFAULT_AUDIO_FILE_TYPES,
    MixPath
)
from media_tools.util.mixcloud.create_api_token import CreateAPIToken


def exists(check: Callable) -> Callable:
    def inner(arg: str) -> Path:
        path = Path(arg)
        if not path.exists():
            raise ValueError(f'{arg} does not exist')
        if not check(path):
            raise ValueError(f'{arg} is of wrong type')
        return path
    return inner


def parse_commandline(args: List[str]) -> Namespace:
    exit_on_error = {'exit_on_error': False} if sys.version_info >= (3, 9) else {}
    parser = ArgumentParser(
        description='Interface to the Mixcloud API to create mixes',
        **exit_on_error  # type: ignore
    )
    subparsers = parser.add_subparsers(
        title='subcommands', required=True
    )
    parse_upload_args(exit_on_error, subparsers)
    parse_create_auth_args(exit_on_error, subparsers)

    return parser.parse_args(args)


def parse_upload_args(exit_on_error, subparsers):
    parser_upload = subparsers.add_parser(
        'upload', help='Create a mix from audio files and uploads it to Mixcloud',
        **exit_on_error  # type: ignore
    )
    parser_upload.add_argument(
        '-d', '--directory', type=exists(Path.is_dir), required=True,
        help='Directory containing the mix'
    )
    parser_upload.add_argument(
        '-e', '--extensions', nargs='+', default=DEFAULT_AUDIO_FILE_TYPES,
        help='List of extensions considered as audio files for the mix'
    )
    parser_upload.add_argument(
        '-q', '--quiet', action='store_true'
    )
    parser_upload.add_argument(
        '-s', '--strict', action='store_true', help='Fail if any required data are missing'
    )
    parser_upload.add_argument(
        '-c', '--crossfade-ms', type=int, default=DEFAULT_CROSSFADE_MS,
        help='Milliseconds overlap between tracks'
    )
    parser_upload.add_argument(
        '-r', '--max-retry', type=int, default=DEFAULT_MAX_RETRY,
        help='Maximum number of retries for failing uploads'
    )
    group_auth = parser_upload.add_mutually_exclusive_group()
    group_auth.add_argument(
        '-a', '--auth-token-file', type=exists(Path.is_file),
        help='File containing the Mixcloud auth token'
    )
    group_auth.add_argument(
        '-t', '--auth-token-string', type=str, help='Mixcloud auth token as string'
    )
    group_description = parser_upload.add_mutually_exclusive_group()
    group_description.add_argument(
        '--description', type=str, help='Description for the mix as string'
    )
    group_description.add_argument(
        '--description-file', type=exists(Path.is_file),
        help='File containing the description for the mix'
    )
    group_tags = parser_upload.add_mutually_exclusive_group()
    group_tags.add_argument(
        '--tags', nargs='*', type=str, help='Tags for the mix as a list of strings'
    )
    group_tags.add_argument(
        '--tags-file', type=exists(Path.is_file),
        help='File containing the tags for the mix, one per line'
    )
    parser_upload.add_argument(
        '--picture-file', type=exists(Path.is_file), help='Picture file for the mix'
    )
    parser_upload.set_defaults(execute=do_upload)


def parse_create_auth_args(exit_on_error, subparsers):
    parser_create_auth = subparsers.add_parser(
        'create-auth', help='Create Mixcloud authentication and authorization',
        **exit_on_error  # type: ignore
    )
    parser_create_auth.add_argument(
        '--browser', choices=('system', 'selenium'), default='system',
        help='Browser used for app and token registration ("system" for interactive, '
             '"selenium" for automatic)'
    )
    group_step = parser_create_auth.add_mutually_exclusive_group()
    group_step.add_argument(
        '--create-app', action='store_true', help='Create a Mixcloud app (step 1)',
    )
    group_step.add_argument(
        '--create-code', action='store_true', help='Create an OAuth code (step 2)'
    )
    group_step.add_argument(
        '--create-token', action='store_true', help='Create an OAuth token (step 3)'
    )
    parser_create_auth.add_argument(
        '--client-id', type=str, help='Client ID for the app you generated in step 1'
    )
    parser_create_auth.add_argument(
        '--client-secret', type=str, help='Client ID for the app you generated in step 1'
    )
    parser_create_auth.add_argument(
        '--oauth-code', type=str, help='OAuth code you received in step 2'
    )
    parser_create_auth.set_defaults(execute=create_authentication)


def prep_mix_dir(opts: Namespace) -> None:
    description_file = opts.directory / 'description.txt'
    tags_file = opts.directory / 'tags.txt'
    if opts.description_file:
        copy(opts.description_file, description_file)
    if opts.description:
        with description_file.open('w') as file:
            file.write(opts.description)
    if opts.tags_file:
        copy(opts.tags_file, tags_file)
    if opts.tags:
        with tags_file.open('w') as file:
            file.write('\n'.join(opts.tags))
    if opts.picture_file:
        copy(opts.picture_file, opts.directory)
    check_strict(opts, description_file, tags_file)


def check_strict(opts, description_file, tags_file):
    if not description_file.exists():
        warning_or_error(opts, f'description file {description_file} needed')
    if not tags_file.exists():
        warning_or_error(opts, f'tags file {tags_file} needed')
    if not list(opts.directory.glob('*.*p*g')):
        warning_or_error(opts, f'picture file needed in {opts.directory}')


def warning_or_error(opts, message):
    if opts.strict:
        raise ValueError(message)
    logging.warning(message)


def extract_auth_token(opts: Namespace) -> str:
    if opts.auth_token_string is not None:
        return opts.auth_token_string
    return get_access_token(opts.auth_token_file)


def do_upload(opts: Namespace):
    try:
        access_token = extract_auth_token(opts)
        prep_mix_dir(opts)

        mix_path = MixPath(Path(opts.directory), tuple(f'*.{ext}' for ext in opts.extensions))
        mix = create_mix(mix_path, access_token, crossfade_ms=opts.crossfade_ms, strict=opts.strict)
        mix.export()
        mix.upload(max_retry=opts.max_retry)
    except (ValueError, AuthorizationError) as error:
        logging.error(error)
        sys.exit(1)
    except KeyboardInterrupt:
        logging.warning('interrupted by user!')


def create_authentication(opts: Namespace):
    if opts.create_code and not opts.client_id:
        raise ArgumentError(None, message='--create-code needs --client-id')
    if opts.create_token and not (opts.client_id and opts.client_secret and opts.oauth_code):
        raise ArgumentError(
            None, message='--create-code needs --client-id, --client-secret and --oauth-code '
        )
    if opts.browser == 'selenium':
        raise NotImplementedError('selenium engine')
    create_token = CreateAPIToken.create(opts)
    create_token.run()


def main() -> None:
    try:
        opts = parse_commandline(sys.argv[1:])
    except ArgumentError as error:
        setup_logging(Namespace())
        logging.error(error)
        sys.exit(1)

    setup_logging(opts)
    opts.execute(opts)


if __name__ == '__main__':
    main()
