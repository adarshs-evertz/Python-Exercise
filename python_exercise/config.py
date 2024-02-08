"""
Global Config
=============
"""
from os import getenv

# Loads Configuration from environment variable;
# .. envvar:: TABLE_NAME
#     A string specifying the name of the DynamoDB table to use
#     The table should exist in the specified deployment environment
TABLE_NAME = getenv("DYNAMODB_TABLE", "python-exercise")
