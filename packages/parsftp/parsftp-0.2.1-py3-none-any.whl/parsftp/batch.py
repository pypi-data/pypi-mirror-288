# pylint: disable=missing-module-docstring
import subprocess
import typing

class Batch:
    """Class that represents a batch.

    Args:
        name: The name of this batch.
        input_paths: The list of paths to transfer.
        output_dir: The destination folder, on the destination host, where to
        put the files.
    """

    def __init__(self, name: str, input_paths: typing.List[str],
                 output_dir: str):
        self._name = name
        self._status: int | None = None
        self._proc: subprocess.Popen[bytes] | None = None
        self._input_paths = input_paths
        self._output_dir = output_dir

    @property
    def name(self) -> str:
        """The name of this batch."""
        return self._name

    @property
    def input_paths(self) -> typing.List[str]:
        """The list of paths to transfer."""
        return self._input_paths

    @property
    def output_dir(self) -> str:
        """The destination folder on the host."""
        return self._output_dir

    @property
    def status(self) -> int | None:
        """The status of the transfer.

        Returns:
            None if the transfer was never started or is not completed.
            Otherwise the status number of the completed transfer.
        """
        return self._status

    @status.setter
    def status(self, s: int) -> None:
        """Sets the status of the completed transfer."""
        self._status = s

    @property
    def proc(self) -> subprocess.Popen[bytes] | None:
        """The process of the transfer."""
        return self._proc

    @proc.setter
    def proc(self, p: subprocess.Popen[bytes]) -> None:
        """Sets the process of the transfer."""
        self._proc = p
