import os
from datetime import timedelta
import urllib

# Retrieve the connection string from the environment variable
connection_string = os.getenv('DB_CONNECTION_STRING')
#print(connection_string)

# URL encode the connection string
params = urllib.parse.quote_plus(connection_string)

# Add Configurations
class Config:
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'

    # Add the JWT token location
    JWT_TOKEN_LOCATION = ['headers']  # Specifies that tokens are expected in headers
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Optional: Set token expiration time
