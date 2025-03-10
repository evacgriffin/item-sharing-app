"""
This code has been adapted from the following source:

flask-starter-app
Retrieved on: 02/08/2025
URL: https://github.com/osu-cs340-ecampus/flask-starter-app
"""

import database.db_connector as db
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, json
from flask_mysqldb import MySQL
import os

# Configuration

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Set application variables
APP_MYSQL_HOST = os.getenv("APP_MYSQL_HOST")
APP_MYSQL_USER = os.getenv("APP_MYSQL_USER")
APP_MYSQL_PASSWORD = os.getenv("APP_MYSQL_PASSWORD")
APP_MYSQL_DB_NAME = os.getenv("APP_MYSQL_DB_NAME")
APP_PORT = int(os.getenv("PORT", 4282))


def connect():
    # Connect to the database
    db_connection = db.connect_to_database(APP_MYSQL_HOST, APP_MYSQL_USER, APP_MYSQL_PASSWORD, APP_MYSQL_DB_NAME)
    return db_connection


# Routes

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/users', methods=["POST", "GET"])
def users():
    # Create a new User
    if request.method == "POST":
        if request.form.get("add_user"):
            # Get user form inputs
            user_name = request.form["user_name"]
            password = request.form["password"]
            email = request.form["email"]
            if not request.form.get("neighborhood"):
                user_add_query = ('INSERT INTO Users '
                                    '(userName, password, email) '
                                  'VALUES '
                                    '(%s, %s, %s);')
                query_params = (user_name, password, email, )
            else:
                neighborhood = request.form["neighborhood"]
                user_add_query = ('INSERT INTO Users '
                                    '(userName, password, email, neighborhoodID) '
                                'VALUES '
                                    '(%s, %s, %s, (SELECT neighborhoodID FROM Neighborhoods WHERE neighborhoodName = %s));')
                query_params = (user_name, password, email, neighborhood, )
            print(user_add_query)
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=user_add_query, query_params=query_params )

        return redirect('/users')

    # Get the Users data for display
    if request.method == "GET":
        users_get_query = ('SELECT '
                               'Users.userID AS "User ID", '
                               'Users.username AS Username, '
                               'Users.password AS Password, '
                               'Users.email AS Email, '
                               'Neighborhoods.neighborhoodName AS "Neighborhood" '
                           'FROM Users '
                           'LEFT JOIN Neighborhoods ON Users.neighborhoodID = Neighborhoods.neighborhoodID;')
        neighborhoods_get_query = 'SELECT neighborhoodName FROM Neighborhoods;'
        with connect() as db_connection:
            users_cursor = db.execute_query(db_connection=db_connection, query=users_get_query)
            neighborhoods_cursor = db.execute_query(db_connection=db_connection, query=neighborhoods_get_query)
            users_query_results = users_cursor.fetchall()
            neighborhoods_query_results = neighborhoods_cursor.fetchall()
            return render_template("users.j2", users=users_query_results, neighborhoods=neighborhoods_query_results)

