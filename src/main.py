"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, people, planets, vehicles
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_all_people():

    characters = people.query.all()
    all_people = list(map(lambda x: x.serialize(), characters))
    print(characters)
    response_body = {
        "msg": "Personajes star wars",
        "Character": all_people
    }
    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def get_all_users():

    all_users = User.query.all()
    get_all_users = list(map(lambda x: x.serialize(), all_users))
    response_body = {
        "msg": "Lista de usuarios",
        "Usuarios": get_all_users
    }
    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planet = planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet))
    response_body = {
        "msg": "Planetas star wars",
        "Character": all_planets
    }
    return jsonify(response_body), 200


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    all_vehicle = vehicles.query.all()
    get_all_vehicles = list(map(lambda x: x.serialize(), all_vehicle))
    response_body = {
        "msg": "Vehiculos star wars",
        "Vehiculos": get_all_vehicles
    }
    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):

    if people_id == 0:
        raise APIException("No existe un usuario con ID 0", status_code=500)
    character = people.query.get(people_id)
    if character is None:
        raise APIException(
            "El personaje con ese ID no existe", status_code=400)
    response_body = {
        "Personaje": character.serialize()
    }
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    if planet_id == 0:
        raise APIException("No existe un planeta con ID 0", status_code=500)
    single_planet = planets.query.get(planet_id)
    if single_planet is None:
        raise APIException("El planeta con ese ID no existe", status_code=400)
    response_body = {
        "Planeta": single_planet.serialize()
    }
    return jsonify(response_body), 200


@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_single_vehicle(vehicles_id):

    if vehicles_id == 0:
        raise APIException("No existe un vehiculo con ID 0", status_code=500)
    single_vehicle = vehicles.query.get(vehicles_id)
    if single_vehicle is None:
        raise APIException("El vehiculo con ese ID no existe", status_code=400)
    response_body = {
        "Vehiculo": single_vehicle.serialize()
    }
    return jsonify(response_body), 200

# Ruta para acceder a info de un usuario


@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):

    if user_id == 0:
        raise APIException("No existe un usuario con ID 0", status_code=500)
    user = User.query.get(user_id)
    if user is None:
        raise APIException("El usuario con ese ID no existe", status_code=400)
    response_body = {
        "Usuario": user.serialize()
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def post_new_user():
    body = request.get_json()
    if body['email'] is none:
        raise APIException('Necesitas llenar los campos de email')
    response_body = {

        "msg": "El usuario has sido creado"
    }

    return jsonify(response_body), 200

# Metodo y ruta para agregar elemento favorito a un usuario


@app.route('/user', methods=['PUT'])
def add_user_favorites():
    user_id = request.json.get("user_id", None)
    favorite_id = request.json.get("id", None)
    favorite_type = request.json.get("type", None)

    if user_id is None:
        return jsonify({"msg": "No ha establecio el ID del usuario"}), 400
    if favorite_id is None:
        return jsonify({"msg": "No ha establecio el ID del elemento favorito specified"}), 400
    if favorite_type is None:
        return jsonify({"msg": "No se establecio el tipo de favorito a agregar"}), 400

    user = User.query.get(user_id)

    if User is None:
        return jsonify({"msg": "Usuario no existe"}), 400

    if favorite_type == "person":
        resource = people.query.get(favorite_id)
        user.people.append(resource)
    if favorite_type == "planet":
        resource = planets.query.get(favorite_id)
        user.planets.append(resource)

    if favorite_type == "vehicle":
        resource = vehicles.query.get(favorite_id)
        user.vehicles.append(resource)

    db.session.commit()

    response_body = {
        "msg": "Favorito Agregado",
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
