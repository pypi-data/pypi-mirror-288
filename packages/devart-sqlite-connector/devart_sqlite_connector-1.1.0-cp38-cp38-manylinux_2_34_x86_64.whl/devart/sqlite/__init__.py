"""
Python Connector for SQLite is a connectivity solution for accessing SQLite
databases from Python applications. It fully implements the Python DB API 2.0
specification. The connector is distributed as a wheel package for Windows,
macOS, and Linux.
 
Direct connection

    The connector supports two SQLite library linking modes: static linking and
    dynamic linking. Static linking enables a direct connection to SQLite, so you
    don't have to deploy the SQLite libraries on user workstations. You can use
    the built-in encryption capabilities in the Direct mode to protect your data
    from unauthorized access?the statically linked library provides SQLite
    database encryption without requiring you to purchase an encryption extension.

Version: 1.1.0 

Homepage: https://www.devart.com/python/sqlite/
"""
from .sqlite import *