# Route for updating the selected User
@app.route('/edit_users/<int:id>', methods=["POST", "GET"])
def edit_users(id):
    print(f"Received request for id: {id}")

    # Get data for the User with the specified id
    if request.method == "GET":
        user_get_query = ('SELECT '
                               'Users.userID AS "User ID", '
                               'Users.username AS Username, '
                               'Users.password AS Password, '
                               'Users.email AS Email, '
                               'Neighborhoods.neighborhoodName AS "Neighborhood" '
                            'FROM Users '
                           'LEFT JOIN Neighborhoods ON Users.neighborhoodID = Neighborhoods.neighborhoodID '
                            'WHERE userID = %s;')
        neighborhoods_get_query = 'SELECT neighborhoodName FROM Neighborhoods;'
        with connect() as db_connection:
            user_cursor = db.execute_query(db_connection=db_connection, query=user_get_query, query_params=(id,))
            neighborhoods_cursor = db.execute_query(db_connection=db_connection, query=neighborhoods_get_query)
            user_query_results = user_cursor.fetchall()
            neighborhoods_query_results = neighborhoods_cursor.fetchall()
            print(f"Query results: {user_query_results}")
            return render_template("edit_users.j2", user=user_query_results, neighborhoods=neighborhoods_query_results)

    # Update the User with the specified id
    if request.method == "POST":
        # Get form input
        user_name = request.form["user_name"]
        password = request.form["password"]
        email = request.form["email"]
        if not request.form.get("neighborhood"):
            query_params = (user_name, password, email, id,)
            # Execute the query to update the User
            user_update_query = ('UPDATE Users '
                                    'SET '
                                    'userName = %s, '
                                    'password = %s, '
                                    'email = %s, '                                 
                                    'neighborhoodID = NULL '
                                 'WHERE userID = %s;')
        else:
            neighborhood = request.form["neighborhood"]
            query_params = (user_name, password, email, neighborhood, id,)
            user_update_query = ('UPDATE Users '
                                    'SET '
                                    'userName = %s, '
                                    'password = %s, '
                                    'email = %s, '                                 
                                    'neighborhoodID = (SELECT neighborhoodID FROM Neighborhoods WHERE neighborhoodName = %s) '
                                 'WHERE userID = %s;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=user_update_query, query_params=query_params )

        return redirect('/users')

# Route for deleting the selected Item
@app.route('/delete_users/<int:id>')
def delete_users(id):
    # Delete the Item with the specified id
    users_delete_query = 'DELETE FROM Users WHERE userID = %s;'
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=users_delete_query, query_params=(id,))

    return redirect('/users')

@app.route('/items', methods=["POST", "GET"])
def items():
    # Create a new Item
    if request.method == "POST":
        if request.form.get("add_item"):
            # Get user form inputs
            item_name = request.form["item_name"]
            category_name = request.form["category_name"]
            item_add_query = ('INSERT INTO Items '
                                '(itemName, categoryID) '
                            'VALUES '
                                '(%s, (SELECT categoryID FROM ItemCategories WHERE categoryName = %s));')
            print(item_add_query)
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=item_add_query, query_params=(item_name, category_name, ))

        return redirect('/items')

    # Get the Items data for display
    if request.method == "GET":
        items_get_query = ('SELECT '
                                'Items.itemID AS "Item ID", '
                                'Items.itemName AS "Item Name", '
                                'ItemCategories.categoryName AS "Category Name" '
                            'FROM Items '
                            'JOIN ItemCategories ON Items.categoryID = ItemCategories.categoryID;')
        categories_get_query = 'SELECT categoryName FROM ItemCategories;'
        with connect() as db_connection:
            items_cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
            categories_cursor = db.execute_query(db_connection=db_connection, query=categories_get_query)
            items_query_results = items_cursor.fetchall()
            categories_query_results = categories_cursor.fetchall()
            return render_template("items.j2", items=items_query_results, categories=categories_query_results)

# Route for updating the selected Item
@app.route('/edit_items/<int:id>', methods=["POST", "GET"])
def edit_items(id):
    print(f"Received request for id: {id}")

    # Get data for the Item with the specified id
    if request.method == "GET":
        item_get_query = ('SELECT '
                                'Items.itemID AS "Item ID", '
                                'Items.itemName AS "Item Name", '
                                'ItemCategories.categoryName AS "Category Name" '
                            'FROM Items '
                            'JOIN ItemCategories ON Items.categoryID = ItemCategories.categoryID '
                            'WHERE itemID = %s;')
        categories_get_query = 'SELECT categoryName FROM ItemCategories;'
        with connect() as db_connection:
            item_cursor = db.execute_query(db_connection=db_connection, query=item_get_query, query_params=(id,))
            categories_cursor = db.execute_query(db_connection=db_connection, query=categories_get_query)
            item_query_results = item_cursor.fetchall()
            categories_query_results = categories_cursor.fetchall()
            print(f"Query results: {item_query_results}")
            return render_template("edit_items.j2", item=item_query_results, categories=categories_query_results)

    # Update the Item with the specified id
    if request.method == "POST":
        # Get form input
        item_name = request.form["item_name"]
        category_name = request.form["category_name"]

        # Execute the query to update the Item
        item_update_query = ('UPDATE Items '
                                'SET '
                                    'itemName = %s, '
                                    'categoryID = (SELECT categoryID FROM ItemCategories WHERE categoryName = %s) WHERE itemID = %s;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=item_update_query, query_params=(item_name, category_name, id,))

        return redirect('/items')

# Route for deleting the selected Item
@app.route('/delete_items/<int:id>')
def delete_items(id):
    # Delete the Item with the specified id
    items_delete_query = 'DELETE FROM Items WHERE itemID = %s;'
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=items_delete_query, query_params=(id,))

    return redirect('/items')

