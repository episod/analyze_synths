"""
Command-line interface for the audio analysis toolkit.

This package provides the CLI interface for the audio analysis toolkit,
allowing users to run analysis from the command line with various options
and configurations.
"""

from .main import main, parse_arguments

__all__ = ['main', 'parse_arguments']