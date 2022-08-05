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
from models import db, User
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


@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):

    if user_id==0:
        raise APIException("No existe un usuario con ID 0",status_code=500)
    user =User.query.get(user_id)
    if user is None:
        raise APIException("El usuario con ese ID no existe",status_code=400)
    response_body={
        "Usuario":user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/User',methods=['POST'])
def post_new_user():
    body = request.get_json()
    if body['email'] is none:
        raise APIException('Necesitas llenar los campos de email')
    response_body={
        
        "msg":"El usuario has sido creado"
    }

    return jsonify(response_body),200

@app.route('/people', methods=['GET'])
def get_all_people():

    response_body = {
    "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
