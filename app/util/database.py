import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.environ.get('DATABASE_URL')

if not DB_URI:
    raise RuntimeError("DatabaseURI_Not_present")

# Global connection and cursor
connection = psycopg2.connect(DB_URI)
cursor = connection.cursor()

def ConnectDB():
    global connection, cursor
    if not DB_URI:
        raise RuntimeError("DatabaseURI_Not_present")
    # psycopg2 connection is open if .closed == 0
    
    connection = psycopg2.connect(DB_URI)
    cursor = connection.cursor()
    
    return cursor, connection
