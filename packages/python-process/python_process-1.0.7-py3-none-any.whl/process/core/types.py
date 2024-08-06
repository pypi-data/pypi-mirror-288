import os
import sys
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
