from __future__ import annotations

import asyncio
import shlex
import subprocess
import sys
from contextlib import suppress
from os import PathLike, fspath
from typing import Any, Optional, Sequence, Union, cast

from typing_extensions import Self

from process.asyncio.constants import DEFAULT_BUFFER_SIZE
from process.asyncio.types import StreamReader, StreamWriter
from process.constants import PIPE
from process.errors import (
    ProcessAlreadyRunError,
    ProcessError,
    ProcessInvalidStreamError,
    ProcessNotRunError,
    ProcessTimeoutError,
)
from process.protocol import ProcessProtocol
from process.types import Buffer, File, StrOrPath
from process.utils import is_windows

if sys.version_info < (3, 11):
    from asyncio import TimeoutError as TimeoutError


class Process(ProcessProtocol[StreamReader, StreamWriter]):
    """A class for spawning, managing, and interacting with a process asynchronously.

    This class provides a convenient interface for running a process, interacting with its input, output, and error streams, and managing its execution.

    Notes:
        In Python 3.7 on Windows, the default [`asyncio`][asyncio] event loop implementation does not support subprocesses.
        To enable subprocess support, it is necessary to change the event loop policy to use [`ProactorEventLoop`][asyncio.ProactorEventLoop] as follows:

        ```python
        import asyncio

        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        ```
    """

    def __init__(
        self,
        arguments: Union[StrOrPath, Sequence[StrOrPath]],
        stdin: Optional[Union[Buffer, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = DEFAULT_BUFFER_SIZE,
    ) -> None:
        """Initialize a new `Process` instance with the given `arguments` and run the process.

        Args:
            arguments: The command and its arguments for the process.
            stdin: A `bytes` object containing the input data, file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`) to use as the standard input.
            stdout: A file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`) to use as the standard output.
            stderr: A file-like object, file descriptor, or special value (`None`, `PIPE`, `DEVNULL`, `STDOUT`) to use as the standard error.
            buffer_size: The buffer size for the stream operations. If `None`, all stream operations are unbuffered.

        Notes:
            If `arguments` is a `str`, it will be split into a list of arguments using [`shlex.split()`][shlex.split].
        """
        if isinstance(arguments, str):
            arguments = shlex.split(arguments)
        elif isinstance(arguments, PathLike):
            arguments = [arguments]

        if buffer_size is None:
            buffer_size = 0

        self._arguments: list[str] = [fspath(argument) for argument in arguments]

        self._stdin: Optional[Union[Buffer, File]] = stdin
        self._stdout: Optional[File] = stdout
        self._stderr: Optional[File] = stderr
        self._buffer_size: int = buffer_size

        self._output: bytes = b""
        self._error: bytes = b""
        self._process: Optional[asyncio.subprocess.Process] = None

    def __del__(self) -> None:
        """Clean up resources used by the process.

        This method cleans up resources as follows:

        - If the process is running, terminate the process.
        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        """
        if self._process is None:
            return

        if self.running:
            self.terminate()

        with suppress(ProcessInvalidStreamError, BrokenPipeError, ConnectionResetError):
            if not self.stdin.is_closing():
                self.stdin.close()

    @property
    def arguments(self) -> list[str]:
        """Get the command-line arguments used to run the process."""
        return list(self._arguments)

    @property
    def id(self) -> int:
        """Return the process identifier.

        ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return self._process.pid

    async def run(self) -> Self:
        """Run the process.

        Returns:
            The current [`Process`][process.asyncio.Process] instance itself.

        Raises:
            ProcessAlreadyRunError: If the process has already been run.
            ProcessError: If the process fails to run.
        """
        if self._process is not None:
            raise ProcessAlreadyRunError("Process has already been run")

        creationflags = 0

        # According to the documentation for [`Popen.send_signal()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L864),
        # > On Windows, ... CTRL_C_EVENT and CTRL_BREAK_EVENT can be sent to processes
        # > started with a *creationflags* parameter which includes ``CREATE_NEW_PROCESS_GROUP``.
        if is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore

        stdin = self._stdin
        should_feed_stdin = isinstance(stdin, (bytes, bytearray, memoryview))

        try:
            self._process = await asyncio.subprocess.create_subprocess_exec(
                *self.arguments,
                stdin=cast(File, stdin) if not should_feed_stdin else PIPE,
                stdout=self._stdout,
                stderr=self._stderr,
                limit=self._buffer_size,
                creationflags=creationflags,
            )
        except Exception as exception:
            raise ProcessError(f"Failed to run process: {exception}")

        if should_feed_stdin:
            # Since `Popen.communicate()` requires the process to terminate, we feed the input ourselves.
            # If deadlock issues are reported, consider using a different approach, such as threading.
            self.stdin.write(cast(Buffer, stdin))
            await self.stdin.drain()

            self.stdin.close()

            # Contrary to the documentation for [`StreamWriter.wait_closed()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/asyncio-stream.rst?plain=1#L383),
            # using `wait_closed()` in Python 3.7 raises `AttributeError: 'SubprocessStreamProtocol' object has no attribute '_closed'`.
            if sys.version_info >= (3, 8):
                await self.stdin.wait_closed()

        return self

    async def output(self, join: bool = True) -> bytes:
        r"""Return the standard output of the process if the process was created with `stdout=PIPE`.

        Warning:
            If the standard output of the process is modified by others, the result of [`output()`][process.asyncio.Process.output] will be affected by those changes.

            ```python
            async with Process("echo something") as process:
                print(await process.stdout.read(4))  # b'some'
            print(await process.output())  # b'thing\n'
            ```

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if join:
            await self.join()

        self._output += await self.stdout.read()

        return self._output

    async def error(self, join: bool = True) -> bytes:
        """Return the standard error of the process if the process was created with `stderr=PIPE`.

        Warning:
            If the standard error of the process is modified by others, the result of [`error()`][process.asyncio.Process.error] will be affected by those changes.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if join:
            await self.join()

        self._error += await self.stderr.read()

        return self._error

    async def join(self, timeout: Optional[float] = None) -> None:
        """Wait for the process to complete.

        Args:
            timeout: Maximum time to wait for the process to complete, in seconds. If `None`, wait indefinitely.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessTimeoutError: If the process does not complete within the specified timeout.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        try:
            await asyncio.wait_for(self._process.wait(), timeout=timeout)
        except TimeoutError:
            raise ProcessTimeoutError(f"Process did not complete within {timeout} seconds")

    def signal(self, signal: int) -> None:
        """Send a signal to the process.

        Args:
            signal: The signal number to send.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        self._process.send_signal(signal)

    def terminate(self) -> None:
        """Gracefully terminate the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        self._process.terminate()

    def kill(self) -> None:
        """Forcefully kill the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        self._process.kill()

    async def __aenter__(self) -> Self:
        """Enter the runtime context for this [`Process`][process.asyncio.Process] instance.

        This method runs the process.

        Returns:
            The current [`Process`][process.asyncio.Process] instance itself.
        """
        return await self.run()

    async def __aexit__(self, *args: Any) -> None:
        """Exit the runtime context for this [`Process`][process.asyncio.Process] instance.

        This method cleans up the process execution as follows:

        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        - Wait for the process to complete.
        - Read the remaining output from the standard output stream if the process was created with `stdout=PIPE`.
        - Read the remaining error output from the standard error stream if the process was created with `stderr=PIPE`.
        """
        with suppress(ProcessInvalidStreamError):
            # Since we are cleaning up, suppress errors from closing the standard input stream by following the approach in
            # https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Lib/subprocess.py#L1097
            with suppress(BrokenPipeError, ConnectionResetError):
                if not self.stdin.is_closing():
                    self.stdin.close()

                    # Contrary to the documentation for [`StreamWriter.wait_closed()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/asyncio-stream.rst?plain=1#L383),
                    # using `wait_closed()` in Python 3.7 raises `AttributeError: 'SubprocessStreamProtocol' object has no attribute '_closed'`.
                    if sys.version_info >= (3, 8):
                        await self.stdin.wait_closed()

        await self.join()

        with suppress(ProcessInvalidStreamError):
            self._output += await self.stdout.read()

        with suppress(ProcessInvalidStreamError):
            self._error += await self.stderr.read()

    @property
    def stdin(self) -> StreamWriter:
        """Get the standard input stream of the process.

        Returns:
            The standard input stream of the process if the process was created with `stdin=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdin=PIPE`.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if self._process.stdin is None:
            raise ProcessInvalidStreamError("Process was not created with `stdin=PIPE`")

        return self._process.stdin

    @property
    def stdout(self) -> StreamReader:
        """Get the standard output stream of the process.

        Returns:
            The standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if self._process.stdout is None:
            raise ProcessInvalidStreamError("Process was not created with `stdout=PIPE`")

        return self._process.stdout

    @property
    def stderr(self) -> StreamReader:
        """Get the standard error stream of the process.

        Returns:
            The standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if self._process.stderr is None:
            raise ProcessInvalidStreamError("Process was not created with `stderr=PIPE`")

        return self._process.stderr

    @property
    def running(self) -> bool:
        """Check if the process is currently running.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return self._process.returncode is None

    @property
    def exit_code(self) -> Optional[int]:
        """Get the exit code of the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return self._process.returncode
