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
from sqlalchemy import *
from flask_cors import CORS
from datetime import datetime
import json

import os, sys
from os import environ

app = Flask(__name__)
#REMEMBER TO CHANGE WINDOWS OR MAC ROOT or ROOT:ROOT
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/appointment' or 'mysql+mysqlconnector://root:root@localhost:3306/appointment' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Appointments(db.Model):
    __tablename__ = 'appointment' 

    appointment_id = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.VARCHAR(9), nullable=False)
    patient_name = db.Column(db.VARCHAR(50), nullable=False)
    gender = db.Column(db.VARCHAR(1) , nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.VARCHAR(50) ,nullable=False) 
    appointment_date = db.Column(db.VARCHAR(20), nullable=False)
    appointment_time = db.Column(db.VARCHAR(9), nullable=False)
    did = db.Column(db.Integer, nullable=True)
    aid = db.Column(db.Integer, nullable=True)
    doctor_name = db.Column(db.VARCHAR(50), nullable=True)
    status = db.Column(db.VARCHAR(10), nullable=False)
    room_no = db.Column(db.VARCHAR(10), nullable=True)

    def __init__(self, NRIC, patient_name, gender, contact_number, email, appointment_date, appointment_time, did, aid, doctor_name, status, room_no):
        self.NRIC = NRIC
        self.patient_name = patient_name
        self.gender = gender
        self.contact_number = contact_number
        self.email = email
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.did = did
        self.aid = aid
        self.doctor_name = doctor_name
        self.status = status
        self.room_no = room_no

    def json(self):
        return {"appointment_id": self.appointment_id, "NRIC": self.NRIC, "patient_name": self.patient_name, 
                "gender": self.gender, "contact_number": self.contact_number, 
                "email": self.email, "appointment_date": self.appointment_date, 
                "appointment_time": self.appointment_time, "did": self.did, "aid": self.aid, 
                "doctor_name": self.doctor_name, "status": self.status, "room_no": self.room_no}

#----------------------------------------------------------------------------------------------------------------
# Get all the appointments
# [GET]

@app.route("/appointment/all")
def get_all_appointments():
    appointments = Appointments.query.all()
    if len(appointments):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointments": [record.json() for record in appointments]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no appointments."
        }
    ), 404

#----------------------------------------------------------------------------------------------------------------
# Get appointment details using appointment id
# [GET] 
@app.route("/appointment/<string:appointment_id>")
def get_appointment_details(appointment_id):
    appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
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

#----------------------------------------------------------------------------------------------------------------
# Get appointment details using NRIC
# [GET] 
@app.route("/appointment/nric/<string:NRIC>")
def get_appointment_details_by_nric(NRIC):
    appointments = Appointments.query.filter(Appointments.NRIC.like(NRIC)).all()

    if appointments:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointments": [record.json() for record in appointments]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Appointment not found."
        }
    ), 404

#----------------------------------------------------------------------------------------------------------------
# Add a new appointment
# [POST] 
@app.route("/appointment", methods=['POST'])
def add_new_appointment():
    add_NRIC = request.json.get('NRIC', None)

    appointment_check = Appointments.query.filter(Appointments.NRIC.like(add_NRIC)).first()
    if (appointment_check):
        return jsonify(
            {
                "code": 400,
                "data": appointment_check.json(),
                "message": "Appointment already exists."
            }
        ), 400

    data = request.get_json()
    appointment = Appointments(**data)

    try:
        db.session.add(appointment)
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the new appointment"
            }
        ), 500 
        
    return jsonify(
        {
            "code": 201,
            "data": appointment.json()
        }
    ), 201 


#----------------------------------------------------------------------------------------------
# Change Date & Time of appointment 
# [PATCH] 
@app.route("/appointment", methods=['PATCH'])
def change_appointment_details():
    if request:
        data = request.get_json()
        data = json.loads(data)

        appointment_id = data['appointment_id']
        appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()

    # appointment_id = request.json.get('appointment_id', None)
    # appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
        if appointment:

            if data['appointment_date']:
                appointment.appointment_date = data['appointment_date']
            if data['appointment_time']:
                appointment.appointment_time = data['appointment_time']
            if data['did']:
                appointment.did = data['did']
            if data['doctor_name']:
                appointment.doctor_name = data['doctor_name']
            if data['status']:
                appointment.status = data['status']

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
                "appointment_id": appointment_id
            },
            "message": "Appointment not found."
        }
    ), 404

#----------------------------------------------------------------------------------------------
# Delete appointment details
# [DELETE]
@app.route("/appointment/<string:appointment_id>", methods=['DELETE'])
def delete_appointment_details(appointment_id):
    appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointment_id": appointment_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "appointment_id": appointment_id
            },
            "message": "Appointment not found."
        }
    ), 404



# #
# # Get all new appointments made
# # [GET] 
# # /appointment/{booked}
# @app.route("/appointment/<string:booked>")
#     def get_all_appointments():
#         pass

# Get booked/matched appointments

@app.route("/appointment/status/<string:status>")
def get_appointments_by_status(status):
    appointments = Appointments.query.filter(Appointments.status.like(status)).all()

    if appointments:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointments": [record.json() for record in appointments]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no appointments."
        }
    ), 404



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
@app.route("/appointment/nextday/<string:date>")
def get_appointments_by_next_day(date):
    # appointments = Appointments.query.filter(Appointments.appointment_date.like(date)).all()
    status = "matched"
    appointments = Appointments.query.filter(Appointments.appointment_date.like(date), Appointments.status.like(status)).all()

    if appointments:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointments": [record.json() for record in appointments]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no appointments."
        }
    ), 404

#----------------------------------------------------------------------------------------------
# Change Date & Time of appointment
# [PATCH]


@app.route("/appointment/update", methods=['PATCH'])
def update_appointment_details():
    if request:
        data = request.get_json()
        data = json.loads(data)

        appointment_id = data['appointment_id']
        appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()

        if appointment:
            if data['appointment_date']:
                appointment.appointment_date = data['appointment_date']
            if data['appointment_time']:
                appointment.appointment_time = data['appointment_time']
            if data['did']:
                appointment.did = data['did']
            if data['doctor_name']:
                appointment.doctor_name = data['doctor_name']
            if data['status']:
                appointment.status = data['status']

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
                "appointment_id": appointment_id
            },
            "message": "Appointment not found."
        }
    ), 404

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": patient appointment ...")
    app.run(host='0.0.0.0', port=5005, debug=True)


