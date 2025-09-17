#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    return "<h1>Flask SQLAlchemy Application</h1>"

# GET all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    pets_list = [pet.to_dict() for pet in pets]
    return make_response(jsonify(pets_list), 200)

# GET single pet
@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        return make_response(jsonify({"error": "Pet not found"}), 404)
    return make_response(jsonify(pet.to_dict()), 200)

# POST create new pet
@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    try:
        new_pet = Pet(
            name=data['name'],
            species=data['species']
        )
        db.session.add(new_pet)
        db.session.commit()
        return make_response(jsonify(new_pet.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

# PATCH update pet
@app.route('/pets/<int:id>', methods=['PATCH'])
def update_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        return make_response(jsonify({"error": "Pet not found"}), 404)

    data = request.get_json()
    if "name" in data:
        pet.name = data["name"]
    if "species" in data:
        pet.species = data["species"]

    db.session.commit()
    return make_response(jsonify(pet.to_dict()), 200)

# DELETE pet
@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        return make_response(jsonify({"error": "Pet not found"}), 404)

    db.session.delete(pet)
    db.session.commit()
    return make_response(jsonify({"message": f"Pet {id} deleted"}), 200)

# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    app.run(port=5555, debug=True)