@app.route('/user_items', methods=["POST", "GET"])
def user_items():
    # Create a new User Item
    if request.method == "POST":
        if request.form.get("add_user_item"):
            # Get user form inputs
            item_name = request.form["item_name"]
            user_name = request.form["user_name"]
            user_item_add_query = ('INSERT INTO UserItems '
                                        '(userID, itemID) '
                                    'VALUES '
                                        '((SELECT userID FROM Users WHERE userName = %s), '
                                        '(SELECT itemID FROM Items WHERE itemName = %s));')
            print(user_item_add_query)
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=user_item_add_query, query_params=(user_name, item_name, ))

        return redirect('/user_items')

    # Get the User Items data for display
    if request.method == "GET":
        user_items_get_query = ('SELECT '
                                    'Users.userName AS "Username", '
                                    'Items.itemName AS "Item Name" '
                                'FROM UserItems '
                                'JOIN Users ON Users.UserID = UserItems.UserID '
                                'JOIN Items ON Items.itemID = UserItems.itemID;')
        users_get_query = 'SELECT userName FROM Users;'
        items_get_query = 'SELECT itemName FROM Items;'
        ids_get_query = 'SELECT userID, itemID FROM UserItems;'

        with connect() as db_connection:
            user_items_cursor = db.execute_query(db_connection=db_connection, query=user_items_get_query)
            users_cursor = db.execute_query(db_connection=db_connection, query=users_get_query)
            items_cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
            ids_cursor = db.execute_query(db_connection=db_connection, query=ids_get_query)
            ids_query_results = ids_cursor.fetchall()
            user_items_query_results = user_items_cursor.fetchall()
            users_query_results = users_cursor.fetchall()
            items_query_results = items_cursor.fetchall()
            return render_template("user_items.j2", user_items=user_items_query_results, users=users_query_results, items=items_query_results, ids=ids_query_results)


