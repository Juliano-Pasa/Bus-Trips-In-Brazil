import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

def GetDefaultConnection():
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def ExecuteQuery(query, cur, conn, data=None):
    try:
        cur.execute(query, data)
    except Exception as e:
        conn.rollback()
        raise e
    
def ExecuteValues(query, cur, conn, data):
    try:
        execute_values(cur, query, data)
    except Exception as e:
        conn.rollback()
        raise e        

def WriteBatchToDB(batch, tableName, cur, conn):
    valuePlaceHolders = ", ".join(["%s"] * len(batch[0]))
    query = f"INSERT INTO {tableName} VALUES ({valuePlaceHolders});"

    for entry in batch:
        ExecuteQuery(query, cur, conn, entry)