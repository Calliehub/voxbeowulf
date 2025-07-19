"""
VoxBeowulf - Beowulf text processing and analysis tools.

A Python package for processing, validating, and analyzing Beowulf text data
from various sources including heorot.dk.
"""

__version__ = "1.0.0"
__author__ = "VoxBeowulf Team"
__description__ = "Beowulf text processing and analysis tools"

from .numbering import FITT_BOUNDARIES, LINE_NUMBER_MARKERS

__all__ = [
    "FITT_BOUNDARIES",
    "LINE_NUMBER_MARKERS",
]
