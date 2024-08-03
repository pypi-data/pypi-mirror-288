"""
OpenSSL-style password argument handling.

See `the package README <https://pypi.org/projects/passarg/>`_ for details.
"""

__version__ = '0.0.1'

import os
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager, ExitStack
from pathlib import Path
from typing import Self


class InvalidPassArg(ValueError):
    """Invalid password argument."""


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
                case _:
                    raise InvalidPassArg(arg)

        yield read_passarg
