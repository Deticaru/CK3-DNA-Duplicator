# Functions package for DNA Duplicator
# This file makes the functions directory a Python package

from .dd_duplicator import duplicate_dna
from .dd_output import copy_to_clipboard, get_from_clipboard

# Exportar las funciones principales para fácil acceso
__all__ = ['duplicate_dna', 'copy_to_clipboard', 'get_from_clipboard']
