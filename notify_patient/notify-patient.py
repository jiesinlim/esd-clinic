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
appointment_URL = environ.get('appointment_URL') or "http://127.0.0.1:5005/appointment/"

#send patient_name, email, appointment_time to notification.py
notification_url = environ.get('notification_URL') or "http://127.0.0.1:5003/notification/" 

@app.route("/notify-patient", methods=['PATCH'])
def updateConfirmDetails():
    if request.is_json:
        try: 
            appointment = request.get_json()
            print("\nReceived a status update in JSON:", appointment)

            result = updateStatus(appointment)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            print(str(e))

            return jsonify({
                "code": 500,
                "message": "notify-patient.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

#This function updates status of appointments

def updateStatus(updatedStatus):
    print('\n-----Invoking appointment microservice-----')
    status_result = invoke_http(
        appointment_URL, method='PATCH', json=updatedStatus)
    print('Status results:', status_result)

    #Check the result; if a failure send it to the error microservice
    code = status_result["code"]
    message = json.dumps(status_result)

    if code not in range(200, 300):
        print('\n\n-----Publishing the (appointment error) message-----')

        return {
            "code": 500,
            "data": {"appointment_result": status_result},
            "message": "Appointment update failure sent for error handling."
        }

    else:
        print('\n\n-----All is good-----')
        return status_result


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
        ": notify patient ...")
    app.run(host='0.0.0.0', port=5006, debug=True)