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
matched_URL = environ.get('matched_URL') or "http://127.0.0.1:5005/appointment/status/matched" 

confirmed_URL = environ.get('confirmed_URL') or "http://127.0.0.1:5005/appointment/status/confirmed"

#send patient_name, email, appointment_time to notification.py
notification_url = environ.get('notification_URL') or "http://127.0.0.1:5003/notification" 


def updateConfirmDetails(appt_id,avail_id,doc_id,doc_name,time,doc_currentavail):
    # Invoke the appointment microservice

    print('\n-----Invoking appointments microservice-----')

    appt_details = json.dumps({
        "NRIC": "",
        "aid": "",
        "appointment_date": "",
        "appointment_id": "",
        "appointment_time": "",
        "contact_number": "",
        "did": "",
        "doctor_name": "",
        "email": "",
        "gender": "",
        "patient_name": "",
        "room_no": "",
        "status": "confirmed"
        })

    print(appt_details)
    updateStatus = invoke_http(matched_URL + str(appt_id), method='PATCH', json=appt_details)
    print('Update result:', updateStatus)


# @app.route("/appointment/status/matched", methods=['GET'])
# def getMatchedDetails():
#     # Invoke the appointment microservice
#     print('\n-----Invoking appointments microservice-----')

#     if request.is_json():
#         try:
#             data = request.get_json()

#             appt_id = data['appointment_id']
#             avail_id = data['aid']
#             doc_id = data['did']
#             doc_name = data['d_name']
#             time = data['appt_time']
#             doc_currentavail = data['doc_avail']

#             result = updateConfirmDetails(appt_id,avail_id,doc_id,doc_name,time, doc_currentavail)

#             return result, result["code"]

#         except Exception as e:
#             # Unexpected error in code
#             pass

#             return jsonify({
#                 "code": 500,
#                 "message": "match.py internal error"
#             }), 500

#     # if reached here, not a JSON request.
#     return jsonify({
#         "code": 400,
#         "message": "Invalid JSON input: " + str(request.get_data())
#     }), 400

@app.route("/appointment/status/confirmed", methods = ['GET'])
def get_confirmed_appointments():
    if request.is_json:
        try:
            data = request.get_json()

            patient_name = data['patient_name']
            email = data['email']
            appt_time = data['appointment_time']

            # do the actual work
            result = getConfirmedAppointmentDetails()
            return result, result["code"]

        except Exception as e:
            pass  # do nothing.

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

def getConfirmedAppointmentDetails(): 
    # Invoke the appointment microservice
    
    print('\n-----Invoking appointments microservice-----')
    getDetails = invoke_http(confirmed_URL, method='GET')
    print('Get result:', getDetails)

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
        ": notify patient ...")
    app.run(host='0.0.0.0', port=5006, debug=True)