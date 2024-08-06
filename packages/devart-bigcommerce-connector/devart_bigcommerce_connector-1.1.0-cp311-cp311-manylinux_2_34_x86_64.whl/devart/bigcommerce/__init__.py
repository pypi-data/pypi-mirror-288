"""
Python Connector for BigCommerce is a connectivity solution for accessing
BigCommerce from Python applications to read and update data. It fully
implements the Python DB API 2.0 specification. The connector is distributed
as a wheel package for Windows, macOS, and Linux.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your BigCommerce data just like you would normally work
    with relational databases. Simple queries are directly converted
    to BigCommerce API calls and executed on the BigCommerce side.
    Complex queries are transformed into simpler queries, which are then converted
    to BigCommerce API calls. The embedded SQL engine then processes the results
    in the local cache and applies advanced SQL features from the original complex
    query.

Version: 1.1.0 

Homepage: https://www.devart.com/python/bigcommerce/
"""
from .bigcommerce import *
