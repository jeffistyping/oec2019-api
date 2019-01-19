from flask import Flask, request, jsonify, redirect, url_for, session, logging, send_from_directory
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import json
from passlib.hash import sha256_crypt
import datetime
import os


# MediHelper API
'''
The Medihelper API allows users to report medical checkup data to the database 
and allow healthcare professionals to quickly screeen issues to determine if a follow up
is required.
'''

# Database Connection Setup
user = os.environ.get('URI_USER')
password = os.environ.get('URI_PASS')
uri = 'mongodb://' + user + ':' + password + '@ds161104.mlab.com:61104/ryeoec2019'
client = MongoClient(uri, connectTimeoutMS=30000)
db = client.get_database("ryeoec2019")
hospital = db.hospital

# Application Startup
app = Flask(__name__)
CORS(app)

@app.route('/send', methods=['GET','POST'])
def send():
	form = RegisterForm(request.form)
	if request.method == 'POST' and hospital.find_one({"name": form.name.data}) == None:
		name = request.form['name']
		gender = request.form['gender']
		pnumber = request.form['phonenumber']
		symptoms = request.form['symptoms']
		doctor = request.form['doctor']
		apptdate = request.form['apptdate']
		post_data = {
    		'name': name,
    		'gender': gender,
    		'pnumber': pnumber,
    		'symptoms': symptoms,
    		'doctor': doctor,
    		'apptdate': apptdate,
    		'date': datetime.datetime.utcnow()
    	}
		result = hospital.insert_one(post_data)
		return name
	return "An account already exists"

@app.route("/api")
def api():
	return "/send - POST client data <br/> /login - Doctors Login"

# @app.route('/login', methods=['GET','POST'])
# def login():
# 	form = RegisterForm(request.form)
# 	if request.method == 'POST':
# 		name = form.name.data
# 		password = sha256_crypt.encrypt(str(form.password.data))
# 		if hospital.find_one({"name": form.name.data}) != None:
# 			try_login = hospital.find_one({"name": form.name.data})
# 			if try_login['password'] == password:
# 				session

if __name__ == "__main__":
	app.run()
