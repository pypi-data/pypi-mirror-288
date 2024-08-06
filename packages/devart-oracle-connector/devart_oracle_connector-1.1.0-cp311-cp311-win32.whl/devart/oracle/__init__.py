"""
Python Connector for Oracle is a connectivity solution for accessing Oracle
databases from Python applications. It fully implements the Python DB API 2.0
specification. The connector is distributed as a wheel package for Windows,
macOS, and Linux.
 
Direct connection

    The connector enables you to establish a direct connection to Oracle from
    a Python application via TCP/IP, eliminating the need for the database client
    libraries. A direct connection increases the speed of data transmission
    between the application and Oracle database server and streamlines
    the deployment process since you don't have to distribute any client
    libraries with the application.
 
Secure communication

    The connector supports encrypted communications using SSL/TLS, SSH tunneling,
    and HTTP/HTTPS tunneling.

Version: 1.1.0 

Homepage: https://www.devart.com/python/oracle/
"""
from .oracle import *
