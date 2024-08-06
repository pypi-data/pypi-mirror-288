"""
Python Connector for HubSpot is a connectivity solution for accessing HubSpot
from Python applications to read and update data. It fully implements
the Python DB API 2.0 specification. The connector is distributed as a wheel
package for Windows and Windows Server.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your HubSpot data just like you would normally work with
    relational databases. Simple queries are directly converted to HubSpot API
    calls and executed on the HubSpot side.
    Complex queries are transformed into simpler queries, which are then converted
    to HubSpot API calls. The embedded SQL engine then processes the results
    in the local cache and applies advanced SQL features from the original complex
    query.

Version: 1.1.0 

Homepage: https://www.devart.com/python/hubspot/
"""
from .hubspot import *
