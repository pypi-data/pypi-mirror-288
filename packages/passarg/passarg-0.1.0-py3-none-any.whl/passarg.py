"""
OpenSSL-style password argument handling.

See `the package README <https://pypi.org/project/passarg/>`_ for details.
"""

__version__ = '0.1.0'

import os
import subprocess
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager, ExitStack
from getpass import getpass
from pathlib import Path
from urllib.parse import urlsplit


class InvalidPassArg(ValueError):
    """Invalid password argument."""


_DEFAULT_OP_FIELD = 'password'


def _read_from_op_url(url: str):
    scheme, netloc, path, query, frag = urlsplit(url)
    path = path.strip('/')
    match path.rsplit('/', 1):
        case [item, field]:
            return _read_from_op(netloc, item, field or _DEFAULT_OP_FIELD)
        case [item]:
            return _read_from_op(netloc, item, _DEFAULT_OP_FIELD)


def _read_from_op(vault: str, item: str, field: str):
    cmd = ['op', 'item', 'get']
    if vault:
        cmd.append(f'--vault={vault}')
    cmd.extend([f'--field={field}', '--reveal', '--', item])
    return subprocess.check_output(cmd).decode().rstrip('\n')


@contextmanager
def reader() -> Iterator[Callable[[str], str]]:
    """
    Returns a passarg-reading context manager.

    When entered, the context manager yields a function that can be called
    to read a password from the given string argument,
    in the same syntax as in `openssl-passphrase-options(1)`_.

    The context manager closes all ``file:`` and ``fd:`` sources used
    upon exiting the context, but leaves `stdin`` open.

    See the package README for details.

    .. _openssl-passphrase-options(1):
        https//docs.openssl.org/3.3/man1/openssl-passphrase-options/
    """
    with ExitStack() as stack:
        files = {}

        def read_passarg(arg: str) -> str:
            """
            Reads a password from the given source.

            :param arg:
                the source from which to read the password.
                See `openssl-passphrase-options(1)`_ for details.
            :returns:
                the password read.
            :raises `InvalidPassArg`:
                if `arg` is invalid.
            :raises `KeyError`:
                if the given ``env:`` variable is not found.
            :raises `OSError`:
                if the given ``file:``(-like) source cannot be opened or read.
            :raises `subprocess.CalledProcessError`:
                if an external command (such as 1Password CLI) failed.

            .. _openssl-passphrase-options(1):
                https//docs.openssl.org/3.3/man1/openssl-passphrase-options/
            """
            match arg.split(':', 1):
                case ['pass', password]:
                    return password
                case ['env', var]:
                    return os.environ[var]
                case ['file', pathname]:
                    pathname = Path(pathname).resolve()
                    try:
                        f = files[pathname]
                    except KeyError:
                        f = stack.enter_context(pathname.open())
                        files[pathname] = f
                    return f.readline().rstrip('\n')
                case ['fd', number]:
                    fd = int(number)
                    try:
                        f = files[fd]
                    except KeyError:
                        f = stack.enter_context(open(fd))
                        files[fd] = f
                    return f.readline().rstrip('\n')
                case ['stdin']:
                    return sys.stdin.readline().rstrip('\n')
                case ['prompt']:
                    return getpass()
                case ['prompt', prompt]:
                    return getpass(prompt)
                case ['op', *_]:
                    return _read_from_op_url(arg)
                case _:
                    raise InvalidPassArg(arg)

        yield read_passarg
