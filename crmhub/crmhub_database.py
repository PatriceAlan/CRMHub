import mysql.connector
import os
from dotenv import load_dotenv

# Intialise environment variables
load_dotenv()

database = mysql.connector.connect(
    host = 'localhost',
    user = os.getenv('DATABASE_USER'),
    passwd = os.getenv('DATABASE_PASS')

)

# prepare a cursor object
cursorObject = database.cursor()

# create a database
cursorObject.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME')}")

print("Database created !")