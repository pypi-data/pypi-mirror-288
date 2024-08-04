# fs.rclonefs
# __init__.py
"""Pyfilesystem2 access to rclone remotes using rclone-python.
"""

from .rclone import Rclone
from .rclonefs import RcloneFS

__version__ = (
    __import__("pkg_resources")
    .resource_string(__name__,"_version.txt")
    .strip()
    .decode("ascii")
)
__author__ = "Raygan Henley"
__author_email__ = "raygan@raygan.com"
__license__ = "MIT"