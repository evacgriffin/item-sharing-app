"""
This code has been adapted from the following sources:

flask-starter-app
Retrieved on: 02/08/2025
URL: https://github.com/osu-cs340-ecampus/flask-starter-app
"""

from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

# Routes

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/user_items')
def user_items():
    return render_template("user_items.j2")

@app.route('/transfers')
def transfers():
    return render_template("transfers.j2", transfers=transfers_sample_data)

@app.route('/transfer_items')
def transfer_items():
    return render_template("transfer_items.j2", transfer_items=transfer_items_sample_data)

@app.route('/neighborhoods')
def neighborhoods():
    return render_template("neighborhoods.j2")

@app.route('/item_categories')
def item_categories():
    return render_template("item_categories.j2", item_categories=item_categories_sample_data)

# Static Sample Data
transfers_sample_data = [
    {
        "transferID": 1,
        "transferDateTime": "2025-02-04 11:00",
        "lendingUserID": 3,
        "borrowingUserID": 1
    },
    {
        "transferID": 2,
        "transferDateTime": "2025-02-07 15:30",
        "lendingUserID": 3,
        "borrowingUserID": 2
    },
    {
        "transferID": 3,
        "transferDateTime": "2025-01-27 17:45",
        "lendingUserID": 1,
        "borrowingUserID": 2
    },
    {
        "transferID": 4,
        "transferDateTime": "2025-01-01 10:00",
        "lendingUserID": 1,
        "borrowingUserID": 3
    },
    {
        "transferID": 5,
        "transferDateTime": "2025-02-01 18:30",
        "lendingUserID": 5,
        "borrowingUserID": 4
    }
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

item_categories_sample_data = [
    {
        "categoryID": 1,
        "categoryName": "lighting"
    },
    {
        "categoryID": 2,
        "categoryName": "food"
    },
    {
        "categoryID": 3,
        "categoryName": "drinks"
    },
    {
        "categoryID": 4,
        "categoryName": "clothing"
    },
    {
        "categoryID": 5,
        "categoryName": "energy"
    }
]

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4281))

    app.run(port=port)