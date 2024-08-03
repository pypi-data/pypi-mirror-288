""""Infomark Terminal CLI entry point."""

import sys

from infomark_cli.utils.logging_utils import change_logging_context, reset_logging_context


def main():
    """Entry point for the Infomark Terminal command-line interface."""
    print("Initializing...\n")  # noqa: T201

    # pylint: disable=import-outside-toplevel
    from infomark_cli.config.setup import initialize
    from infomark_cli.controllers.command_controller import execute

    initialize()

    is_dev_mode = "--dev" in sys.argv[1:]
    is_debug_mode = "--debug" in sys.argv[1:]

    execute(is_dev_mode, is_debug_mode)


if __name__ == "__main__":
    initial_logging_context = change_logging_context()
    try:
        main()
    except Exception:
        pass
    finally:
        reset_logging_context(initial_logging_context)
