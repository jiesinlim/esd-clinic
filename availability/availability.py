import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
# REMEMBER TO CHANGE WINDOWS OR MAC ROOT or ROOT:ROOT
#app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
    #'dbURL') or 'mysql+mysqlconnector://root@localhost:3306/availability' or 'mysql+mysqlconnector://root:root@localhost:3306/availability'

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/esd_clinic' or 'mysql+mysqlconnector://root:root@localhost:3306/esd_clinic'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Availability(db.Model):
    __tablename__ = 'availability'

    aid = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.Integer, nullable=False)
    doctor_name = db.Column(db.String(26), nullable=False)
    date = db.Column(db.Date, nullable=False)
    availability = db.Column(db.VARCHAR(1000), nullable=True)

    def __init__(self, aid, did, name, date, availability):
        self.aid = aid
        self.did = did
        self.doctor_name = name
        self.date = date
        self.availability = availability

    def json(self):
        return {"aid": self.aid, "did": self.did, "name": self.doctor_name, "date": self.date, "availability": self.availability}


@app.route("/availability")
def get_all():
    availability_list = Availability.query.all()
    if len(availability_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "doctor_availability": [availability.json() for availability in availability_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no doctors."
        }
    ), 404


@app.route("/availability/<string:aid>")
def find_by_aid(aid):
    availability = Availability.query.filter_by(aid=aid).first()
    if availability:
        return jsonify(
            {
                "code": 200,
                "data": availability.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Doctor not found."
        }
    ), 404


@app.route("/availability", methods=['POST'])
def add_doctor():
    aid = request.json.get('aid', None)

    if (Availability.query.filter_by(aid=aid).first()):
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
    availability = Availability(**data)

    try:
        db.session.add(availability)
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
            "data": availability.json()
        }
    ), 201


@app.route("/availability", methods=['PATCH'])
def update_doctor():
    aid = request.json.get('aid', None)
    availability = Availability.query.filter_by(aid=aid).first()
    if availability:
        data = request.get_json()
        if data['did']:
            availability.did = data['did']
        if data['name']:
            availability.name = data['name']
        if data['date']:
            availability.date = data['date']
        if data['availability']:
            availability.availability = data['availability']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": availability.json()
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


@app.route("/availability/<string:aid>", methods=['DELETE'])
def delete_doctor_avail(aid):
    availability = Availability.query.filter_by(aid=aid).first()
    if availability:
        db.session.delete(availability)
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


# Syntax of appointment = "YYYY-MM-DD+HHMM"
# SQL Query:
# SELECT * FROM doctor WHERE availability LIKE '%1500%' AND date LIKE '2021-03-21'
# Guide how to use LIKE https://stackoverflow.com/questions/39384923/how-to-use-like-operator-in-sqlalchemy

@app.route("/availability/datetime/<string:appointment>")
def find_by_appointmentslot(appointment):
    appointment_date = appointment[0:10]
    appointment_time = appointment[11:]

    avail_doctors = Availability.query.filter(Availability.availability.like(
        "%" + appointment_time + "%"), Availability.date.like(appointment_date)).all()

    if avail_doctors:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "available_doctors": [doctor.json() for doctor in avail_doctors]
                }

            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are currently no doctors available at this appointment timeslot."
        }
    ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": doctor availability ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
