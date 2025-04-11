#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response(
        [restaurant.to_dict(rules=('-restaurant_pizzas', '-pizzas',))for restaurant in restaurants],
        200
    )


@app.route('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return{"error": "Restaurant not found"}, 404
    
    return make_response(
        restaurant.to_dict(rules=('-restaurant_pizzas.restaurant', '-restaurant_pizzas',)),
        200
    )


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {'error': "Restaurant not found"}, 404
    
    db.session.delete(restaurant)
    db.session.commit()

    return '', 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
