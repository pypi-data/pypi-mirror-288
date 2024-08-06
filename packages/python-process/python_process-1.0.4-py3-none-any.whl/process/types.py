import os
import sys
from io import BufferedReader, BufferedWriter, FileIO
from typing import IO, Any, Coroutine, TypeVar, Union

from typing_extensions import TypeAlias

T = TypeVar("T")

Returns: TypeAlias = Union[T, Coroutine[Any, Any, T]]

if sys.version_info >= (3, 9):
    PathLike = os.PathLike[str]
else:
    PathLike = os.PathLike

StrOrPath: TypeAlias = Union[str, PathLike]

# According to the documentation for [`typing.ByteString`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/typing.rst?plain=1#L3272):
# > This type represents the types :class:`bytes`, :class:`bytearray`, and :class:`memoryview` of byte sequences.
# > Prefer :class:`collections.abc.Buffer`, or a union like ``bytes | bytearray | memoryview``.
Buffer: TypeAlias = Union[bytes, bytearray, memoryview]

# Reference: https://github.com/python/typeshed/blob/0fd6cd211f9f8b17d6b3960ff96051ec89fb908c/stdlib/subprocess.pyi#L65
File: TypeAlias = Union[int, IO[bytes]]

# According to the documentation for [`Popen.stdin`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L892)
# > If the *stdin* argument was :data:`PIPE`, this attribute is a writeable stream object as returned by :func:`open`.
# According to the documentation for [`open`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/functions.rst?plain=1#L1418)
# > When used to open a file in a binary mode with buffering, the returned class is a subclass of :class:`io.BufferedIOBase`.
# > The exact class varies: in read binary mode, it returns an :class:`io.BufferedReader`;
# > in write binary and append binary modes, it returns an :class:`io.BufferedWriter`, and
# > in read/write mode, it returns an :class:`io.BufferedRandom`.
# > When buffering is disabled, the raw stream, a subclass of :class:`io.RawIOBase`, :class:`io.FileIO`, is returned.
StreamReader: TypeAlias = Union[FileIO, BufferedReader]
StreamWriter: TypeAlias = Union[FileIO, BufferedWriter]
