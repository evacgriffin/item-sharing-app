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
APP_PORT = int(os.getenv("PORT", 4281))

db_connection = db.connect_to_database(APP_MYSQL_HOST, APP_MYSQL_USER, APP_MYSQL_PASSWORD, APP_MYSQL_DB_NAME)

# Routes

@app.route('/')
def root():
    return render_template("main.j2")


@app.route('/users')
def users():
    # Get the Users data for display
    if request.method == "GET":
        users_get_query = 'SELECT userID AS "User ID", username AS Username, password AS Password, email AS Email, neighborhoodID AS "Neighborhood ID" FROM Users;'
        cursor = db.execute_query(db_connection=db_connection, query=users_get_query)
        query_results = cursor.fetchall()
        return render_template("users.j2", users=query_results)


@app.route('/items')
def items():
    # Get the Items data for display
    if request.method == "GET":
        items_get_query = 'SELECT itemID AS "Item ID", itemName AS "Item Name", categoryID AS "Category ID" FROM Items;'
        cursor = db.execute_query(db_connection=db_connection, query=items_get_query)
        query_results = cursor.fetchall()
        return render_template("items.j2", items=query_results)


@app.route('/user_items')
def user_items():
    # Get the User Items data for display
    if request.method == "GET":
        user_items_get_query = 'SELECT userID AS "User ID", itemID AS "Item ID" FROM UserItems;'
        cursor = db.execute_query(db_connection=db_connection, query=user_items_get_query)
        query_results = cursor.fetchall()
        return render_template("user_items.j2", user_items=query_results)


@app.route('/transfers', methods=["GET"])
def transfers():
    # Get the Transfers data for display
    if request.method == "GET":
        transfers_get_query = 'SELECT transferID AS "Transfer ID", transferDateTime AS "Transfer Date and Time", lendingUserID AS "Lending User ID", borrowingUserID AS "Borrowing User ID" FROM Transfers;'
        cursor = db.execute_query(db_connection=db_connection, query=transfers_get_query)
        query_results = cursor.fetchall()
        return render_template("transfers.j2", transfers=query_results)


@app.route('/transfer_items')
def transfer_items():
    # Get the Transfer Items data for display
    if request.method == "GET":
        transfer_items_get_query = 'SELECT transferItemID AS "Transfer Item ID", itemID AS "Item ID", transferID AS "Transfer ID", quantity AS Quantity, milliliters AS Milliliters, pounds AS Pounds FROM TransferItems;'
        cursor = db.execute_query(db_connection=db_connection, query=transfer_items_get_query)
        query_results = cursor.fetchall()
        return render_template("transfer_items.j2", transfer_items=query_results)

@app.route('/neighborhoods')
def neighborhoods():
    # Get the Neighborhoods data for display
    if request.method == "GET":
        neighborhoods_get_query = 'SELECT neighborhoodID AS "Neighborhood ID", neighborhoodName AS "Neighborhood Name" FROM Neighborhoods;'
        cursor = db.execute_query(db_connection=db_connection, query=neighborhoods_get_query)
        query_results = cursor.fetchall()
        return render_template("neighborhoods.j2", neighborhoods=query_results)

@app.route('/item_categories', methods=["GET"])
def item_categories():
    # Get the Item Categories data for display
    if request.method == "GET":
        item_categories_get_query = 'SELECT categoryID AS "Category ID", categoryName AS "Category Name" FROM ItemCategories;'
        cursor = db.execute_query(db_connection=db_connection, query=item_categories_get_query)
        query_results = cursor.fetchall()
        return render_template("item_categories.j2", item_categories=query_results)


# Listener

if __name__ == "__main__":
    port = APP_PORT

    app.run(port=port)