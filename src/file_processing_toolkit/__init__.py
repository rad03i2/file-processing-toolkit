"""File Processing Toolkit public API."""
from .core import FileRecord, scan, hash_file, find_duplicates, plan_rename, apply_rename

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed (@rad03i2)"
__all__ = ["FileRecord", "scan", "hash_file", "find_duplicates", "plan_rename", "apply_rename"]
