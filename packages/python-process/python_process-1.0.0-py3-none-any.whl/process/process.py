from __future__ import annotations

import shlex
import subprocess
from contextlib import suppress
from io import BufferedIOBase, BufferedReader, BufferedWriter, FileIO, RawIOBase
from os import PathLike, fspath
from typing import Any, Optional, Sequence, Union, cast

from typing_extensions import Self

from process.constants import DEFAULT_BUFFER_SIZE, PIPE
from process.errors import (
    ProcessAlreadyRunError,
    ProcessError,
    ProcessInvalidStreamError,
    ProcessNotRunError,
    ProcessTimeoutError,
)
from process.protocol import ProcessProtocol
from process.types import Buffer, File, StreamReader, StreamWriter, StrOrPath
from process.utils import is_windows


class Process(ProcessProtocol[StreamReader, StreamWriter]):
    """A class for spawning, managing, and interacting with a process synchronously.

    This class provides a convenient interface for running a process, interacting with its input, output, and error streams, and managing its execution.
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
        self._process: Optional[subprocess.Popen[bytes]] = None

    def __del__(self) -> None:
        """Clean up resources used by the process.

        This method cleans up resources as follows:

        - If the process is running, terminate the process.
        - Wait for the process to complete.
        - Close the standard output stream if the process was created with `stdout=PIPE` and the stream is not closed.
        - Close the standard error stream if the process was created with `stderr=PIPE` and the stream is not closed.
        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        """
        if self._process is None:
            return

        if self.running:
            self.terminate()
            self.join()

        with suppress(ProcessInvalidStreamError):
            if not self.stdout.closed:
                self.stdout.close()

        with suppress(ProcessInvalidStreamError):
            if not self.stderr.closed:
                self.stderr.close()

        with suppress(ProcessInvalidStreamError, BrokenPipeError, ConnectionResetError):
            if not self.stdin.closed:
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

    def run(self) -> Self:
        """Run the process.

        Returns:
            The current [`Process`][process.Process] instance itself.

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
            self._process = subprocess.Popen(
                self.arguments,
                bufsize=self._buffer_size,
                stdin=cast(File, stdin) if not should_feed_stdin else PIPE,
                stdout=self._stdout,
                stderr=self._stderr,
                creationflags=creationflags,
            )
        except Exception as exception:
            raise ProcessError(f"Failed to run process: {exception}")

        if should_feed_stdin:
            # Since `Popen.communicate()` requires the process to terminate, we feed the input ourselves.
            # If deadlock issues are reported, consider using a different approach, such as threading.
            self.stdin.write(cast(Buffer, stdin))
            self.stdin.close()

        return self

    def output(self, join: bool = True) -> bytes:
        r"""Return the standard output of the process if the process was created with `stdout=PIPE`.

        Warning:
            If the standard output of the process is modified by others, the result of [`output()`][process.Process.output] will be affected by those changes.

            ```python
            with Process("echo something") as process:
                print(process.stdout.read(4))  # b'some'
            print(process.output())  # b'thing\n'
            ```

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if join:
            self.join()

        if not self.stdout.closed:
            self._output += self.stdout.read()

        return self._output

    def error(self, join: bool = True) -> bytes:
        """Return the standard error of the process if the process was created with `stderr=PIPE`.

        Warning:
            If the standard error of the process is modified by others, the result of [`error()`][process.Process.error] will be affected by those changes.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        if join:
            self.join()

        if not self.stderr.closed:
            self._error += self.stderr.read()

        return self._error

    def join(self, timeout: Optional[float] = None) -> None:
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
            self._process.wait(timeout)
        except subprocess.TimeoutExpired:
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

    def __enter__(self) -> Self:
        """Enter the runtime context for this [`Process`][process.Process] instance.

        This method runs the process.

        Returns:
            The current [`Process`][process.Process] instance itself.
        """
        return self.run()

    def __exit__(self, *args: Any) -> None:
        """Exit the runtime context for this [`Process`][process.Process] instance.

        This method cleans up the process execution as follows:

        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        - Wait for the process to complete.
        - Read the remaining output from the standard output stream and then close the stream if the process was created with `stdout=PIPE` and the stream is not closed.
        - Read the remaining error output from the standard error stream and then close the stream if the process was created with `stderr=PIPE` and the stream is not closed.
        """
        with suppress(ProcessInvalidStreamError):
            # Since we are cleaning up, suppress errors from closing the standard input stream by following the approach in
            # https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Lib/subprocess.py#L1097
            with suppress(BrokenPipeError, ConnectionResetError):
                if not self.stdin.closed:
                    self.stdin.close()

        self.join()

        with suppress(ProcessInvalidStreamError):
            if not self.stdout.closed:
                self._output += self.stdout.read()
                self.stdout.close()

        with suppress(ProcessInvalidStreamError):
            if not self.stderr.closed:
                self._error += self.stderr.read()
                self.stderr.close()

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

        # According to the documentation for [`Popen.stdin`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L892)
        # > If the *stdin* argument was :data:`PIPE`, this attribute is a writeable stream object as returned by :func:`open`.
        # According to the documentation for [`open`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/functions.rst?plain=1#L1418)
        # > When used to open a file in a binary mode with buffering, the returned class is a subclass of :class:`io.BufferedIOBase`.
        # > The exact class varies: in read binary mode, it returns an :class:`io.BufferedReader`;
        # > in write binary and append binary modes, it returns an :class:`io.BufferedWriter`, and
        # > in read/write mode, it returns an :class:`io.BufferedRandom`.
        # > When buffering is disabled, the raw stream, a subclass of :class:`io.RawIOBase`, :class:`io.FileIO`, is returned.
        if isinstance(self._process.stdin, BufferedIOBase):
            return cast(BufferedWriter, self._process.stdin)
        elif isinstance(self._process.stdin, RawIOBase):
            return cast(FileIO, self._process.stdin)
        else:
            assert False, "Unreachable code"

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

        # According to the documentation for [`Popen.stdout`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L901)
        # > If the *stdout* argument was :data:`PIPE`, this attribute is a readable stream object as returned by :func:`open`.
        # According to the documentation for [`open`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/functions.rst?plain=1#L1418)
        # > When used to open a file in a binary mode with buffering, the returned class is a subclass of :class:`io.BufferedIOBase`.
        # > The exact class varies: in read binary mode, it returns an :class:`io.BufferedReader`;
        # > in write binary and append binary modes, it returns an :class:`io.BufferedWriter`, and
        # > in read/write mode, it returns an :class:`io.BufferedRandom`.
        # > When buffering is disabled, the raw stream, a subclass of :class:`io.RawIOBase`, :class:`io.FileIO`, is returned.
        if isinstance(self._process.stdout, BufferedIOBase):
            return cast(BufferedReader, self._process.stdout)
        elif isinstance(self._process.stdout, RawIOBase):
            return cast(FileIO, self._process.stdout)
        else:
            assert False, "Unreachable code"

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

        # According to the documentation for [`Popen.stderr`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L911)
        # > If the *stderr* argument was :data:`PIPE`, this attribute is a readable stream object as returned by :func:`open`.
        # According to the documentation for [`open`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/functions.rst?plain=1#L1418)
        # > When used to open a file in a binary mode with buffering, the returned class is a subclass of :class:`io.BufferedIOBase`.
        # > The exact class varies: in read binary mode, it returns an :class:`io.BufferedReader`;
        # > in write binary and append binary modes, it returns an :class:`io.BufferedWriter`, and
        # > in read/write mode, it returns an :class:`io.BufferedRandom`.
        # > When buffering is disabled, the raw stream, a subclass of :class:`io.RawIOBase`, :class:`io.FileIO`, is returned.
        if isinstance(self._process.stderr, BufferedIOBase):
            return cast(BufferedReader, self._process.stderr)
        elif isinstance(self._process.stderr, RawIOBase):
            return cast(FileIO, self._process.stderr)
        else:
            assert False, "Unreachable code"

    @property
    def running(self) -> bool:
        """Check if the process is currently running.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return self._process.poll() is None

    @property
    def exit_code(self) -> Optional[int]:
        """Get the exit code of the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return self._process.returncode
