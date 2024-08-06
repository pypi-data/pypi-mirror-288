"""
Python Connector for xBase is a connectivity solution for accessing FoxPro,
Visual FoxPro, dBase, and other databases in DBF file formats from Python
applications. It fully implements the Python DB API 2.0 specification.
The connector is distributed as a wheel package for Windows, macOS, and Linux.
 
Direct connection

    The connector enables you to establish a direct connection to Visual FoxPro,
    dBase, and other xBase databases eliminating the need for the client library.
    A direct connection increases the speed of data transmission between a Python
    application and an xBase database and simplifies the deployment.
 
Local indexing

    The connector offers an internal data indexing mechanism that is way more
    efficient than native DBF indexes for complex queries.
 
Retrieval of corrupted data

    You can choose to ignore corrupted data and metadata errors in DBF tables.
    Corrupted data is skipped, while intact data is properly retrieved.

Version: 1.1.0 

Homepage: https://www.devart.com/python/xbase/
"""
from .xbase import *
