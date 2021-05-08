from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bookuser-db'
app.config["MONGO_URI"] = "mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority"
api = Api(app)
mongo = PyMongo(app)


client = pymongo.MongoClient("mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority")
db = client["book-recommender"]
collect = db["user-data"]

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("_id", type=int, help = "user id required", required=True)
user_put_args.add_argument("book 1 id", type=int, help="book 1 id required", required=True)
user_put_args.add_argument("book 1 rating", type=int, help="book 1 rating required", required=True)
user_put_args.add_argument("book 2 id", type=int, help="book 2 id required", required=True)
user_put_args.add_argument("book 2 rating", type=int, help="book 2 rating required", required=True)
user_put_args.add_argument("book 3 id", type=int, help="book 3 id required", required=True)
user_put_args.add_argument("book 3 rating", type=int, help="book 3 rating required", required=True)
user_put_args.add_argument("book 4 id", type=int, help="book 4 id required", required=True)
user_put_args.add_argument("book 4 rating", type=int, help="book 4 rating required", required=True)
user_put_args.add_argument("book 5 id", type=int, help="book 5 id required", required=True)
user_put_args.add_argument("book 5 rating", type=int, help="book 5 rating required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("book_id", type=int, help="Book id is required")
user_update_args.add_argument("sentiment", type=str, help="swipe sentiment is required")

def abort_if_id_dne(user_id):
    if db.collect.find({"_id": user_id}).count()==0:
        abort(404, message="Could not find user")

def abort_if_id_exists(user_id):
    if db.collect.find({"_id": user_id}).count()>0:
        abort(409, message="User already exists")

class User(Resource):
    def get(self, user_id):
        abort_if_id_dne(user_id)
        #get a book rec from back end and return the book id
        return jsonify(jsonify({"book id":1, "book title": "book one", "author name": "author one", "url":"url1"}), #just a template to remember the format to return
        jsonify(jsonify({"book id":2, "book title": "book two", "author name": "author two", "url":"url2"})),
        jsonify(jsonify({"book id":3, "book title": "book three", "author name": "author three", "url":"url3"})),
        jsonify(jsonify({"book id":4, "book title": "book four", "author name": "author four", "url":"url4"})),
        jsonify(jsonify({"book id":5, "book title": "book five", "author name": "author five", "url":"url5"})))

    def put(self, user_id):
        # check if user_id and args["_id"] are the same!!!
        args = user_put_args.parse_args()
        print(args["_id"])
        abort_if_id_exists(args["_id"])
        collect.insert_one(args)
        #args is a list of book id/rating tuples for a specific user
        return {"entry": args}, 201

    def delete(self, user_id):
        collect.delete_one({"_id": user_id})
        return '', 204

    
    def patch(self, user_id):
        abort_if_id_dne(user_id)
		args = user_update_args.parse_args()
        book_id = args["book_id"]
        sentiment = args["sentiment"]
		result = db.collect.findOne({"_id":user_id})
        #if not result["swipes"]:
        #not done

		return result

api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)