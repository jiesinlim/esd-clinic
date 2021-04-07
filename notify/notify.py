from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

import json
import amqp_setup
import pika


app = Flask(__name__)
CORS(app)

#get next day appts
appointment_URL = environ.get('appointment_URL') or "http://127.0.0.1:5005/appointment" 

@app.route("/confirm/<string:date>", methods=['GET'])
def displayMatchedAppts(date):
    # Invoke the appointment microservice
    print('\n-----Invoking appointments microservice-----')
    if date:
        try:
        # do the actual work
            result = getMatchedAppts(date)
            return result, result["code"]

        except Exception as e:
            # Unexpected error in code
            pass

            return jsonify({
                "code": 500,
                "message": "appointment.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def getMatchedAppts(date):
    print('\n-----Invoking appt microservice-----')
    matchedAppts = invoke_http(appointment_URL + '/nextday/' + str(date), method='GET')
    print('Matched Appts:', matchedAppts)
    return matchedAppts

@app.route("/confirm/confirmAppts", methods = ['PATCH'])
def confirm_appointments():
    if request.is_json:
        try:
            data = request.get_json()

            # do the actual work
            result = updateConfirmDetails(data)
            return result, result["code"]

        except Exception as e:
            pass  # do nothing.

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

def updateConfirmDetails(data):
    print(type(data))
    #update patient appointment with assigned doctor id and name
    # Invoke the appointment microservice
        # do the actual work
    #parse match into 6 separate values
    patient_name = data['patient_name']
    email = data['email']
    appt_id = data['appointment_id']
    appt_time = data['appointment_time']
 

    # appt_id = data['appointment_id']
    # patient_name = data['patient_name']
    # doc_name = data['d_name']
    # time = data['appt_time']
    # appt_date = data['appointment_date']
    # Invoke the appointment microservice

    print('\n-----Invoking appointments microservice-----')

    details = {
            "NRIC": "",
            "aid": "",
            "appointment_date": "",
            "appointment_id": appt_id,
            "appointment_time": "",
            "contact_number": "",
            "did": "",
            "doctor_name": "",
            "email": "",
            "gender": "",
            "patient_name": "",
            "room_no": "",
            "status": "confirmed"
            }

    appt_details = json.dumps(details)

    print(appt_details)
    updateStatus = invoke_http(appointment_URL, method='PATCH', json=appt_details)
    print('Update result:', updateStatus)

    print('\n-----Invoking notification microservice-----')

    notify_patient = {
            "patient_name": patient_name,
            "email": email,
            "appointment_time": appt_time
            }

    notification_details = json.dumps(notify_patient)

    print(notification_details)
    #notification = invoke_http(notification_URL, method='PATCH', json=notification_details)
    if(updateStatus["code"] in range(200, 300)):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.email", 
        body=notification_details) 

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
        ": notify patient ...")
    app.run(host='0.0.0.0', port=5006, debug=True)