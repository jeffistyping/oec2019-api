from flask import Flask, request, jsonify, redirect, url_for, session, logging, send_from_directory
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import json
from passlib.hash import sha256_crypt
import datetime
import os

# user = os.environ.get('URI_USER')
# password = os.environ.get('URI_PASS')

user = "jadmin"
password = "ryerson2019"


uri = 'mongodb://' + user + ':' + password + '@ds161104.mlab.com:61104/ryeoec2019'

client = MongoClient(uri, connectTimeoutMS=30000)
db = client.get_database("ryeoec2019")
hospital = db.hospital
# password = sha256_crypt.encrypt("jimmy")
# gender="male"
# pnumber="109238120"
# symptoms="cough"
# post_data = {
 	#     		'name': password,
#     		'gender': gender,
#     		'pnumber': pnumber,
#     		'password': password,
#     		'symptoms': symptoms,
#     		'date': datetime.datetime.utcnow()
#     	}
# result = hospital.insert_one(post_data)
# print(hospital.find_one())


app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and hospital.find_one({"name": form.name.data}) == None:
		name = form.name.data
		gender = form.gender.data
		pnumber = form.phonenumber.data
		password = sha256_crypt.encrypt(str(form.password.data))
		symptoms = form.symptoms.data
		post_data = {
    		'name': name,
    		'gender': gender,
    		'pnumber': pnumber,
    		'password': password,
    		'symptoms': symptoms,
    		'date': datetime.datetime.utcnow()
    	}
		result = hospital.insert_one(post_data)
		hopital.find_one()
		return name
	return "An account already exists"


# @app.route('/login', methods=['GET','POST'])
# def login():
# 	form = RegisterForm(request.form)
# 	if request.method == 'POST':
# 		name = form.name.data
# 		password = sha256_crypt.encrypt(str(form.password.data))
# 		if hospital.find_one({"name": form.name.data}) != None:
# 			try_login = hospital.find_one({"name": form.name.data})



if __name__ == "__main__":
	app.run()
