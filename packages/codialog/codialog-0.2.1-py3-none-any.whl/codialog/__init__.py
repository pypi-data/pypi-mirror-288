# Import necessary modules
from .app import create_app

# Public API of the package
__all__ = ['create_app']

# Version checking
from importlib.metadata import version, PackageNotFoundError

__version__ = "0.2.1"