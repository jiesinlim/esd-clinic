#assumption1:patient's unique key is NRIC.
#assumption2:patient need to create account first, then can book an appointment.
#assumption3:each patient can only book one appointment. (NRIC, Appt_date, Appt_time)
#assumption4: whole row of appointment details will be deleted in our data base once patient cancelled the appointment
#<schema_name>.<table_name>.<column_name>

#own notes
#partial update = PATCH
#change whole thing = PUT


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
#REMEMBER TO CHANGE WINDOWS OR MAC ROOT or ROOT:ROOT
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/esd_clinic' or 'mysql+mysqlconnector://root:root@localhost:3306/esd_clinic' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    NRIC = db.Column(db.VARCHAR(9), primary_key=True)
    patient_name = db.Column(db.VARCHAR(50), nullable=False)
    gender = db.Column(db.VARCHAR(1) , nullable=False)
    # !!!!! need to find the actual one for F/M
    contact_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.VARCHAR(50) ,nullable=False) 

    def __init__(self, NRIC, patient_name, gender, contact_number, email):
        self.NRIC = NRIC
        self.patient_name = patient_name
        self.gender = gender
        self.contact_number = contact_number
        self.email = email

    def json(self):
        return {"NRIC": self.NRIC, "patient_name": self.patient_name, 
                "gender": self.gender, "contact_number": self.contact_number, 
                "email": self.email}

class Appointments(db.Model):
    __tablename__ = 'appointment'
    
    #aid is auto-generated
    # aid = db.Column(primary_key=True, db.ForeignKey(
    #     'appointment.aid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    
    # !!! need to test which code can auto-increment the aid
    aid = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.VARCHAR(9), nullable=False)
    appointment_date = db.Column(db.Date(), nullable=False)
    appointment_time = db.Column(db.Time(), nullable=False)
    did = db.Column(db.Integer, nullable=True)
    doctor_name = db.Column(db.VARCHAR(50), nullable=True)
    status = db.Column(db.VARCHAR(10), nullable=False)
    room_no = db.Column(db.VARCHAR(10), nullable=True)

    def __init__(self, aid, NRIC, did, doctor_name, appointment_date, appointment_time, status, room_no):
        self.aid = aid
        self.NRIC = NRIC
        self.did = did
        self.doctor_name = doctor_name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.room_no = room_no

    def json(self):
        return {"aid": self.aid, "NRIC":self.NRIC, 
                "did": self.did, "doctor_name": self.doctor_name, 
                "appointment_date": self.appointment_date, 
                "appointment_time": self.appointment_time, 
                "status": self.status, "room_no": self.room_no}



# Add new appointment
# [POST] 
@app.route("/appointment", methods=['POST'])
def add_new_appointment(NRIC, appointment_date, appointment_time):
    # !!!!! need to check if the inputs are correct?
    if (Appointments.query.filter_by(NRIC=NRIC, appointment_date=appointment_date, appointment_time=appointment_time).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "NRIC": NRIC,
                    "appointment_date": appointment_date,
                    "appointment_time" : appointment_time,
                },
                "message": "Appointment already exists."
            }
        ), 400

    data = request.get_json()
    appointment = Appointments(NRIC, appointment_date, appointment_time, status, **data)
    #!!!!! check how to add status='booked'
    
    try:
        db.session.add(appointment)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "NRIC": NRIC,
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
@app.route("/appointment/<string:aid>")
def get_appointment_details(aid):
    appointment = Appointments.query.filter_by(aid=aid).first()
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
@app.route("/appointment/<string:aid>", methods=['PUT'])
def change_appointment_details(aid):
    appointment = Appointments.query.filter_by(aid=aid).first()
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
# [DELETE]
@app.route("/appointment/<string:aid>", methods=['DELETE'])
def delete_appointment_details(aid):
    appointment = Appointments.query.filter_by(aid=aid).first()
    if appointment:
        db.session.delete(appointment)
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

# Get all appointments

# @app.route("/appointment/<string:status>")
# def get_all_appointments():
#     appointments = Appointments.query.filter_by(status=status)
#     if len(appointments):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "appointments": [record.json() for record in appointments]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no appointments."
#         }
#     ), 404

# OR

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

# if __name__ == '__main__':
#     app.run(port=5002, debug=True)

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": patient appointment ...")
    app.run(host='0.0.0.0', port=5002, debug=True)


