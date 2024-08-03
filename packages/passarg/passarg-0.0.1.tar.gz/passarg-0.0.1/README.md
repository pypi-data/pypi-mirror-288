# passarg: OpenSSL password/-phrase argument

The passarg ("password argument") module implements
OpenSSL-style password/passphrase argument handling.

# Quickstart

```python
from argparse import ArgumentParser

import passarg

parser = ArgumentParser()
parser.add_argument('--pass-in', metavar='SPEC', default='env:MY_PASS_IN')
parser.add_argument('--pass-out', metavar='SPEC', default='env:MY_PASS_OUT')
args = parser.parse_args()

with passarg.reader() as read_passarg:
    pass_in = read_passarg(args.pass_in)
    pass_out = read_passarg(args.pass_out)
```

The program above then by default reads the input/output passphrases
from the environment variables `${MY_PASS_IN}` and `${MY_PASS_OUT}`;
if run with `--pass-in file:dec-pass.txt --pass-out stdin`,
then it reads the input/output passphrases
from the file `dec-pass.txt` and the standard input respectively.

# Passphrase Argument Syntax

From [openssl-passphrase-options(1)]:

> Pass phrase arguments can be formatted as follows.
>
> * **pass**:*password*
>
>   The actual password is *password*.
>   Since the password is visible to utilities (like 'ps' under Unix)
>   this form should only be used where security is not important.
>
> * **env**:*var*
>
>   Obtain the password from the environment variable *var*.
>   Since the environment of other processes is visible on certain platforms
>   (e.g. ps under certain Unix OSes)
>   this option should be used with caution.
>
> * **file**:*pathname*
>
>   Reads the password from the specified file *pathname*,
>   which can be a regular file, device, or named pipe.
>   Only the first line, up to the newline character, is read from the stream.
>
>   If the same *pathname* argument is supplied
>   to both **-passin** and **-passout** arguments,
>   the first line will be used for the input password,
>   and the next line will be used for the output password.
>
> * **fd**:*number*
>
>   Reads the password from the file descriptor *number*.
>   This can be useful for sending data via a pipe, for example.
>   The same line handling as described for **file:** applies
>   to passwords read from file descriptors.
>
>   **fd:** is not supported on Windows.
>
> * **stdin**
>
>   Reads the password from standard input.
>   The same line handling as described for **file:** applies
>   to passwords read from standard input.

# .env ("dotenv") File Support

passarg can be combined with [python-dotenv] to add support for dotenv files.
Simply call load_dotenv before entering the `passarg.reader()` context:

```python
from argparse import ArgumentParser

import dotenv

import passarg

parser = ArgumentParser()
parser.add_argument('--api-key', metavar='SPEC', default='env:MY_API_KEY')
parser.add_argument('--env-file', metavar='PATH', default='.env')
args = parser.parse_args()

dotenv.load_dotenv(args.env_file)

with passarg.reader() as read_passarg:
    api_key = read_passarg(args.api_key)
```

Then it can be run in the directory with an `.env` file like:

```
MY_API_KEY=MySuperSecretKeyOmigod
```

## Passargs Sharing Same File-like Source

As explained in [Passphrase Argument Syntax](#passphrase-argument-syntax) above,
multiple passphrase arguments can share the same file-like source,
with each source reading one line from the source.

The order of calls to `read_passarg()` matters, and should be documented.
For example, the [Quickstart example](#quickstart) above
reads `--pass-in` first then `--pass-out`,
implementing the same input-password-first ordering as with OpenSSL.

[python-dotenv]: https://pypi.org/project/python-dotenv/
[openssl-passphrase-options(1)]: https//docs.openssl.org/3.3/man1/openssl-passphrase-options/
