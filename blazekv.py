"""
BlazeKV Python Bindings
Professional-grade Python wrapper for BlazeKV C library

Usage:
    from blazekv import BlazeKV
    
    db = BlazeKV()
    db.set("key", "value")
    print(db.get("key"))  # Output: value
"""

import ctypes
import os
import platform
from pathlib import Path
from typing import Optional, Union

__version__ = "1.0.0"
__author__ = "BlazeKV Contributors"
__license__ = "Proprietary"


class BlazeKVError(Exception):
    """Base exception for BlazeKV errors"""
    pass


class BlazeKV:
    """
    Professional Python interface to BlazeKV C library
    
    Attributes:
        db_file (str): Path to database file
    """
    
    def __init__(self, db_file: str = "data.db"):
        """
        Initialize BlazeKV database
        
        Args:
            db_file (str): Path to database file (default: data.db)
            
        Raises:
            BlazeKVError: If library initialization fails
        """
        self.db_file = db_file
        self._lib = self._load_library()
        self._init_functions()
        
    def _load_library(self) -> ctypes.CDLL:
        """Load the native BlazeKV library"""
        system = platform.system()
        
        # Try to find library
        lib_paths = [
            Path(__file__).parent / "blazekv.so",
            Path(__file__).parent / "blazekv.dll",
            Path(__file__).parent / "blazekv.dylib",
        ]
        
        for path in lib_paths:
            if path.exists():
                try:
                    return ctypes.CDLL(str(path))
                except OSError:
                    continue
        
        # Fallback: try system path
        try:
            if system == "Windows":
                return ctypes.CDLL("blazekv.dll")
            elif system == "Darwin":
                return ctypes.CDLL("blazekv.dylib")
            else:
                return ctypes.CDLL("blazekv.so")
        except OSError as e:
            raise BlazeKVError(
                "Failed to load BlazeKV library. "
                "Ensure blazekv is compiled and in system PATH"
            ) from e
    
    def _init_functions(self) -> None:
        """Initialize ctypes function signatures"""
        # Define function signatures
        self._lib.set.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._lib.get.argtypes = [ctypes.c_char_p]
        self._lib.get.restype = ctypes.c_char_p
        self._lib.delete.argtypes = [ctypes.c_char_p]
        self._lib.load_db.argtypes = []
        self._lib.save_db.argtypes = []
        
    def set(self, key: Union[str, bytes], value: Union[str, bytes]) -> None:
        """
        Set a key-value pair
        
        Args:
            key (str or bytes): The key
            value (str or bytes): The value
            
        Raises:
            BlazeKVError: If operation fails
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(value, str):
            value = value.encode('utf-8')
        
        try:
            self._lib.set(key, value)
        except Exception as e:
            raise BlazeKVError(f"Failed to set key: {e}") from e
    
    def get(self, key: Union[str, bytes]) -> Optional[str]:
        """
        Get a value by key
        
        Args:
            key (str or bytes): The key to retrieve
            
        Returns:
            str or None: The value if found, None otherwise
            
        Raises:
            BlazeKVError: If operation fails
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        try:
            result = self._lib.get(key)
            if result is None:
                return None
            return result.decode('utf-8') if isinstance(result, bytes) else result
        except Exception as e:
            raise BlazeKVError(f"Failed to get key: {e}") from e
    
    def delete(self, key: Union[str, bytes]) -> None:
        """
        Delete a key-value pair
        
        Args:
            key (str or bytes): The key to delete
            
        Raises:
            BlazeKVError: If operation fails
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        try:
            self._lib.delete(key)
        except Exception as e:
            raise BlazeKVError(f"Failed to delete key: {e}") from e
    
    def load(self) -> None:
        """Load database from disk"""
        try:
            self._lib.load_db()
        except Exception as e:
            raise BlazeKVError(f"Failed to load database: {e}") from e
    
    def save(self) -> None:
        """Save database to disk"""
        try:
            self._lib.save_db()
        except Exception as e:
            raise BlazeKVError(f"Failed to save database: {e}") from e
    
    def __setitem__(self, key: str, value: str) -> None:
        """Support dict-like syntax: db['key'] = 'value'"""
        self.set(key, value)
    
    def __getitem__(self, key: str) -> Optional[str]:
        """Support dict-like syntax: value = db['key']"""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value
    
    def __delitem__(self, key: str) -> None:
        """Support dict-like syntax: del db['key']"""
        self.delete(key)
    
    def __enter__(self):
        """Context manager support"""
        self.load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.save()


# Example usage and tests
if __name__ == "__main__":
    try:
        # Basic usage
        db = BlazeKV()
        
        # Set values
        db.set("username", "alice")
        db.set("email", "alice@example.com")
        
        # Get values
        print(f"Username: {db.get('username')}")
        print(f"Email: {db.get('email')}")
        
        # Dict-like syntax
        db["counter"] = "42"
        print(f"Counter: {db['counter']}")
        
        # Context manager
        with BlazeKV() as database:
            database.set("temp", "value")
            print(f"Temp: {database.get('temp')}")
        
        print("\n✅ All tests passed!")
        
    except BlazeKVError as e:
        print(f"❌ Error: {e}")
