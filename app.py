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

@app.route('/create_doctor', methods=['GET','POST'])
def create_doctor():
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		post_data = {
    		'docname': name,
    		'password': sha256_crypt.hash(password),
    		'date': datetime.datetime.utcnow()
    	}
		result = hospital.insert_one(post_data)
		return "<h1>Doctor Profile Created!</h1>"
	return "Invalid"



@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
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
		return "yes"
	return "no"

@app.route("/api")
def api():
	return "/send - POST client data <br/> /login - POST Doctors Login"


# Doctors must be added to the database via IT Services
# Contact IT for new doctor onboarding
# DOCTOR MODEL
'''{
	docname: "doctor's name"
	password: "password"
}
'''
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		if hospital.find_one({"docname": name}) != None:
			try_login = hospital.find_one({"docname": name})
			if sha256_crypt.verify(password, try_login['password']):
				patient_names = []
				genders = []
				pnumbers = []
				symptoms = []
				doctors = []
				apptdates = []
				for patient in hospital.find({"doctor": name }):
					patient_names.append(patient['name'])
					genders.append(patient['gender'])
					pnumbers.append(patient['pnumber'])
					symptoms.append(patient['symptoms'])
					doctors.append(patient['doctor'])
					apptdates.append(patient['apptdate'])
				return jsonify({"names": patient_names, "genders": genders, "phonenumbers": pnumbers, "symptoms": symptoms, "doctors": doctors, "apptdates": apptdates})
	return jsonify({})

if __name__ == "__main__":
	app.run()
