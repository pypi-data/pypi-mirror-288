"""CLI for Parallel SFTP module."""

import argparse
import logging
import yaml

from .logger import configure_logging
from .parsftp import ParSftp

logger = logging.getLogger('parsftp')

def read_args() -> argparse.Namespace:
    """Parse command line arguments."""

    # Setup parser
    parser = argparse.ArgumentParser(description='Parallel SFTP.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # SFTP command
    parser.add_argument('-c', '--sftp-cmd', dest='sftp_cmd',
                        default="treesftp",
                        help="Path to the treesftp program.")

    # Input YAML
    parser.add_argument("-i", "--input", required=True,
                        help=("The YAML that describes the batches of files" +
                              "to transfer."))

    # Output YAML
    parser.add_argument("-o", "--output", required=True,
                        help=("The output YAML containing the list of input"
                              " batches and their corresponding status."))

    # Logging
    parser.add_argument('-q', dest='quiet', action='store_true',
        help='Set verbose level to 0.')
    parser.add_argument('--log-file', dest='log_file', required=False,
                        help='Path to a log file.')
    parser.add_argument('-v', action='count', dest='verbose', default=1,
        help='Set verbose level.')

    # SFTP arguments
    parser.add_argument('sftp_args', nargs=argparse.REMAINDER)

    # Parse
    args = parser.parse_args()

    if args.quiet:
        args.verbose = 0

    return args

def main() -> int:
    """CLI (Command Line Interface) function."""

    status = 0

    # Get command line arguments
    args = read_args()

    # Configure logging
    configure_logging(args.verbose, args.log_file)
    logger.debug("Arguments: %s", args)

    try:
        # Run transfer
        trans = ParSftp.from_yaml(args.input)
        trans.run(sftp_cmd = args.sftp_cmd, sftp_args = args.sftp_args[1:])
        status = trans.status

        # Write YAML output
        with open(args.output, "w", encoding="utf8") as f:
            yaml.safe_dump_all([trans.get_batch_statuses()], f,
                               explicit_start=True)

    except Exception as e: # pylint: disable=broad-exception-caught
        logger.fatal("Exception occured: %s", e)
        status = 1

    return status
