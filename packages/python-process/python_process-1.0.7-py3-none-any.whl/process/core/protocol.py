from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence, TypeVar, Union

from typing_extensions import Protocol, Self, overload

from process.core.constants import PIPE
from process.core.types import Buffer, File, Returns, StrOrPath

if TYPE_CHECKING:
    from process.asyncio.types import Process as AsyncProcess
    from process.asyncio.types import StreamReader as AsyncStreamReader
    from process.asyncio.types import StreamWriter as AsyncStreamWriter
    from process.types import Process, StreamReader, StreamWriter


P_co = TypeVar("P_co", "Process", "AsyncProcess", covariant=True)
W_co = TypeVar("W_co", "StreamWriter", "AsyncStreamWriter", covariant=True)
R_co = TypeVar("R_co", "StreamReader", "AsyncStreamReader", covariant=True)


class ProcessProtocol(Protocol[P_co, W_co, R_co]):
    """A protocol that defines the interface for spawning and managing a process."""

    @overload
    def __init__(
        self,
        arguments: StrOrPath,
        stdin: Optional[Union[Buffer, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        arguments: Sequence[StrOrPath],
        stdin: Optional[Union[Buffer, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None: ...

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
            buffer_size: The buffer size for the stream operations. If `None`, the default buffer size will be used. If `0`, all operations will be unbuffered.

        Notes:
            If `arguments` is a `str`, it will be split into a list of arguments using [`shlex.split()`][shlex.split].
        """
        ...

    def __del__(self) -> None:
        """Clean up resources used by the process."""
        ...

    @property
    def arguments(self) -> list[str]:
        """Get the command-line arguments used to run the process."""
        ...

    @property
    def id(self) -> int:
        """Return the process identifier.

        ProcessNotRunError: If the process has not been run.
        """
        ...

    def run(self) -> Returns[Self]:
        """Run the process.

        Returns:
            The current `Process` instance itself.

        Raises:
            ProcessAlreadyRunError: If the process has already been run.
            ProcessError: If the process fails to run.
        """
        ...

    def output(self, join: bool = True) -> Returns[bytes]:
        """Return the standard output of the process if the process was created with `stdout=PIPE`.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    def error(self, join: bool = True) -> Returns[bytes]:
        """Return the standard error of the process if the process was created with `stderr=PIPE`.

        Args:
            join: Whether to wait for the process to complete before retuning the standard output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...

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
        ...

    def terminate(self) -> None:
        """Gracefully terminate the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def kill(self) -> None:
        """Forcefully kill the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def close(self) -> Returns[None]:
        """Close the process and release its resources.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """

    @property
    def process(self) -> P_co:
        """Get the underlying process object.

        Returns:
            The process object, which is either an instance of [`subprocess.Popen`][subprocess.Popen] or [`asyncio.subprocess.Process`][asyncio.subprocess.Process]

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    @property
    def stdin(self) -> W_co:
        """Get the standard input stream of the process.

        Returns:
            The standard input stream of the process if the process was created with `stdin=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdin=PIPE`.
        """
        ...

    @property
    def stdout(self) -> R_co:
        """Get the standard output stream of the process.

        Returns:
            The standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    @property
    def stderr(self) -> R_co:
        """Get the standard error stream of the process.

        Returns:
            The standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...

    @property
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
        ...
