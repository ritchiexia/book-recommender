import pandas as pd
import torch
import numpy as np
from torch import nn, optim
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
mongo = PyMongo(app)

bookFP = "goodbooks.csv"
ratingFP = "goodbooks-ratings.csv"

books = pd.read_csv(bookFP)
#Compile all non-english languages - indices determined by inspection
foreign = books["language_code"].unique()[6:].tolist()
foreign.append(books["language_code"].unique()[4])
#iterate through foreign languages keeping only books that aren't in that language
for lang in foreign:
    books = books[books["language_code"] != lang]

book_conv = { m : m-1 for m in books['book_id'] }
books['book_id'] = books['book_id'].apply(lambda m: book_conv[m]) 

conv_arr = [-1] * 10001
count = 0
#iterate through remaining books to create mapping for dataset class
for id in books["book_id"]:
    conv_arr[id] = count
    count = count + 1
#Remove unneccessary columns for Mongo Upload
books.drop("goodreads_book_id", inplace=True, axis=1)
books.drop("best_book_id", inplace=True, axis=1)
books.drop("work_id", inplace=True, axis=1)
books.drop("books_count", inplace=True, axis=1)
books.drop("isbn", inplace=True, axis=1)
books.drop("isbn13", inplace=True, axis=1)
books.drop("original_publication_year", inplace=True, axis=1)
books.drop("original_title", inplace=True, axis=1)
books.drop("language_code", inplace=True, axis=1)
books.drop("average_rating", inplace=True, axis=1)
books.drop("ratings_count", inplace=True, axis=1)
books.drop("work_ratings_count", inplace=True, axis=1)
books.drop("work_text_reviews_count", inplace=True, axis=1)
books.drop("ratings_1", inplace=True, axis=1)
books.drop("ratings_2", inplace=True, axis=1)
books.drop("ratings_3", inplace=True, axis=1)
books.drop("ratings_4", inplace=True, axis=1)
books.drop("ratings_5", inplace=True, axis=1)
books.drop("small_image_url", inplace=True, axis=1)
#Code to upload books to Mongo goes below
#Code to upload books to Mongo goes above
books_dict = books.to_dict('records')
client = pymongo.MongoClient("mongodb+srv://dbUser:cpen291@cluster0.02dfd.mongodb.net/book-recommender?retryWrites=true&w=majority")
db = client["book-recommender"]
book_collect = db["book-data"]
book_collect.insert_many(books_dict, ordered=False)

#Not sure if the below code should stay here or be elsewhere. We will need wherever we train our models. Not sure if we need it in the backnd anymore, now that book info
#is in Mongo.

class Dataset(torch.utils.data.Dataset):
    def __init__(self, fn):
        self.dataframe = pd.read_csv(fn)
        u2n = { u: n for n, u in enumerate(self.dataframe['user_id'].unique()) } 
        apply_conv = { m: conv_arr[m] for m in self.dataframe["book_id"] }
        #book_conv = { m : m-1 for m in books['book_id'] }
        #self.dataframe['book_id'] = self.dataframe['book_id'].apply(lambda m: book_conv[m]) 
        self.dataframe['user_id'] = self.dataframe['user_id'].apply(lambda u: u2n[u])
        self.dataframe["book_id"] = self.dataframe["book_id"].apply(lambda m: apply_conv[m])
        self.dataframe = self.dataframe[self.dataframe["book_id"] != -1]
        self.coords = torch.LongTensor(self.dataframe[['user_id', 'book_id']].values)
        self.ratings = torch.FloatTensor(self.dataframe['rating'].values)
        self.n_users = self.dataframe['user_id'].nunique()
        self.n_boooks = self.dataframe['book_id'].nunique()
    
    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return (self.coords[i], self.ratings[i])


ds = Dataset(ratingFP)

torch.save({
    'ds' : ds}, "ds.pt")

app.run(debug=True)