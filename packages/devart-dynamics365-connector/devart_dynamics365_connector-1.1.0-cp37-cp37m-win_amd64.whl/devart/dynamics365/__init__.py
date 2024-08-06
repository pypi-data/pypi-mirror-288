"""
Python Connector for Dynamics 365 is a connectivity solution for accessing
Dynamics 365 Customer Engagement (formerly Dynamics CRM) from Python
applications to read and update data. It fully implements the Python DB API
2.0 specification. The connector is distributed as a wheel package
for Windows, macOS, and Linux.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your Dynamics 365 data just like you would normally work
    with relational databases. Simple queries are directly converted to Dynamics
    365 API calls and executed on the Dynamics 365 side.
    Complex queries are transformed into simpler queries, which are then converted
    to Dynamics 365 API calls. The embedded SQL engine then processes the results
    in the local cache and applies advanced SQL features from the original complex
    query.

Version: 1.1.0 

Homepage: https://www.devart.com/python/dynamics365/
"""
from .dynamics365 import *
