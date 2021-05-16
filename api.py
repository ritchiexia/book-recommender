#Code developped following the following tutorials: "Python MongoDB Tutorial using PyMongo": https://www.youtube.com/watch?v=rE_bJl2GAY8 and ":"Python REST API Tutorial - Buidling a Flask REST API": https://www.youtube.com/watch?v=GMppyAPbLYk

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from backend import User, find_paired_user, RLModel, get_recs, update_model, create_matrix, create_book_feature_matrix, BookRecommenderEmbeddingML
import torch

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bookuser-db'
app.config["MONGO_URI"] = "mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority"
api = Api(app)
mongo = PyMongo(app)


client = pymongo.MongoClient("mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority")
db = client["book-recommender"]
collect = db["final-book-data"]

#Code for importing model will go here
load = torch.load('new-best-1.pt', map_location=torch.device('cpu'))
model = load['best-model']
fullMat = create_matrix(model)
bookMat = create_book_feature_matrix(model)

users = [0] * 10
ratings = []
#users[1] = User([[1,1],[2,3],[3,4],[5,5],[6,3]],fullMat,1,24,model)

@app.route("/book/<user_id>", methods=["GET"])
def get(user_id):
    #abort_if_id_dne(user_id)
    recs = get_recs(users, user_id, bookMat, collect)
    return jsonify({'one':recs[0],'two':recs[1],'three':recs[2],'four':recs[3],'five':recs[4]})

@app.route("/book/<user_id>", methods=["PUT"])
def put(user_id):
    #abort_if_id_dne(user_id)
    put_json = request.get_json()
    init_flag = put_json["init_flag"]
    book_id = put_json["book_id"]
    sentiment = put_json["sentiment"]
    alert = update_model(users, user_id, init_flag, (book_id,sentiment), ratings, fullMat, bookMat, model)
    print(alert)
    val = 0
    if alert:
        val = 1
    return {'alert' : val}, 201 #returns empty string ie no return value, and apprporiate status code, 201
    #return (book_id,sentiment) #not used

app.run(debug=True)#