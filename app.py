from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
app = Flask(__name__)

from pymongo import MongoClient
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
print(app.config["MONGO_URI"])

client = MongoClient(app.config["MONGO_URI"])
db = client.get_database('food-find')
places = db.places




@app.route('/')
def index():
    return render_template('index.html', places=places.find())


@app.route('/places/new')
def new_place():
    return render_template('new_place.html')


@app.route('/places', methods=['POST'])
def add_place():
    place = {
        'name': request.form.get('name'),
        'rating': request.form.get('rating'),
        'price': request.form.get('price')
    }
    places.insert_one(place)
    return redirect(url_for('index'))











if __name__ == '__main__':
    app.run(debug=True)