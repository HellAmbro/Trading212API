from rich.console import Console

_console = Console()


def log(msg: str) -> None:
    """Takes a string and logs it to the console.

    Args:
        msg (str): The message to log.
    """
    _console.log(msg)