# Route to edit User Items
@app.route('/edit_user_items/<int:user_id>-<int:item_id>', methods=["POST", "GET"])
def edit_user_items(user_id, item_id):
    print(f"Received request for ids: {user_id}, {item_id}")

    # Get data for the User Item with the specified id
    if request.method == "GET":
        user_item_get_query = ('SELECT '
                                    'Users.userName AS "Username", '
                                    'Items.itemName AS "Item Name" '
                                'FROM UserItems '
                                'JOIN Users ON Users.UserID = UserItems.UserID '
                                'JOIN Items ON Items.itemID = UserItems.itemID '
                                'WHERE UserItems.userID = %s AND UserItems.itemID = %s '
                               'LIMIT 1;')
        users_get_query = 'SELECT userName FROM Users;'
        items_get_query = 'SELECT itemName FROM Items;'
        ids_get_query = ('SELECT userID, itemID FROM UserItems WHERE userID = %s AND itemID = %s;')

        with connect() as db_connection:
            user_item_cursor = db.execute_query(db_connection=db_connection, query=user_item_get_query, query_params=(user_id, item_id, ))
            users_cursor = db.execute_query(db_connection=db_connection, query=users_get_query)
            items_cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
            ids_cursor = db.execute_query(db_connection=db_connection, query=ids_get_query, query_params=(user_id, item_id, ))
            ids_query_results = ids_cursor.fetchall()
            user_item_query_results = user_item_cursor.fetchall()
            users_query_results = users_cursor.fetchall()
            items_query_results = items_cursor.fetchall()
            print(f"Query results: {user_item_query_results}")
            return render_template("edit_user_items.j2", user_item=user_item_query_results, users=users_query_results, items=items_query_results, ids=ids_query_results)

    # Update the User Item with the specified ids
    if request.method == "POST":
        # Get form input
        item_name = request.form["item_name"]
        user_name = request.form["user_name"]
        # Execute the query to update the Item
        user_item_update_query = ('UPDATE UserItems '
                                'SET '
                                    'itemID = (SELECT itemID from Items WHERE itemName = %s), '
                                    'userID = (SELECT userID FROM Users WHERE userName = %s) '
                                  'WHERE userID = %s AND itemID = %s '
                                  'LIMIT 1;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=user_item_update_query, query_params=(item_name, user_name, user_id, item_id))

        return redirect('/user_items')


# Route to delete User Item
@app.route('/delete_user_items/<int:user_id>-<int:item_id>')
def delete_user_items(user_id, item_id):
    # Delete the User Item with the specified ids
    user_items_delete_query = ('DELETE FROM UserItems '
                                    'WHERE userID = %s AND itemID = %s '
                               'LIMIT 1;')
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=user_items_delete_query, query_params=(user_id, item_id))

    return redirect('/user_items')


# Transfers Route
@app.route('/transfers', methods=["POST", "GET"])
def transfers():
    # Create a new Transfer
    if request.method == "POST":
        if request.form.get("add_transfer"):
            # Get user form inputs
            transfer_date_time = request.form["transfer_date_time"]
            lending_user_name = request.form["lending_user_name"]
            borrowing_user_name = request.form["borrowing_user_name"]
            transfer_add_query = ('INSERT INTO Transfers '
                                    '(transferDateTime, lendingUserID, borrowingUserID) '
                                'VALUES '
                                    '(%s, (SELECT userID FROM Users WHERE userName = %s), (SELECT userID FROM Users WHERE userName = %s));')
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=transfer_add_query, query_params=(transfer_date_time, lending_user_name, borrowing_user_name, ))

        return redirect('/transfers')


    # Get the Transfers data for display
    if request.method == "GET":
        # Source used as a reference for the following query that JOINs on the Users table twice:
        # Title: How to Join the Same Table Twice
        # Author: Marija Ilic
        # Retrieved On: 03/06/2025
        # URL: https://learnsql.com/blog/how-to-join-same-table-twice/
        transfers_get_query = ('SELECT '
                                    'TransferUsers.transferID AS "Transfer ID", '
                                    'TransferUsers.transferDateTime AS "Transfer Date and Time", '
                                    'LendingUsers.userName AS "Lending User", BorrowingUsers.userName AS "Borrowing User" '
                                'FROM Transfers AS TransferUsers '
                                'JOIN Users AS LendingUsers ON LendingUsers.userID = TransferUsers.lendingUserID '
                                'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = TransferUsers.borrowingUserID '
                                'ORDER BY TransferUsers.transferID;')
        lending_users_get_query = 'SELECT userName AS lendingUserName FROM Users;'
        borrowing_users_get_query = 'SELECT userName AS borrowingUserName FROM Users;'
        with connect() as db_connection:
            transfers_cursor = db.execute_query(db_connection=db_connection, query=transfers_get_query)
            lending_users_cursor = db.execute_query(db_connection=db_connection, query=lending_users_get_query)
            borrowing_users_cursor = db.execute_query(db_connection=db_connection, query=borrowing_users_get_query)
            transfers_query_results = transfers_cursor.fetchall()
            lending_users_query_results = lending_users_cursor.fetchall()
            borrowing_users_query_results = borrowing_users_cursor.fetchall()
            return render_template("transfers.j2", transfers=transfers_query_results, lending_users=lending_users_query_results, borrowing_users=borrowing_users_query_results)


