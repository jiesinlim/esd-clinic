from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/esd_clinic' or 'mysql+mysqlconnector://root:root@localhost:3306/esd_clinic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    pid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.VARCHAR(15), nullable=False)
    appointment_date = db.Column(db.Date(), nullable=False)
    appointment_time = db.Column(db.VARCHAR(15), nullable=False)
    did = db.Column(db.Integer(), nullable=True)
    doctor_name = db.Column(db.VARCHAR(15), nullable=True)
    status = db.Column(db.VARCHAR(10), nullable=False)
    

    def __init__(self, pid, name, appointment_date, appointment_time, did, doctor_name, status):
        self.pid = pid
        self.name = name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.did = did
        self.doctor_name = doctor_name
        self.status = status

    def json(self):
        return {"pid": self.pid, "name": self.name, "appointment_date": self.appointment_date, "appointment_time": self.appointment_time, "did": self.did, "doctor_name": self.doctor_name, "status": self.status}

#add to patient microservice
@app.route("/nurse")
def get_all():
    patientrecords = Patient.query.all()
    if len(patientrecords):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "patients": [record.json() for record in patientrecords]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no patients."
        }
    ), 404

#add find_by_appointmentslot function to doctoravail.py
# @app.route("/doctor/<string:appointment>")  #syntax of appointment = "YYYY-MM-DD+HHMM"
# def find_by_appointmentslot(appointment):
#     appointment_date = appointment[0:10]
#     appointment_time = appointment[11:]
    
#     #doctor avail matches patient booking
#     avail_doctors = Doctor.query.filter_by(appointment_date=appointment_date, appointment_time=appointment_time) #gets a list of doctors

#     if avail_doctors:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "avail_doctors":[doctor.json() for doctor in avail_doctors]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are currently no doctors available at this appointment timeslot."
#         }
#     ), 404


@app.route("/nurse/<string:pid>", methods=['PATCH'])
def match_doctor(pid):
    patient = Patient.query.filter_by(pid=pid).first()
    if patient:
        data = request.get_json()
        if data['doctor_name']:
            patient.doctor_name = data['doctor_name']
        if data['did']:
            patient.did = data['did']
        if data['doctor_name'] and data['did']:
            patient.status = "Matched" 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "pid": pid
            },
            "message": "Patient not found in booked appointments."
        }  
    ), 404


@app.route("/nurse/confirm", methods=['PATCH'])
def confirm(pid):  #confirm and notify using AMQP
    patient = Patient.query.filter_by(pid=pid).first()
    if patient:
        data = request.get_json()  #returns data of  "confirm" when nurse clicks confirm
        if patient.status == "Matched" and data == "confirm":
            patient.status = "Confirmed" 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "pid": pid
            },
            "message": "Patient not found in matched appointments."
        }  
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
