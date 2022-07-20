"""
Module containing a dynamic reference to the absolute path of the root directory of the repository on any user's
operating system.
Sub-directories can then be accessed, for example, by: directory_path = ROOT_PATH / "game" / "app"
"""

# Standard library imports
from pathlib import Path

ROOT_PATH = Path(__file__).parent
