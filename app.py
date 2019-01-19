from flask import Flask, request, jsonify, redirect, url_for, session, logging, send_from_directory
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import json
from creds import *
from passlib.hash import sha256_crypt

user, password = creds()

uri = 'mongodb://' + user + ':' + password + '@ds161104.mlab.com:61104/ryeoec2019'

client = MongoClient(uri, connectTimeoutMS=30000)
db = client.get_database("ryeoec2019")
hospital = db.hospital

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		# push to db
		return True
	return False

@app.route('/login', methods=['GET','POST'])
def login():
	form = RegisterForm(reque)


if __name__ == "__main__":
	app.run()
