import argparse
import sys
from typing import NoReturn, Sequence

from incremental_backup._utility import print_error
from incremental_backup.cli.command import (
    COMMAND_CLASSES,
    CommandArgumentError,
    CommandError,
    get_command_class,
)

__all__ = ["cli_entrypoint", "cli_main"]


def cli_entrypoint() -> NoReturn:
    """Process-level entrypoint of the incremental backup program.
    Collects arguments from `sys.argv`, performs all processing, then terminates the process with `sys.exit()`."""

    exit_code = cli_main(sys.argv)
    sys.exit(exit_code)


def cli_main(arguments: Sequence[str], /) -> int:
    """Intermediate entrypoint function which may be handy for testing purposes.

    :param arguments: The program command line arguments.
    :return: Process exit code.
    """

    # Strip off the "program name" argument.
    arguments = arguments[1:]

    try:
        arg_parser = _get_argument_parser()
        parsed_arguments = arg_parser.parse_args(arguments)
        command_class = get_command_class(parsed_arguments.command)
        command_instance = command_class(parsed_arguments)
        command_instance.run()
        return EXIT_CODE_SUCCESS
    except CommandArgumentError as e:
        if e.usage is None:  # TODO: (breaking) remove when usage is removed
            arg_parser.print_usage(sys.stderr)
        else:
            print(e.usage, file=sys.stderr)
        print()
        print(f"{arg_parser.prog}: error: {e.message}", file=sys.stderr)
        return EXIT_CODE_INVALID_ARGUMENTS
    except CommandError as e:
        print_error(str(e))
        return EXIT_CODE_GENERAL_ERROR
    except Exception as e:
        print_error(f"Unhandled exception: {repr(e)}")
        return EXIT_CODE_LOGIC_ERROR


def _get_argument_parser() -> argparse.ArgumentParser:
    """Creates the command line argument parser. Adds subparsers for each command."""

    arg_parser = _ArgumentParser("incremental_backup", description="Incremental backup tool.")
    arg_subparser = arg_parser.add_subparsers(title="commands", required=True, dest="command")

    for cls in COMMAND_CLASSES:
        cls.add_arg_subparser(arg_subparser)

    return arg_parser


class _ArgumentParser(argparse.ArgumentParser):
    """Custom `argparse.ArgumentParser` implementation so we can throw exceptions for invalid arguments instead of
    exiting the process."""

    def error(self, message: str) -> NoReturn:
        raise CommandArgumentError(message)


# Process exit codes.
EXIT_CODE_SUCCESS = 0
EXIT_CODE_INVALID_ARGUMENTS = 1
EXIT_CODE_GENERAL_ERROR = 2
EXIT_CODE_LOGIC_ERROR = -1
