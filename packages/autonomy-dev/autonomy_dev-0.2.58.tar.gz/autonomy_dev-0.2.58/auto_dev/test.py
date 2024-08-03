"""
Module for testing the project.
"""
from auto_dev.cli_executor import CommandExecutor


def test_path(
    path: str,
    verbose: bool = False,
    watch: bool = False,
) -> bool:
    """
    Check the path for linting errors.
    :param path: The path to check
    """
    command = CommandExecutor(
        [
            "poetry",
            "run",
            "pytest",
            str(path),
            "-vv",
        ]
        + (["-ff"] if watch else [])
    )
    result = command.execute(verbose=verbose, stream=True)
    return result