# Route for updating the selected Transfer
@app.route('/edit_transfers/<int:id>', methods=["POST", "GET"])
def edit_transfers(id):
    print(f"Received request for id: {id}")

    # Get data for the Transfer with the specified id
    if request.method == "GET":
        transfer_get_query = ('SELECT '
                                    'TransferUsers.transferID AS "Transfer ID", '
                                    'TransferUsers.transferDateTime AS "Transfer Date and Time", '
                                    'TransferUsers.borrowingUserID, '
                                    'TransferUsers.lendingUserID '
                                'FROM Transfers AS TransferUsers '
                                'JOIN Users AS LendingUsers ON LendingUsers.userID = TransferUsers.lendingUserID '
                                'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = TransferUsers.borrowingUserID '
                                'WHERE TransferUsers.transferID = %s;')
        lending_users_get_query = 'SELECT userName AS lendingUserName FROM Users;'
        borrowing_users_get_query = 'SELECT userName AS borrowingUserName FROM Users;'
        with connect() as db_connection:
            transfer_cursor = db.execute_query(db_connection=db_connection, query=transfer_get_query, query_params=(id, ))
            lending_users_cursor = db.execute_query(db_connection=db_connection, query=lending_users_get_query)
            borrowing_users_cursor = db.execute_query(db_connection=db_connection, query=borrowing_users_get_query)
            transfer_query_results = transfer_cursor.fetchall()
            print(f"Transfer Query Results: {transfer_query_results}")
            lending_users_query_results = lending_users_cursor.fetchall()
            borrowing_users_query_results = borrowing_users_cursor.fetchall()
            return render_template("edit_transfers.j2", transfer=transfer_query_results, lending_users=lending_users_query_results, borrowing_users=borrowing_users_query_results)

    # Update the Transfer with the specified id
    if request.method == "POST":
        # Get form input
        transfer_date_time = request.form["transfer_date_time"]
        lending_user_name = request.form["lending_user_name"]
        borrowing_user_name = request.form["borrowing_user_name"]

        # Execute queries to get the userIDs
        with connect() as db_connection:
            lending_user_id_query = 'SELECT userID FROM Users WHERE userName = %s'
            borrowing_user_id_query = 'SELECT userID FROM Users WHERE userName = %s'
            lending_user_id_cursor = db.execute_query(db_connection=db_connection, query=lending_user_id_query, query_params=(lending_user_name, ))
            borrowing_user_id_cursor = db.execute_query(db_connection=db_connection, query=borrowing_user_id_query, query_params=(borrowing_user_name, ))
            lending_user_id = lending_user_id_cursor.fetchall()[0]['userID']
            borrowing_user_id = borrowing_user_id_cursor.fetchall()[0]['userID']

        # Execute the query to update the Transfer
        transfer_update_query = ('UPDATE Transfers '
                                    'SET transferDateTime = %s, lendingUserID = %s, borrowingUserID = %s '
                                    'WHERE transferID = %s;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=transfer_update_query, query_params=(transfer_date_time, lending_user_id, borrowing_user_id, id,))

        return redirect('/transfers')


# Route for deleting the selected Transfer
@app.route('/delete_transfers/<int:id>')
def delete_transfers(id):
    # Delete the Transfer with the specified id
    transfers_delete_query = 'DELETE FROM Transfers WHERE transferID = %s;'
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=transfers_delete_query, query_params=(id, ))

    return redirect('/transfers')


