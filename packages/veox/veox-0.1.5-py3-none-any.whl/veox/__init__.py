from .client import init, RemoteModel, VeoxServiceUnavailable
from .client import DataProtector  # Add this line

__all__ = ['init', 'RemoteModel', 'VeoxServiceUnavailable', 'DataProtector']  # Update this line
__version__ = "0.1.5"  # Increment the version number
