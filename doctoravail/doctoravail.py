from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#Mac: set dbURL=mysql+mysqlconnector://root:root@localhost:3306/doctor python doctoravail.py
#Windows: set dbURL=mysql+mysqlconnector://root@localhost:3306/doctor python doctoravail.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Doctor(db.Model):
    __tablename__ = 'doctor'

    did = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(26), nullable=False)
    date = db.Column(db.Date, nullable=False)
    availability = db.Column(db.VARCHAR(1000), nullable=True)

    def __init__(self, did, name, date, availability):
        self.did = did
        self.name = name
        self.date = date
        self.availability = availability

    def json(self):
        return {"did": self.did, "name": self.name, "date": self.date, "availability": self.availability}

#http://127.0.0.1:6000/doctor
#postman link: https://app.getpostman.com/join-team?invite_code=070d8129eba91022935f3c488d0ed83b 
@app.route("/doctor")
def get_all():
    doctorlist = Doctor.query.all()
    if len(doctorlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "doctoravail": [doctor.json() for doctor in doctorlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no doctors."
        }
    ), 404

#http://127.0.0.1:6000/doctor/1
@app.route("/doctor/<string:did>")
def find_by_did(did):
    doctor = Doctor.query.filter_by(did=did).first()
    if did:
        return jsonify(
            {
                "code": 200,
                "data": doctor.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Doctor not found."
        }
    ), 404


#http://127.0.0.1:6000/doctor/4
#{
#    "name": "Dr. Strange",
#    "date": "2021-03-24",
#    "availability": "1500, 1600, 1800"
#}
@app.route("/doctor", methods=['POST'])
def add_doctor():
    did = request.json.get('did', None)
    
    if (Doctor.query.filter_by(did=did).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "did": did
                },
                "message": "Doctor already exists in database."
            }
        ), 400

    data = request.get_json()
    doctor = Doctor(**data)

    try:
        db.session.add(doctor)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    print(json.dumps(doctor.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": doctor.json()
        }
    ), 201

##http://127.0.0.1:6000/doctor/4
#{
#    "name": "Dr. Stevens",
#    "date": "2021-03-24",
#    "availability": "1500, 1600, 1800, 1900, 2000, 2100"
#}
@app.route("/doctor/<string:did>", methods=['PUT'])
def update_doctor(did):
    doctor = Doctor.query.filter_by(did=did).first()
    if doctor:
        data = request.get_json()
        if data['name']:
            doctor.name = data['name']
        if data['date']:
            doctor.date = data['date']
        if data['availability']:
            doctor.availability = data['availability'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": doctor.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "did": did
            },
            "message": "Doctor not found."
        }
    ), 404

#http://127.0.0.1:6000/doctor/4
@app.route("/doctor/<string:did>", methods=['DELETE'])
def delete_doctor(did):
    doctor = Doctor.query.filter_by(did=did).first()
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "did": did
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "did": did
            },
            "message": "Doctor not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
