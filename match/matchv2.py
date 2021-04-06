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

#build: docker build -t marcsoh/match:1.0 ./
#run:

# check correct patient url for updating patient record
appointment_URL = environ.get(
    'appointment_URL') or "http://127.0.0.1:5005/appointment"
# add patient booked datetime to doctor_URL
# update doctor availability (remove alr matched timeslot)
availability_URL = environ.get(
    'availability_URL') or "http://127.0.0.1:5001/availability"


@app.route("/update_doctor", methods=['PATCH'])
def updateDoctor():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # pass both assigned doctor and patient id and name, appt time
            availability = request.get_json()
            print("\nReceived a doctor update in JSON:", availability)

            result = processAvailability(availability)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            print(str(e))

            return jsonify({
                "code": 500,
                "message": "match.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

#This function updates availability for doctors


def processAvailability(updatedAvailability):

    print('\n-----Invoking availability microservice-----')
    availability_result = invoke_http(
        availability_URL, method='PATCH', json=updatedAvailability)
    print('Availability results:', availability_result)

    #Check the result; if a failure send it to the error microservice
    code = availability_result["code"]
    message = json.dumps(availability_result)

    if code not in range(200, 300):
        print('\n\n-----Publishing the (availability error) message-----')

        return {
            "code": 500,
            "data": {"availability_result": availability_result},
            "message": "Availability update failure sent for error handling."
        }

    else:
        print('\n\n-----All is good-----')
        return availability_result


@app.route("/match_patient", methods=['PATCH'])
def matchPatient():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # pass both assigned doctor and patient id and name, appt time
            appointment = request.get_json()
            print("\nReceived a patient update in JSON:", appointment)

            result = processAppointment(appointment)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            print(str(e))

            return jsonify({
                "code": 500,
                "message": "match.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processAppointment(updatedAppointment):
    print('\n-----Invoking appointment microservice-----')
    appointment_result = invoke_http(
        appointment_URL, method='PATCH', json=updatedAppointment)
    print('appointmentresults:', appointment_result)

    #Check the result; if a failure send it to the error microservice
    code = appointment_result["code"]
    message = json.dumps(appointment_result)

    if code not in range(200, 300):
        print('\n\n-----Publishing the (appointment error) message-----')

        return {
            "code": 500,
            "data": {"appointment_result": appointment_result},
            "message": "Appointment update failure sent for error handling."
        }

    else:
        print('\n\n-----All is good-----')
        return appointment_result


#This works
def processDateTime(datetime):
    availabilities = invoke_http(
        availability_URL + '/datetime/' + str(datetime), method='GET')
    return availabilities

#This is the same as the one is availability


@app.route("/availability/<string:datetime>", methods=['GET'])
def getAvailDoctorsbyDatetime(datetime):

    # if request.is_json:
    if datetime:
        try:
            # data = request.get_json() #pass data of patient's appt time and date
            # date = data.appointment_date
            # time = data.appointment_time
            print("\nReceived a patient's appointment date & time:", datetime)

        # do the actual work
            result = processDateTime(datetime)
            return result, result["code"]

        except Exception as e:
            pass  # do nothing.

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
          " for matching a doctor to the patient...")
    app.run(host='0.0.0.0', port=5002, debug=True)
