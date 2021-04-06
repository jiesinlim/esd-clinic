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
appointment_URL = environ.get('appointment_URL') or "http://127.0.0.1:5005/appointment"
# add patient booked datetime to doctor_URL
# update doctor availability (remove alr matched timeslot)
availability_URL = environ.get('availability_URL') or "http://127.0.0.1:5001/availability"




@app.route("/match_doctor", methods=['PATCH'])
def matchDoctor():
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
    availability_result = invoke_http(availability_URL, method='PATCH', json=updatedAvailability)
    print('Availability results:', availability_result)

    #Check the result; if a failure send it to the error microservice
    code = availability_result["code"]
    message = json.dumps(availability_result)

    if code not in range (200,300):
        print('\n\n-----Publishing the (availability error) message-----')

        return {
            "code": 500,
            "data": {"availability_result": availability_result},
            "message": "Availability update failure sent for error handling."
        }

    else:
        print('\n\n-----All is good-----')
        return availability_result

#This works
# def getAvailabilityByDateTime(datetime):
#     availabilities = invoke_http(doctor_URL + 'datetime/' + str(datetime), method='GET')
#     return availabilities

# #This is the same as the one is availability
@app.route("/availdoctors/<string:datetime>", methods=['GET'])
def getAvailDoctorsbyDatetime(datetime):

    # if request.is_json:
    if datetime:
        try:
            # data = request.get_json() #pass data of patient's appt time and date
            # date = data.appointment_date
            # time = data.appointment_time
            print("\nReceived a patient's appointment date & time:", datetime)

        # do the actual work
            result = getAvailDoctors(datetime)
            return result, result["code"]

        except Exception as e:
            pass  # do nothing.

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# @app.route("/nurse/<string:pid>", methods=['PATCH'])
# def match_doctor(pid):
#     patient = Patient.query.filter_by(pid=pid).first()
#     if patient:
#         data = request.get_json()
#         if data['doctor_name']:
#             patient.doctor_name = data['doctor_name']
#         if data['did']:
#             patient.did = data['did']
#         if data['doctor_name'] and data['did']:
#             patient.status = "Matched" 
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": patient.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "pid": pid
#             },
#             "message": "Patient not found in booked appointments."
#         }  
#     ), 404


# @app.route("/nurse/confirm", methods=['PATCH'])
# def confirm(pid):  #confirm and notify using AMQP
#     patient = Patient.query.filter_by(pid=pid).first()
#     if patient:
#         data = request.get_json()  #returns data of  "confirm" when nurse clicks confirm
#         if patient.status == "Matched" and data == "confirm":
#             patient.status = "Confirmed" 
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": patient.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "pid": pid
#             },
#             "message": "Patient not found in matched appointments."
#         }  
#     ), 404


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
        " for matching a doctor to the patient...")
    app.run(host='0.0.0.0', port=5002, debug=True)
