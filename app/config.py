# for configuration settings
#import os

from datetime import timedelta
import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=server name;"
    "DATABASE=database name;"
    "UID=username;"
    "PWD=password;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Add Configurations
class Config:
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'

#  Add the JWT token location
    JWT_TOKEN_LOCATION = ['headers']  # Specifies that tokens are expected in headers
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Optional: Set token expiration time