@app.route('/transfer_items', methods=["POST", "GET"])
def transfer_items():
    # Create a new Transfer Item
    if request.method == "POST":
        if request.form.get("add_transfer_item"):
            # Get user form inputs
            transfer_id = request.form["transfer_id"]
            transfer_item_name = request.form["transfer_item_name"]
            quantity = request.form["quantity"]
            milliliters = request.form["milliliters"]
            pounds = request.form["pounds"]
            transfer_item_add_query = ('INSERT INTO TransferItems '
                                            '(transferID, itemID, quantity, milliliters, pounds) '
                                        'VALUES '
                                            '(%s, (SELECT itemID FROM Items WHERE itemName = %s), %s, %s, %s);')
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=transfer_item_add_query, query_params=(transfer_id, transfer_item_name, quantity, milliliters, pounds, ))

        return redirect('/transfer_items')


    # Get the Transfer Items data for display
    if request.method == "GET":
        transfer_items_get_query = ('SELECT '
                                        'TransferItems.transferItemID AS "Transfer Item ID", '
                                        'Items.itemName AS "Item Name", '
                                        'Transfers.transferID AS "Transfer ID", '
                                        'LendingUsers.userName AS "Lending User", '
                                        'BorrowingUsers.userName AS "Borrowing User", '
                                        'TransferItems.quantity AS Quantity, '
                                        'TransferItems.milliliters AS Milliliters, '
                                        'TransferItems.pounds AS Pounds '
                                    'FROM TransferItems '
                                    'JOIN Items ON Items.itemID = TransferItems.itemID '
                                    'JOIN Transfers ON Transfers.transferID = TransferItems.transferID '
                                    'JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID '
                                    'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID '
                                    'ORDER BY TransferItems.transferItemID;')
        items_get_query = 'SELECT itemName FROM Items;'
        transfers_get_query = ('SELECT '
                                    'Transfers.transferID, '
                                    'LendingUsers.userName AS "Lending User", '
                                    'BorrowingUsers.userName AS "Borrowing User" '
                                'FROM Transfers '
                                'JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID '
                                'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID;')
        ids_get_query = 'SELECT transferID, itemID FROM TransferItems;'
        with connect() as db_connection:
            transfer_items_cursor = db.execute_query(db_connection=db_connection, query=transfer_items_get_query)
            items_cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
            transfers_cursor = db.execute_query(db_connection=db_connection, query=transfers_get_query)
            ids_cursor = db.execute_query(db_connection=db_connection, query=ids_get_query)
            transfer_items_query_results = transfer_items_cursor.fetchall()
            items_query_results = items_cursor.fetchall()
            transfers_query_results = transfers_cursor.fetchall()
            ids_query_results = ids_cursor.fetchall()
            return render_template("transfer_items.j2", transfer_items=transfer_items_query_results, items=items_query_results, transfers=transfers_query_results, ids=ids_query_results)
        

