from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)


# Routes

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/user-items')
def user_items():
    return render_template("user_items.j2")

@app.route('/transfers')
def transfers():
    return render_template("transfers.j2")

@app.route('/transfer-items')
def transfer_items():
    return render_template("transfer_items.j2")

@app.route('/neighborhoods')
def neighborhoods():
    return render_template("neighborhoods.j2")

@app.route('/item-categories')
def item_categories():
    return render_template("item_categories.j2")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4281))

    app.run(port=port)