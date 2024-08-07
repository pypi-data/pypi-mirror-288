import importlib.metadata
from .utils import Monkey

# get version from toml, or use dev placeholder if running from local files
try:
    __version__ = importlib.metadata.version("psychopy-monkeys")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.dev"

__all__ = [
    "Monkey",
]