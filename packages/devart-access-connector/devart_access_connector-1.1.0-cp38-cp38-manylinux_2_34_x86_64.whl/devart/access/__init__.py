"""
Python Connector for Microsoft Access is a connectivity solution for accessing
Microsoft Access databases from Python applications. It fully implements
the Python DB API 2.0 specification. The connector is distributed as a wheel
package for Windows, macOS, and Linux.
 
Direct connection

    Python offers a standard pyodbc module, which you can use to access Microsoft
    Access databases through the Microsoft Access ODBC Driver. This method has
    several disadvantages:
    - Microsoft offers Access ODBC drivers only for the Windows platform.
    - Users might experience issues opening databases created in the latest
    versions of Microsoft Access.
    - Users have to install either Microsoft Access or Microsoft Access Database
    Engine Redistributable on their machine.
    - By default, Microsoft Access is a single-user database system. An Access
    database cannot be opened concurrently in multiple applications.
    Our connector provides the following advantages:
    - A direct access to a database without installing Microsoft Access or
    Microsoft Access Database Engine Redistributable on the user's machine
    - Support for all major desktop platforms: Windows, macOS, and Linux
    - Support for the .mdb and .accdb file formats, including databases created
    in the latest Microsoft Access versions
    - A read-only multi-user mode to enable several users to read data from
    a database simultaneously

Version: 1.1.0 

Homepage: https://www.devart.com/python/access/
"""
from .access import *
