"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

jackson_family.add_member(
    {
    'first_name': 'John',
    'age': 33,
    'lucky_numbers': [7, 13, 22]
    }
)

jackson_family.add_member(
    {
    'first_name': 'Jane',
    'age': 35,
    'lucky_numbers': [10, 14, 3]
    }
)

jackson_family.add_member(
    {
    'first_name': 'Jimmy',
    'age': 5,
    'lucky_numbers': [1]
    }
)
# #POST
# @app.route('/members', methods=['POST'])
# def add_new_member():
#     new_family_member = request.json
#     jackson_family.add_member(new_family_member)
#     members = jackson_family.get_all_members()
#     response_body = {
#         "results": members
#     }
#     return jsonify(response_body), 200

#POST
@app.route('/member', methods=['POST'])
def create_member():
    body = request.get_json()
    new_member = {
        "id": body["id"],
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }
    jackson_family.add_member(new_member)
    response_body = {
        "msg": "New member successfully added",
        "member":  new_member
    }
    return jsonify(response_body), 200

#GET members
@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    return jsonify(members), 200

#GET by ID
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    member = jackson_family.get_member(id)
    return jsonify(member), 200

#Delete member by ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    return jsonify({"done" : True, "deleted_member": member}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
