import asyncio

from typing_extensions import TypeAlias

Process: TypeAlias = asyncio.subprocess.Process

StreamWriter: TypeAlias = asyncio.StreamWriter
StreamReader: TypeAlias = asyncio.StreamReader
