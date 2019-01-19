from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import json
import datetime 
import pprint
from creds import *

user, password = creds()

uri = 'mongodb://' + user + ':' + password + '@ds161104.mlab.com:61104/ryeoec2019'

client = MongoClient(uri, connectTimeoutMS=30000)
db = client.get_database("ryeoec2019")
hospital = db.hospital

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
	app.run()
