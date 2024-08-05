""" Entrypoint for the CLI tools. """

from . import version_manager

print(__package__)
__all__ = ["version_manager"]
