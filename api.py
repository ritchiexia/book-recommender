from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from backend import User, find_paired_user, RLModel, get_recs, update_model, create_matrix, create_book_feature_matrix
import torch

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bookuser-db'
app.config["MONGO_URI"] = "mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority"
api = Api(app)
mongo = PyMongo(app)


client = pymongo.MongoClient("mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority")
db = client["book-recommender"]
collect = db["user-data"]

#Code for importing model will go here
load = torch.load('model.pt')
model = load['best-model']
fullMat = create_matrix()
bookMat = create_book_feature_matrix()

users = [0] * 10
user_swipe_args = reqparse.RequestParser()
user_swipe_args.add_argument("init_flag", type=int, help="init flag is required")
user_swipe_args.add_argument("book_id", type=int, help="Book id is required")
user_swipe_args.add_argument("sentiment", type=str, help="swipe sentiment is required")

def abort_if_id_dne(user_id):
    if db.collect.find({"_id": user_id}).count()==0:
        abort(404, message="Could not find user")

def abort_if_id_exists(user_id):
    if db.collect.find({"_id": user_id}).count()>0:
        abort(409, message="User already exists")

class Book(Resource):
    def get(self, user_id):
        #abort_if_id_dne(user_id)
        recs = get_recs(user_id)
        return jsonify(jsonify({recs[0]}), jsonify(jsonify(recs[1])), jsonify(jsonify({recs[2])), jsonify(jsonify(recs[3])), jsonify(jsonify(recs[4])))

    def put(self, user_id):
        #abort_if_id_dne(user_id)
        args = user_swipe_args.parse_args()
        book_id = args["book_id"]
        sentiment = args["sentiment"]
        update_model(user_id,args["init_flag"],(book_id,sentiment))
        return (book_id,sentiment) #not used

    def delete(self, user_id):
        collect.delete_one({"_id": user_id})
        return '', 204

api.add_resource(Book, "/book/<int:user_id>")

app.run(debug=True)