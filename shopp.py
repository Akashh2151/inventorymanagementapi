import json
from bson import ObjectId
import pymongo
from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
 

import re as r
# _______________________________________________________________
# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017")
# database
db = client["app_database"]
# collection
shop = db["Shop"]
# __________________________________________________________________

app = Flask(__name__)
jwt = JWTManager(app)
# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"


@app.route("/dashboard")
@jwt_required
def dasboard():
    return jsonify(message="Welcome! to our task kiran")




# insert data
@app.route('/inventory/subReports', methods=['POST'])
def add_user():
    _json = request.json
    _itemName = request.json['itemName']
    _soldQty = request.json['soldQty']
    _qtyInStock = request.json['qtyInStock']
    # validate the received values
    if _itemName and _soldQty and _qtyInStock :
        # do not save password as a plain text
        # _hashed_password = generate_password_hash(_password)
        # save details
        id = shop.insert_one(
            {'itemName': _itemName, 'soldQty': _soldQty, 'qtyInStock': _qtyInStock})
        resp = jsonify(msg='User added successfully!'), 200
        # resp.status_code = 200
        return resp
    else:
     ress = jsonify(msg="user not addded")
    return ress




# get all data
@app.route('/inventory/subReports',methods=['GET'])
def users():
	users = shop.find()
	resp = dumps(users)
	return resp




# get data using id
@app.route('/inventory/subReports/<id>')
def user(id):
	user = shop.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp

    

@app.route('/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']		
	# validate the received values
	if _name and _email and _password and _id and request.method == 'PUT':
		#do not save password as a plain text
		_hashed_password = generate_password_hash(_password)
		# save edits
		shop.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return jsonify(msg="user not updated"),409



@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	shop.delete_one({'_id': ObjectId(id)})
	resp = jsonify(msg='User deleted successfully!')
	resp.status_code = 200
	return resp


# @app.route('/inventory/subReports', methods=['GET'])
# def mongo_read():
#     data = request.json
#     if data is None or data == {}:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400,
#                         mimetype='application/json')
#     obj1 = shop
#     response = obj1.find()
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')



if __name__ == '__main__':
    app.run(host="localhost", debug=True)
