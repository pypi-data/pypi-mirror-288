"""
Python Connector for Salesforce is a connectivity solution for accessing
Salesforce from Python applications to read and update data. It fully
implements the Python DB API 2.0 specification. The connector is distributed
as a wheel package for Windows, macOS, and Linux.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your Salesforce data just like you would normally work with
    relational databases. Simple queries are directly converted to Salesforce API
    calls and executed on the Salesforce side.
    Complex queries are transformed into simpler queries, which are then converted
    to Salesforce API calls. The embedded SQL engine then processes the results
    in the local cache and applies advanced SQL features from the original complex
    query.

Version: 1.1.0 

Homepage: https://www.devart.com/python/salesforce/
"""
from .salesforce import *
