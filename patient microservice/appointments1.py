#assumption1:patient's unique key is NRIC.
#assumption2:patient need to create account first, then can book an appointment.
#assumption3:each patient can only book one appointment. (NRIC, Appt_date, Appt_time)
#assumption4: whole row of appointment details will be deleted in our data base once patient cancelled the appointment
#<schema_name>.<table_name>.<column_name>

#own notes
#partial update = PATCH
#change whole thing = PUT

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/appointment' or 'mysql+mysqlconnector://root@localhost:3306/appointment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    nric = db.Column(db.VARCHAR(9), primary_key=True)
    patient_name = db.Column(db.VARCHAR(15), nullable=False)
    gender = db.Column(db.Column(db.VARCHAR(15)) , nullable=False)
    # !!!!! need to find the actual one for F/M
    contact_number = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.VARCHAR(15) ,nullable=False) 

    def __init__(self, nric, patient_name, gender, contact_number, email):
        self.nric = nric
        self.patient_name = patient_name
        self.gender = gender
        self.contact_number = contact_number
        self.email = email

    def json(self):
        return {"nric": self.nric, "patient_name": self.patient_name, 
                "gender": self.gender, "contact_number": self.contact_number, 
                "email": self.email}

class Appointments(db.Model):
    __tablename__ = 'appointment'
    
    #aid is auto-generated
    # aid = db.Column(primary_key=True, db.ForeignKey(
    #     'appointment.aid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    
    # !!! need to test which code can auto-increment the aid
    aid = db.Column(db.Integer, primary_key=True)
    nric = db.Column(db.VARCHAR(10), nullable=False)
    appointment_date = db.Column(db.appointment_date, nullable=False)
    appointment_time = db.Column(db.appointment_time, nullable=False)
    did = db.Column(db.Integer, nullable=True)
    status = db.Column(db.VARCHAR(10), nullable=True)
    room_no = db.Column(db.VARCHAR(10), nullable=True)

    def __init__(self, aid, pid, did, date, time, status, room_no):
        self.aid = aid
        self.nric = nric
        self.did = did
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.room_no = room_no

    def json(self):
        return {"aid": self.aid, "nric":self.nric, 
                "did": self.did, "date": self.appointment_date, 
                "time": self.appointment_time, "status": self.status,
                "room_no": self.room_no}

# Add new appointment
# [POST] 
# /appointment 
@app.route("/appointment", methods=['POST'])
def add_new_appointment(nric, appointment_date, appointment_time):
    # !!!!! need to check if the inputs are correct?
    if (Appointments.query.filter_by(nric=nric, appointment_date=appointment_date, appointment_time=appointment_time).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "nric": nric,
                    "appointment_date": appointment_date,
                    "appointment_time" : appointment_time
                },
                "message": "Appointment already exists."
            }
        ), 400

    data = request.get_json()
    appointment = Appointments(nric, appointment_date, appointment_time, **data)

    try:
        db.session.add(appointment)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "nric": nric,
                    "appointment_date": appointment_date,
                    "appointment_time" : appointment_time
                },
                "message": "An error occurred adding the new appointment"
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": appointment.json()
        }
    ), 201
		
# Get appointment details
# [GET] 
# /appointment?status={booked/confirmed}
@app.route("/appointment/<string:aid>")
def get_appointment_details(aid):
    appointment = Appointment.query.filter_by(aid=aid).first()
    if appointment:
        return jsonify(
            {
                "code": 200,
                "data": appointment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Appointment not found."
        }
    ), 404

# Change Date & Time of appointment 
# [PUT] 
# /appointment/{appointmentID}
@app.route("/appointment/<string:aid>", methods=['PUT'])
def change_appointment_details(aid):
    appointment = appointment.query.filter_by(aid=aid).first()
    if appointment:
        data = request.get_json()
        if data['appointment_date']:
            appointment.appointment_date = data['appointment_date']
        if data['appointment_time']:
            appointment.appointment_time = data['appointment_time']
        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": appointment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "aid": aid
            },
            "message": "Appointment not found."
        }
    ), 404

# Delete appointment details
# [GET]
# /appointment?status={booked/confirmed}
@app.route("/appointment/<string:aid>", methods=['DELETE'])
def delete_appointment_details(aid):
    appointment = Appointment.query.filter_by(aid=aid).first()
    if appointment:
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "aid": aid
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "aid": aid
            },
            "message": "Appointment not found."
        }
    ), 404

# # -----------NURSE below-------------------------
# # Get all new appointments made
# # [GET] 
# # /appointment/{booked}
# @app.route("/appointment/<string:booked>")
#     def get_all_appointments():
#         pass

# # Get all next day appointments
# # [GET] 
# # /appointment?date={next day}
# @app.route("/appointment?date={next_day}")
#     def get_all_next_day_appointments():
#         pass

# # Update appointment
# # [PUT] 
# # /appointment/{appointmentID}
# @app.route("/appointment/{appointmentID}")
#     def update_appointment():
#         pass
# # -------------------------------------------------

if __name__ == '__main__':
    app.run(port=5000, debug=True)


