# pylint: disable=missing-module-docstring
import logging
import subprocess
import time
import typing
import yaml

import schema  # type: ignore[import-untyped]

from .batch import Batch

logger = logging.getLogger('parsftp')

SCHEMA_INPUT_YAML = schema.Schema({
    str: {
        "input": [str],
        "output": str
    }
})

def create_sftp_proc(sftp_cmd: str, sftp_args: typing.List[str],
                     inpaths: typing.List[str], outdir: str,
                     ) -> subprocess.Popen[bytes]:
    """Creates a new process and runs an SFTP transfer in it."""
    cmd = [sftp_cmd, '-o', outdir] + inpaths + sftp_args
    logger.debug("Run transfer: %s", cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE)

class ParSftp:
    """Class that implements parallel SFTP.

    This implementation uses an external SFTP program (treesftp).
    """

    def __init__(self) -> None:
        self._batches: typing.Dict[str, Batch] = {}

    @classmethod
    def from_yaml(cls, file: str) -> typing.Self:
        """Builds a ParSftp instance from YAML input.

        Args:
            file: Path to the YAML file.

        Returns: 
            A ParSftp object.
        """

        trans = cls()

        # Load list of batches
        with open(file, "r", encoding="utf8") as f:
            batch_docs = list(yaml.safe_load_all(f))

        # Loop on all batch defintions
        for batches in batch_docs:

            # Validate schema
            SCHEMA_INPUT_YAML.validate(batches)

            # Loop on batches
            for name, batch in batches.items():

                trans.add_batch(Batch(name, input_paths = batch['input'],
                                      output_dir = batch['output']))

        return trans

    def add_batch(self, batch: Batch) -> None:
        """Adds a batch to transfer.

        Args:
            batch: a Batch object.

        Returns:
            Nothing.
        """

        if batch.name in self._batches:
            raise RuntimeError(f"Batch name \"{batch.name}\" is duplicated.")

        self._batches[batch.name] = batch

    @property
    def status(self) -> int:
        """The status of the whole transfer.

        0 if transfer was successful, 1 otherwise (not started or failure).
        """

        status = 0

        # Loop on all batches
        for batch in self._batches.values():

            # If any batch was not terminated or failed we must return failure
            if batch.status is None or batch.status != 0:
                status = 1
                break

        return status

    def get_batch_statuses(self) -> typing.Dict[str, int]:
        """Get the statuses of all batches.

        Returns:
            A dictionary with batch names as keys, and their statuses as values.
        """

        statuses: typing.Dict[str, int] = {}

        # Loop on all batches
        for batch in self._batches.values():
            statuses[batch.name] = 255 if batch.status is None else batch.status

        return statuses

    def run(self, sftp_cmd: str = "treesftp",
            sftp_args: typing.List[str] | None = None,
            sleep_time: float = 0.1) -> None:
        """Run the batch transfers.

        Args:
            sftp_cmd: The SFTP command to run.
            sftp_args: Arguments to pass to the SFTP command, at each call.
            sleep_time: Time to wait after checking status of SFTP commands, if
                        at least one has not terminated.

        Returns:
            Nothing.
        """

        # Loop on all batches
        for batch in self._batches.values():

            # Start transfer
            batch.proc = create_sftp_proc(
                    sftp_cmd, [] if sftp_args is None else sftp_args,
                    inpaths=batch.input_paths, outdir=batch.output_dir)

        # Wait for all processes to return
        done = False
        while not done:
            done = True

            # Check status of each batch
            for batch in self._batches.values():
                if batch.status is None and not batch.proc is None:
                    status = batch.proc.poll()
                    if status is None:
                        done = False
                    else:
                        batch.status = status

                # Wait some time
                if not done:
                    time.sleep(sleep_time)
