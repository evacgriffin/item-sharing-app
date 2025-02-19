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

@app.route('/users')
def users():
    return render_template("users.j2", users=users_sample_data)

@app.route('/items')
def items():
    return render_template("items.j2", items=items_sample_data)

@app.route('/user_items')
def user_items():
    return render_template("user_items.j2", user_items=user_items_sample_data)

@app.route('/transfers')
def transfers():
    return render_template("transfers.j2", transfers=transfers_sample_data)

@app.route('/transfer_items')
def transfer_items():
    return render_template("transfer_items.j2", transfer_items=transfer_items_sample_data)

@app.route('/neighborhoods')
def neighborhoods():
    return render_template("neighborhoods.j2", neighborhoods=neighborhoods_sample_data)

@app.route('/item_categories')
def item_categories():
    return render_template("item_categories.j2", item_categories=item_categories_sample_data)

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
        "neighborhoodID": 1
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