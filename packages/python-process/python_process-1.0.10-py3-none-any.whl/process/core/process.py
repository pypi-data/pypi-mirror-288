from __future__ import annotations

import asyncio
import shlex
import subprocess
import sys
from abc import ABC, abstractmethod
from contextlib import suppress
from os import PathLike, fspath
from typing import TYPE_CHECKING, Generic, Optional, Sequence, TypeVar, Union

from typing_extensions import Self

from process.core.constants import PIPE
from process.core.errors import ProcessInvalidStreamError, ProcessNotRunError
from process.core.protocol import ProcessProtocol
from process.core.types import Buffer, File, Returns, StrOrPath

if TYPE_CHECKING:
    from process.asyncio.types import StreamReader as AsyncStreamReader
    from process.asyncio.types import StreamWriter as AsyncStreamWriter
    from process.types import StreamReader, StreamWriter


W = TypeVar("W", "StreamWriter", "AsyncStreamWriter", covariant=True)
R = TypeVar("R", "StreamReader", "AsyncStreamReader", covariant=True)


class AbstractProcess(ABC, ProcessProtocol[W, R], Generic[W, R]):
    """Abstract base class for managing processes."""

    def __init__(
        self,
        arguments: Union[StrOrPath, Sequence[StrOrPath]],
        stdin: Optional[Union[Buffer, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None:
        """Initialize a new `Process` instance with the given `arguments` and run the process.

        Args:
            arguments: The command and its arguments for the process.
            stdin: A `bytes` object containing the input data, file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`) to use as the standard input.
            stdout: A file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`) to use as the standard output.
            stderr: A file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`, `STDOUT`) to use as the standard error.
            buffer_size: The buffer size for the stream operations. If `0`, all operations will be unbuffered.

        Notes:
            If `arguments` is a `str`, it will be split into a list of arguments using [`shlex.split()`][shlex.split].
        """
        if isinstance(arguments, str):
            arguments = shlex.split(arguments)
        elif isinstance(arguments, PathLike):
            arguments = [arguments]

        if buffer_size is None:
            raise ValueError("`buffer_size` should be set to the default buffer size.")

        self._arguments: list[str] = [fspath(argument) for argument in arguments]

        self._stdin: Optional[Union[Buffer, File]] = stdin
        self._stdout: Optional[File] = stdout
        self._stderr: Optional[File] = stderr

        self._buffer_size: int = buffer_size

        self._output: bytes = b""
        self._error: bytes = b""

        if sys.version_info >= (3, 9):
            self._process: Optional[Union[subprocess.Popen[bytes], asyncio.subprocess.Process]] = None
        else:
            self._process: Optional[Union[subprocess.Popen, asyncio.subprocess.Process]] = None

    @abstractmethod
    def __del__(self) -> None:
        """Clean up resources used by the process."""
        ...

    @property
    def arguments(self) -> list[str]:
        """Get the command-line arguments used to run the process."""
        return list(self._arguments)

    if sys.version_info >= (3, 9):

        @property
        @abstractmethod
        def process(self) -> Union[subprocess.Popen[bytes], asyncio.subprocess.Process]:
            """Get the underlying process object.

            Returns:
                The process object, which is either an instance of [`subprocess.Popen`][subprocess.Popen] or [`asyncio.subprocess.Process`][asyncio.subprocess.Process]

            Raises:
                ProcessNotRunError: If the process has not been run.
            """
            ...
    else:

        @property
        @abstractmethod
        def process(self) -> Union[subprocess.Popen, asyncio.subprocess.Process]:
            """Get the underlying process object.

            Returns:
                The process object, which is either an instance of [`subprocess.Popen`][subprocess.Popen] or [`asyncio.subprocess.Process`][asyncio.subprocess.Process]

            Raises:
                ProcessNotRunError: If the process has not been run.
            """
            ...

    @property
    def id(self) -> int:
        """Return the process identifier.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        return self.process.pid

    @property
    @abstractmethod
    def running(self) -> bool:
        """Check if the process is currently running.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    @property
    def exit_code(self) -> Optional[int]:
        """Get the exit code of the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        return self.process.returncode

    @abstractmethod
    def run(self) -> Returns[Self]:
        """Run the process.

        Returns:
            The current `Process` instance itself.

        Raises:
            ProcessAlreadyRunError: If the process has already been run.
            ProcessError: If the process fails to run.
        """
        ...

    @abstractmethod
    def output(self, join: bool = True) -> Returns[bytes]:
        """Return the standard output of the process if the process was created with `stdout=PIPE`.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    @abstractmethod
    def error(self, join: bool = True) -> Returns[bytes]:
        """Return the standard error of the process if the process was created with `stderr=PIPE`.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...

    @abstractmethod
    def join(self, timeout: Optional[float] = None) -> Returns[None]:
        """Wait for the process to complete.

        Args:
            timeout: Maximum time to wait for the process to complete, in seconds. If `None`, wait indefinitely.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessTimeoutError: If the process does not complete within the specified timeout.
        """
        ...

    def signal(self, signal: int) -> None:
        """Send a signal to the process.

        Args:
            signal: The signal number to send.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        self.process.send_signal(signal)

    def terminate(self) -> None:
        """Gracefully terminate the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        self.process.terminate()

    def kill(self) -> None:
        """Forcefully kill the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        self.process.kill()

    @abstractmethod
    def close(self) -> Returns[None]:
        """Terminate the process, wait for the process to complete, and clean up resources used by the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """

    @property
    @abstractmethod
    def stdin(self) -> W:
        """Get the standard input stream of the process.

        Returns:
            The standard input stream of the process if the process was created with `stdin=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdin=PIPE`.
        """
        ...

    @property
    @abstractmethod
    def stdout(self) -> R:
        """Get the standard output stream of the process.

        Returns:
            The standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    @property
    @abstractmethod
    def stderr(self) -> R:
        """Get the standard error stream of the process.

        Returns:
            The standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...

    def __repr__(self) -> str:
        """Return a [`str`][str] representation of the current process instance.

        Returns:
            A [`str`][str] representation of the current process instance.
        """
        items = [f"arguments={self.arguments!r}"]

        with suppress(ProcessNotRunError):
            items.extend([f"id={self.id!r}", f"running={self.running!r}", f"exit_code={self.exit_code!r}"])

            with suppress(ProcessInvalidStreamError):
                items.append(f"stdin={self.stdin!r}")

            with suppress(ProcessInvalidStreamError):
                items.append(f"stdout={self.stdout!r}")

            with suppress(ProcessInvalidStreamError):
                items.append(f"stderr={self.stderr!r}")

        return f"{type(self).__name__}({', '.join(items)})"
