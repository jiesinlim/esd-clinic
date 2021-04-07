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
doctor_URL = environ.get('availability_URL') or "http://127.0.0.1:5001/availability"


def getAvailDoctors(datetime):
    # Invoke the doctor microservice
    print('\n-----Invoking doctor microservice-----')

    availDoctors = invoke_http(doctor_URL + '/datetime/' + str(datetime), method='GET')
    print('Available doctors:', availDoctors)
    return availDoctors


def updateMatchDetails(data):
    print(type(data))
    #update patient appointment with assigned doctor id and name
    # Invoke the appointment microservice
        # do the actual work
    #parse match into 6 separate values
    appt_id = data['appointment_id']
    avail_id = data['aid']
    doc_id = data['did']
    doc_name = data['d_name']
    time = data['appt_time']
    doc_currentavail = data['doc_avail']  #get this info by getting doctor's full availability by avail_id

    print('\n-----Invoking appointments microservice-----')

    details = {
                "NRIC": "",
                "aid": "",
                "appointment_date": "",
                "appointment_id": appt_id,
                "appointment_time": "",
                "contact_number": "",
                "did": int(doc_id),
                "doctor_name": str(doc_name),
                "email": "",
                "gender": "",
                "patient_name": "",
                "room_no": "",
                "status": "matched"
            }

    appt_details = json.dumps(details)
    # print(type(appt_details))
    assignDoctor = invoke_http(appointment_URL, method='PATCH', json=appt_details)
    print('Match result:', assignDoctor)



    # handle doctor availability 
    print('\n-----Invoking availability microservice-----')

    # time_array = doc_currentavail.split(", ")
    # print(time_array)
    # time_array.remove(time)
    # newAvailability = ', '.join([str(slot) for slot in time_array])
    # print(newAvailability)
    avail_obj = {
                    "aid": avail_id,
                    "availability": doc_currentavail,
                    "date": "",
                    "did": "",
                    "timeslot": time
                }

    new_avail = json.dumps(avail_obj)

    print(type(new_avail), new_avail)
    
    # update doctor(specific avail_id) availability
    # Invoke the doctor microservice

    updateAvailability = invoke_http(f'{doctor_URL}/timeslot', method='PATCH', json=new_avail)
    print('updated timeslot result:', updateAvailability)
    # result = f"Successfully assigned doctor: {assignDoctor}, Successfully updated doctor's availability: {updateAvailability}"
    return assignDoctor, updateAvailability



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
    

@app.route("/match", methods=['PATCH'])
def match_doctor():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            data = request.get_json()  #pass both assigned doctor and patient id and name, appt time
            print("\nReceived a doctor-patient match in JSON:", data)


            result = updateMatchDetails(data)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify({
                "code": 200,
                "message": "Matched"
            }), 200

        except Exception as e:
            # Unexpected error in code
            pass

            return jsonify({
                "code": 500,
                "message": "match.py internal error"
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
        " for matching a doctor to the patient...")
    app.run(host='0.0.0.0', port=5002, debug=True)
