from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import json
import datetime

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:root@localhost:3306/clinic"
#run this command to connect to SQL
#Mac: export dbURL=mysql+mysqlconnector://root:root@localhost:3306/doctor python doctoravail.py
#Windows: set dbURL=mysql+mysqlconnector://root@localhost:3306/doctor python doctoravail.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Doctor(db.Model):
    __tablename__ = 'doctor'

    aid = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(26), nullable=False)
    date = db.Column(db.Date, nullable=False)
    availability = db.Column(db.VARCHAR(1000), nullable=True)

    def __init__(self, aid, did, name, date, availability):
        self.aid = aid
        self.did = did
        self.name = name
        self.date = date
        self.availability = availability

    def json(self):
        return {"aid": self.aid, "did": self.did, "name": self.name, "date": self.date, "availability": self.availability}


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

@app.route("/doctor/<string:aid>")
def find_by_aid(aid):
    doctor = Doctor.query.filter_by(aid=aid).first()
    if aid:
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


@app.route("/doctor", methods=['POST'])
def add_doctor():
    aid = request.json.get('aid', None)
    
    if (Doctor.query.filter_by(aid=aid).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "aid": aid
                },
                "message": "Doctor availability ID already exists in database."
            }
        ), 400

    data = request.get_json()
    doctor = Doctor(**data)

    try:
        db.session.add(doctor)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding doctor availability. "
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": doctor.json()
        }
    ), 201

@app.route("/doctor", methods=['PUT'])
def update_doctor():
    aid = request.json.get('aid', None)
    doctor = Doctor.query.filter_by(aid=aid).first()
    if doctor:
        data = request.get_json()
        if data['did']:
            doctor.did = data['did']
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
                "aid": aid
            },
            "message": "Doctor availability ID not found."
        }
    ), 404

@app.route("/doctor/<string:aid>", methods=['DELETE'])
def delete_doctor_avail(aid):
    doctor = Doctor.query.filter_by(aid=aid).first()
    if doctor:
        db.session.delete(doctor)
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
            "message": "Doctor availability ID not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5001, debug=True)
