# oaieval/__init__.py

__version__ = "1.0.6"

# Import the main function to be easily accessible
from .main import main

# Define what should be accessible when `from oaieval import *` is used
__all__ = ["main"]

print("Initializing oaieval package")
