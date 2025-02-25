"""
This code has been adapted from the following sources:

flask-starter-app/database/db_connector.py
Retrieved on: 02/21/2025
URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py
"""

import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set application variables
HOST = os.getenv("340DBHOST")
USER = os.getenv("340DBUSER")
PW = os.getenv("340DBPW")
DB = os.getenv("340DB")


def connect_to_database(host = HOST, user = USER, passwd = PW, db = DB):
    '''
    Connects to a database and returns a database object
    '''
    db_connection = MySQLdb.connect(host,user,passwd,db)
    return db_connection


def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    Executes a given SQL query on the given db connection and returns a Cursor object.
    '''

    if db_connection is None:
        print("No database connection!")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty!")
        return None

    print(f"Executing {query} with {query_params}...")
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    #TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)

    # Commits changes to the database
    db_connection.commit()

    return cursor