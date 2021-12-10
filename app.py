import re
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import random
import os
app = Flask(__name__)

from pymongo import MongoClient
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
print(app.config["MONGO_URI"])


client = MongoClient(app.config["MONGO_URI"])
db = client.get_database('food-find')
places = db.places



#---------------------- /
@app.route('/')
def index():
    return render_template('index.html', places=places.find())

#---------------------- / new place
@app.route('/places/new')
def new_place():
    return render_template('new_place.html')

#---------------------- / submit it

@app.route('/places', methods=['POST'])
def add_place():
    place = {
        'name': request.form.get('name'),
        'rating': request.form.get('rating'),
        'price': request.form.get('price'),
        'date': request.form.get('date'),
        'desc': request.form.get('desc')
    }
    places.insert_one(place)
    return redirect(url_for('index'))

#---------------------- / show one
@app.route('/places/<place_id>')
def show_place(place_id):
    place = places.find_one({'_id': ObjectId(place_id)})
    return render_template('show_place.html', place = place)

#---------------------- / edit it
@app.route('/places/<place_id>/edit')
def edit_place(place_id):
    place = places.find_one({'_id': ObjectId(place_id)})
    return render_template('edit_place.html', place=place)

#---------------------- / update with edit
@app.route('/places/<place_id>', methods=['POST'])
def update_place(place_id):
    updated_place = {
        'name': request.form.get('name'),
        'rating': request.form.get('rating'),
        'price': request.form.get('price'),
        'date': request.form.get('date'),
        'desc': request.form.get('desc')
    }
    places.update_one(
        {'_id': ObjectId(place_id)},
        {'$set': updated_place}
    )
    return redirect(url_for('show_place', place_id=place_id))


#---------------------- / delete it
@app.route('/places/<place_id>/delete', methods=['POST'])
def delete_place(place_id):
    places.delete_one({'_id': ObjectId(place_id)})
    return redirect(url_for('index'))



#---------------------- / get a random place
@app.route('/places/select')
def show_selection():
    selected = places.aggregate( [ { "$sample": { "size": 1 } } ])
    return render_template("show_selection.html", selected=selected)


#---------------------- / place description
# @app.route('/places/descriptions', methods=['POST'])
# def desc_new():
#     desc = {
#         'place_id':ObjectId(request.form.get('place_id')),
#         'desc-content': request.form.get('desc-content'),
#     }
#     descriptions.insert_one(desc) 
#     return redirect(url_for('places_show', place_id=request.form.get('place_id')))











if __name__ == '__main__':
    app.run(debug=True)