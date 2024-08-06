"""Top-level package for SLURM Completed Logs Utils."""

__author__ = """Jaideep Sundaram"""
__email__ = 'jai.python3@gmail.com'
__version__ = '0.1.0'

from .parser import Parser as SlurmCompletedLogsParser # noqa F401
from .record import Record as SlurmCompletedLogsRecord # noqa F401