# Route to edit Transfer Items
@app.route('/edit_transfer_items/<int:id>', methods=["POST", "GET"])
def edit_transfer_items(id):
    # Get data for the Transfer Item with the specified id
    if request.method == "GET":
        transfer_item_get_query = ('SELECT '
                                        'TransferItems.transferItemID AS "Transfer Item ID", '
                                        'Items.itemName AS "Item Name", '
                                        'Transfers.transferID AS "Transfer ID", '
                                        'LendingUsers.userName AS "Lending User", '
                                        'BorrowingUsers.userName AS "Borrowing User", '
                                        'TransferItems.quantity AS Quantity, '
                                        'TransferItems.milliliters AS Milliliters, '
                                        'TransferItems.pounds AS Pounds '
                                    'FROM TransferItems '
                                    'JOIN Items ON Items.itemID = TransferItems.itemID '
                                    'JOIN Transfers ON Transfers.transferID = TransferItems.transferID '
                                    'JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID '
                                    'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID '
                                    'WHERE TransferItems.transferItemID = %s;')
        items_get_query = 'SELECT itemName FROM Items;'
        transfers_get_query = ('SELECT '
                                    'Transfers.transferID, '
                                    'LendingUsers.userName AS "Lending User", '
                                    'BorrowingUsers.userName AS "Borrowing User" '
                                'FROM Transfers '
                                'JOIN Users AS LendingUsers ON LendingUsers.userID = Transfers.lendingUserID '
                                'JOIN Users AS BorrowingUsers ON BorrowingUsers.userID = Transfers.borrowingUserID;')

        with connect() as db_connection:
            transfer_item_cursor = db.execute_query(db_connection=db_connection, query=transfer_item_get_query, query_params=(id, ))
            items_cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
            transfers_cursor = db.execute_query(db_connection=db_connection, query=transfers_get_query)
            transfer_item_query_results = transfer_item_cursor.fetchall()
            print(f"Transfer Item query result: {transfer_item_query_results}")
            items_query_results = items_cursor.fetchall()
            transfers_query_results = transfers_cursor.fetchall()
            return render_template("edit_transfer_items.j2", transfer_item=transfer_item_query_results, transfers=transfers_query_results, items=items_query_results)

    # Update the Transfer Item with the specified id
    if request.method == "POST":
        # Get form input
        transfer_id = request.form["transfer_id"]
        item_name = request.form["item_name"]
        quantity = request.form["quantity"]
        milliliters = request.form["milliliters"]
        pounds = request.form["pounds"]
        # Execute the query to update the Transfer Item
        transfer_item_update_query = ('UPDATE TransferItems '
                                        'SET transferID = %s, '
                                            'itemID = %s, '
                                            'quantity = %s, '
                                            'milliliters = %s, '
                                            'pounds = %s '
                                        'WHERE transferItemID = %s;')
        # Get item ID from the returned item name
        item_id_get_query = ('SELECT itemID '
                                'FROM Items '
                                'WHERE itemName = %s;')
        with connect() as db_connection:
            item_id_cursor = db.execute_query(db_connection=db_connection, query=item_id_get_query, query_params=(item_name, ))
            item_id = item_id_cursor.fetchall()[0]['itemID']
            db.execute_query(db_connection=db_connection, query=transfer_item_update_query, query_params=(transfer_id, item_id, quantity, milliliters, pounds, id,))

        return redirect('/transfer_items')


@app.route('/delete_transfer_items/<int:transfer_id>-<int:item_id>')
def delete_transfer_items(transfer_id, item_id):
    # Delete the Transfer Item with the specified transferID and itemID
    transfer_items_delete_query = ('DELETE FROM TransferItems '
                                        'WHERE transferID = %s AND itemID = %s;')
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=transfer_items_delete_query, query_params=(transfer_id, item_id))

    return redirect('/transfer_items')


# Neighborhoods Route
@app.route('/neighborhoods', methods=["POST", "GET"])
def neighborhoods():
    # Create a new Neighborhood
    if request.method == "POST":
        if request.form.get("add_neighborhood"):
            # Get user form inputs
            neighborhood_name = request.form["neighborhood_name"]
            neighborhood_add_query = 'INSERT INTO Neighborhoods (neighborhoodName) VALUES (%s);'
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=neighborhood_add_query, query_params=(neighborhood_name,))

        return redirect('/neighborhoods')

    # Retrieve the Neighborhood data for display
    if request.method == "GET":
        neighborhoods_get_query = ('SELECT '
                                        'neighborhoodID AS "Neighborhood ID", '
                                        'neighborhoodName AS "Neighborhood Name" '
                                    'FROM Neighborhoods;')
        with connect() as db_connection:
            cursor = db.execute_query(db_connection=db_connection, query=neighborhoods_get_query)
            query_results = cursor.fetchall()
            return render_template("neighborhoods.j2", neighborhoods=query_results)


