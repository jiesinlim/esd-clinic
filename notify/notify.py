from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

#update appointment status from matched to confirmed
matched_URL = environ.get('appointment_URL') or "http://127.0.0.1:5005/appointment/status/matched" 

#send patient_name, email, appointment_time to notification.py
notification_url = environ.get('notification_URL') or "http://127.0.0.1:5003/notification" 

@app.route("/confirm/all", methods=['GET'])
def displayMatchedAppts():
    # Invoke the appointment microservice
    print('\n-----Invoking appointments microservice-----')
    try:
    # do the actual work
        result = getMatchedAppts()
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

def getMatchedAppts():
    print('\n-----Invoking appt microservice-----')
    matchedAppts = invoke_http(matched_URL, method='GET')
    print('Matched Appts:', matchedAppts)
    return matchedAppts

@app.route("/confirm/confirmAppts", methods = ['PATCH'])
def confirm_appointments():
    if request.is_json:
        try:
            data = request.get_json()

            patient_name = data['patient_name']
            email = data['email']
            appt_time = data['appointment_time']
            appt_id = data['appointment_id']

            # do the actual work
            result = updateConfirmDetails(appt_id,patient_name,email,appt_time)
            return result, result["code"]

        except Exception as e:
            pass  # do nothing.

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

def updateConfirmDetails(appt_id,patient_name,email,appt_time):
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
    updateStatus = invoke_http(matched_URL, method='PATCH', json=appt_details)
    print('Update result:', updateStatus)

    print('\n-----Invoking notification microservice-----')

    notify_patient = {
            "patient_name": patient_name,
            "email": email,
            "appointment_time": appt_time
            }

    notification_details = json.dumps(notify_patient)

    print(notification_details)
    notification = invoke_http(notification_URL, method='PATCH', json=notification_details)
    print('Notification result:', notification)

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
        ": notify patient ...")
    app.run(host='0.0.0.0', port=5006, debug=True)