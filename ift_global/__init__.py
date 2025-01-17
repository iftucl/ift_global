from __future__ import annotations

import importlib
import typing

__version__ = "0.0.0"
__version_tuple__ = (0, 0, 0)

__doc__ = """
ift_global
=======================================================================



"""

from ift_global.utils.read_yaml import ReadConfig
from connectors.minio_fileops import MinioFileSystemRepo
__all__ = [
    "ReadConfig",
    "MinioFileSystemRepo",
]