# Route for updating the selected Neighborhood
@app.route('/edit_neighborhoods/<int:id>', methods=["POST", "GET"])
def edit_neighborhoods(id):
    print(f"Received request for id: {id}")

    # Get data for the Neighborhood with the specified id
    if request.method == "GET":
        neighborhood_get_query = ('SELECT '
                                        'neighborhoodID AS "Neighborhood ID", '
                                        'neighborhoodName AS "Neighborhood Name" '
                                    'FROM Neighborhoods '
                                    'WHERE neighborhoodID = %s;')
        with connect() as db_connection:
            cursor = db.execute_query(db_connection=db_connection, query=neighborhood_get_query, query_params=(id,))
            query_results = cursor.fetchall()
            print(f"Query results: {query_results}")
            return render_template("edit_neighborhoods.j2", neighborhood=query_results)

    # Update the Neighborhood with the specified id
    if request.method == "POST":
        # Get form input
        neighborhood_name = request.form["neighborhood_name"]

        # Execute the query to update the Neighborhood
        neighborhood_update_query = ('UPDATE Neighborhoods '
                                        'SET neighborhoodName = %s '
                                        'WHERE neighborhoodID = %s;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=neighborhood_update_query, query_params=(neighborhood_name, id,))

        return redirect('/neighborhoods')


# Route to delete Neighborhoods
@app.route('/delete_neighborhoods/<int:id>')
def delete_neighborhoods(id):
    # Delete the Neighborhood with the specified id
    neighborhoods_delete_query = 'DELETE FROM Neighborhoods WHERE neighborhoodID = %s;'
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=neighborhoods_delete_query, query_params=(id,))

    return redirect('/neighborhoods')

@app.route('/item_categories', methods=["POST", "GET"])
def item_categories():
    # Create a new Item Category
    if request.method == "POST":
        if request.form.get("add_item_category"):
            # Get user form inputs
            item_category_name = request.form["category_name"]
            item_category_add_query = 'INSERT INTO ItemCategories (categoryName) VALUES (%s);'
            with connect() as db_connection:
                db.execute_query(db_connection=db_connection, query=item_category_add_query, query_params=(item_category_name, ))

        return redirect('/item_categories')

    # Retrieve the Item Categories data for display
    if request.method == "GET":
        item_categories_get_query = ('SELECT '
                                        'categoryID AS "Category ID", '
                                        'categoryName AS "Category Name" '
                                    'FROM ItemCategories;')
        with connect() as db_connection:
            cursor = db.execute_query(db_connection=db_connection, query=item_categories_get_query)
            query_results = cursor.fetchall()
            return render_template("item_categories.j2", item_categories=query_results)


# Route for updating the selected Item Category
@app.route('/edit_item_categories/<int:id>', methods=["POST", "GET"])
def edit_item_categories(id):
    # Get data for the Item Category with the specified id
    if request.method == "GET":
        item_category_get_query = ('SELECT '
                                        'categoryID AS "Category ID", '
                                        'categoryName AS "Category Name" '
                                    'FROM ItemCategories '
                                    'WHERE categoryID = %s;')
        with connect() as db_connection:
            cursor = db.execute_query(db_connection=db_connection, query=item_category_get_query, query_params=(id, ))
            query_results = cursor.fetchall()
            print(f"Query results: {query_results}")
            return render_template("edit_item_categories.j2", item_category=query_results)

    # Update the Item Category with the specified id
    if request.method == "POST":
        # Get form input
        category_name = request.form["category_name"]

        # Execute the query to update the Item Category
        item_category_update_query = ('UPDATE ItemCategories '
                                        'SET categoryName = %s '
                                        'WHERE categoryID = %s;')
        with connect() as db_connection:
            db.execute_query(db_connection=db_connection, query=item_category_update_query, query_params=(category_name, id, ))

        return redirect('/item_categories')


# Route for deleting the selected Item Category
@app.route('/delete_item_categories/<int:id>')
def delete_item_categories(id):
    # Delete the Item Category with the specified id
    item_categories_delete_query = 'DELETE FROM ItemCategories WHERE categoryID = %s;'
    with connect() as db_connection:
        db.execute_query(db_connection=db_connection, query=item_categories_delete_query, query_params=(id, ))

    return redirect('/item_categories')


# Listener

if __name__ == "__main__":
    port = APP_PORT

    app.run(port=port)