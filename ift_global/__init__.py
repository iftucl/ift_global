from __future__ import annotations

import importlib
import typing

__version__ = "0.0.0"
__version_tuple__ = (0, 0, 0)

__doc__ = """
ift_global python package
=========================

Python package developed and maintained by Big Data in Quantitative Finance
Institute for Finance and Technology - University College London.


Public API
----------

Main Features:

- ReadConfig: standardise the way we read config files
- MinioFileSystemRepo: generic abstraction for file operations on Minio

"""

from ift_global.utils.read_yaml import ReadConfig
from ift_global.connectors.minio_fileops import MinioFileSystemRepo

__all__ = [
    "ReadConfig",
    "MinioFileSystemRepo",
]