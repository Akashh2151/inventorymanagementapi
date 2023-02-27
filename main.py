import json
from bson import ObjectId
import pymongo
from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
# from werkzeug import generate_password_hash, check_password_hash

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
user = db["User"]
# __________________________________________________________________

app = Flask(__name__)
jwt = JWTManager(app)
# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"


@app.route("/dashboard")
@jwt_required
def dasboard():
    return jsonify(message="Welcome! to our task kiran")


@app.route("/register", methods=["POST"])
def register():
    
    email = (request.form.get("email"))
 
    password = (request.form.get("password"))
    # pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    # email validation
    regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # strong password validation
    regexx = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    # print("ha email aahe___________ ",email)

    # print("_____________ check kya he ")

    # a=0
    # y=len(email)
    # dot=email.find(".")
    # at=email.find("@")

    # for i in range (0,at):
    #     if((email[i]>='a' and email[i]<='z') or (email[i]>='A' and email[i]<='Z')):
    #         a=a+1
    # if(a>0 and at>0 and (dot-at)>0 and (dot+1)<y):
    #     print("Valid Email")
    # else:
    #     print("Invalid Email")

    # test = User.query.filter_by(email=email).first()

    test = user.find_one({"email": email})
    print(f"test_____________________________________{test}")

    if test:
        return jsonify(message="email id is alredy exist "), 409

    if r.fullmatch(regexp, email) and r.fullmatch(regexx, password):
        # id = (request.form.get("id"))
        first_name = (request.form.get("first_name"))
        last_name = (request.form.get("last_name"))
        mobaile_num = (request.form.get("mobaile"))
        user_name = (request.form.get("username"))
        confirm_password = (request.form.get("confirmpassword"))
        business_type=(request.form.get("businesstype"))
       

       
        # password = (request.form.get("password"))
        # print(f"password_________________________________________________{password}")
        user_info = dict(first_name=first_name,
                         last_name=last_name, confirm_password=confirm_password,business_type=business_type,email=email,mobaile_num=mobaile_num,user_name=user_name,password=password)
        print(
            f"all info_____________________________________________________________{user_info}")
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 200

    else:

        return jsonify(message="check your email id and password formate"), 409


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


# @cross_origin()
# @app.route('/getpets', methods = ['GET'])
# def getpets():
#      all_pets = []
#      pets = Pet.query.all()
#      for pet in pets:
#           results = {
#                     "pet_id":pet.id,
#                     "pet_name":pet.pet_name,
#                     "pet_age":pet.pet_age,
#                     "pet_type":pet.pet_type,
#                     "pet_description":pet.pet_description, }
#           all_pets.append(results)

#      return jsonify(
#             {
#                 "success": True,
#                 "pets": all_pets,
#                 "total_pets": len(pets),
#             }
#         )


# @app.route('/users',methods=['GET'])
# def get_some_users():
#     try:
#         data=list(user.find)

#         print(data,"_____________________________")
#         for user in data:
#             user["_id"] = str(user["_id"])
#         return Response(
#             response=json.dumps(data),
#             status=500,
#             mimetype="application/json" )
#     except Exception as ex:
#         print(ex)
#         return Response(response=json.dumps({"message":"can not read users"}))


#     user.delete_one({"_id": ObjectId(id)})
#     return jsonify(message="delete successful"), 200


# @app.route("/user/<int:ObjectId>",methods = ['GET'])
# def insert_one(todoId):
#     todo = user.find_one({"_id": ObjectId})
#     return jsonify(msg="success")








if __name__ == '__main__':
    app.run(host="localhost", debug=True)
