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
    return render_template("users.j2", users=users_sample_data)

@app.route('/items')
def items():
    return render_template("items.j2", items=items_sample_data)

@app.route('/user_items')
def user_items():
    return render_template("user_items.j2", user_items=user_items_sample_data)

@app.route('/transfers', methods=["POST", "GET"])
def transfers():
    # Get the Transfers data for display
    if request.method == "GET":
        transfers_get_query = 'SELECT transferID AS "Transfer ID", transferDateTime AS "Transfer Date and Time", lendingUserID AS "Lending User ID", borrowingUserID AS "Borrowing User ID" FROM Transfers;'
        cursor = db.execute_query(db_connection=db_connection, query=transfers_get_query)
        query_results = cursor.fetchall()
        return render_template("transfers.j2", transfers=query_results)


@app.route('/transfer_items')
def transfer_items():
    return render_template("transfer_items.j2", transfer_items=transfer_items_sample_data)

@app.route('/neighborhoods')
def neighborhoods():
    return render_template("neighborhoods.j2", neighborhoods=neighborhoods_sample_data)

@app.route('/item_categories', methods=["POST", "GET"])
def item_categories():
    # Get the Item Categories data for display
    if request.method == "GET":
        item_categories_get_query = 'SELECT categoryID AS "Category ID", categoryName AS "Category Name" FROM ItemCategories;'
        cursor = db.execute_query(db_connection=db_connection, query=item_categories_get_query)
        query_results = cursor.fetchall()
        return render_template("item_categories.j2", item_categories=query_results)
    
    # Post new entry to Item Categories
    if request.method == "POST":
        if request.form.get("add_item_category"):
            category_name = request.form["category_name"]

        item_categories_add_query = 'INSERT INTO ItemCategories (categoryName) VALUES (%s);'
        cursor = db.execute_query(db_connection=db_connection, query=item_categories_add_query, query_params=(category_name))
        query_results = cursor.fetchall()
        return redirect('/item_categories')

# Static Sample Data
users_sample_data = [
    {
        "userID": 1,
        "userName": "katie775",
        "password": "example_pw_1",
        "email": "katie775@gmail.com",
        "neighborhoodID": 5
    },
    {
        "userID": 2,
        "userName": "friendly_neighbor3",
        "password": "example_pw_2",
        "email": "neighbor3@gmail.com",
        "neighborhoodID": 3
    },
    {
        "userID": 3,
        "userName": "ben.smith89",
        "password": "example_pw_3",
        "email": "bsmith89@gmail.com",
        "neighborhoodID": 4
    },
    {
        "userID": 4,
        "userName": "griff123",
        "password": "example_pw_4",
        "email": "griff123@hotmail.com",
        "neighborhoodID": "NULL"
    },
    {
        "userID": 5,
        "userName": "camper007",
        "password": "example_pw_5",
        "email": "camper7@gmail.com",
        "neighborhoodID": 2
    }
]

items_sample_data = [
    {
        "itemID": 1,
        "itemName": "lantern",
        "categoryID": 1,
    },
    {
        "itemID": 2,
        "itemName": "AA battery",
        "categoryID": 5,
    },
    {
        "itemID": 3,
        "itemName": "water bottle",
        "categoryID": 3,
    },
    {
        "itemID": 4,
        "itemName": "rice",
        "categoryID": 2,
    },
    {
        "itemID": 5,
        "itemName": "beanie",
        "categoryID": 4,
    }
]

user_items_sample_data = [
    {
        "userID": 1,
        "itemID": 5,
    },
    {
        "userID": 1,
        "itemID": 3,
    },
    {
        "userID": 3,
        "itemID": 2,
    },
    {
        "userID": 3,
        "itemID": 4,
    },
    {
        "userID": 5,
        "itemID": 3,
    },
]

transfer_items_sample_data = [
    {
        "transferItemID": 1,
        "itemID": 2,
        "transferID": 1,
        "quantity": 20,
        "milliliters": None,
        "pounds": None
    },
    {
        "transferItemID": 2,
        "itemID": 4,
        "transferID": 2,
        "quantity": 3,
        "milliliters": None,
        "pounds": None
    },
    {
        "transferItemID": 3,
        "itemID": 5,
        "transferID": 3,
        "quantity": 3,
        "milliliters": None,
        "pounds": 2.0
    },
    {
        "transferItemID": 4,
        "itemID": 3,
        "transferID": 4,
        "quantity": 4,
        "milliliters": 500.00,
        "pounds": None
    },
    {
        "transferItemID": 5,
        "itemID": 3,
        "transferID": 5,
        "quantity": 2,
        "milliliters": 600.00,
        "pounds": None
    }
]

neighborhoods_sample_data = [
    {
        "neighborhoodID": 1,
        "neighborhoodName": "Belltown"
    },
    {
        "neighborhoodID": 2,
        "neighborhoodName": "South Lake Union"
    },
    {
        "neighborhoodID": 3,
        "neighborhoodName": "West Capitol Hill"
    },
    {
        "neighborhoodID": 4,
        "neighborhoodName": "Pioneer Square"
    },
    {
        "neighborhoodID": 5,
        "neighborhoodName": "Waterfront"
    }
]


# Listener

if __name__ == "__main__":
    port = APP_PORT

    app.run(port=port)