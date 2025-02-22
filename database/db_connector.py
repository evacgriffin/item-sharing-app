"""
This code has been adapted from the following source:

flask-starter-app/database/db_connector.py
Retrieved on: 02/21/2025
URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py
"""

import MySQLdb

# TODO: Swap these parameters to your database
# You could also try to use the db_credentials, the db_connector.py file on the flask starter app shows an example
def connect_to_database(host = 'localhost', user = 'eva', passwd = 'eva', db = 'cs340'):
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
    db_connection.commit();

    return cursor