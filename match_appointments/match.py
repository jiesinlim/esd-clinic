from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import os

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# appointments_URL = "http://localhost:5000/appointment/" # check correct patient url for updating patient record
doctor_datetime_URL = "http://127.0.0.1:5001/doctor/datetime/" # add patient booked datetime to doctor_URL
doctor_URL = "http://127.0.0.1:5001/doctor/" #update doctor availability (remove alr matched timeslot)


def getAvailDoctors(datetime):
    # Invoke the doctor microservice
    print('\n-----Invoking doctor microservice-----')
    # datetime = f"{date}+{time}"
    availDoctors = invoke_http(doctor_datetime_URL + str(datetime), method='GET')
    print('Available doctors:', availDoctors)
    return availDoctors
    # availDoctors = json.loads(availDoctors)
    # for i in range(len(availDoctors)):
    #     print(availDoctors[i])

# def updateMatchDetails(appt_id,avail_id,doc_id,doc_name,time):
#     #get patient appointment by appt id
#     print('\n-----Invoking appointment microservice-----')
#     appt_details = invoke_http(appointments_URL + str(appt_id), method='GET')
#     print('appointment details:', appt_details)
#     appt_obj = json.loads(appt_details)

#     #update patient appointment with assigned doctor id and name
#     # Invoke the appointment microservice
#     print('\n-----Invoking appointments microservice-----')
#     doctor_details = jsonify(
#         {
#             aid: appt_id,
#             NRIC: appt_obj.data.NRIC,
#             appointment_date: appt_obj.data.appointment_date,
#             appointment_time: appt_obj.data.appointment_time,
#             did: doc_id,
#             doctor_name: doc_name,
#             status: appt_obj.data.status,
#             room_no: appt_obj.data.room_no
#         }
#     )
#     assignDoctor = invoke_http(appointments_URL + str(appt_id), method='PATCH', json=doctor_details)
#     print('Match result:', assignDoctor)

#     # get doctors by aid
#     print('\n-----Invoking doctor microservice-----')
#     doctor_details = invoke_http(doctor_URL + str(avail_id), method='GET')
#     print('assigned doctor result:', doctor_details)

#     # handle doctor availability 
#     avail_obj = json.loads(doctor_details)
#     currentAvail = avail_obj.data.availability
#     time_array = currentAvail.split(", ")
#     updated_array = time_array.remove(time)
#     newAvailability = ', '.join([str(slot) for slot in updated_array])
#     new_avail = jsonify(
#         {
#             aid: avail_obj.data.aid,
#             availability: newAvailability,
#             date: avail_obj.data.date,
#             did: avail_obj.data.did,
#             name: avail_obj.data.name
#         }
#     )

#     # update doctor(specific avail_id) availability
#     # Invoke the doctor microservice
#     print('\n-----Invoking appointments microservice-----')

#     updateAvailability = invoke_http(doctor_URL + str(appt_id), method='PATCH', json=new_avail)
#     print('updated timeslot result:', updateAvailability)



@app.route("/availdoctors/<string:datetime>", methods=['GET'])
def getAvailDoctorsbyDatetime(datetime):
    
    # if request.is_json:
    if datetime:
        try:
        # data = request.get_json() #pass data of patient's appt time and date
        # date = data.appointment_date
        # time = data.appointment_time
            print("\nReceived a patient's appointment date & time in JSON:", datetime)

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
    

# @app.route("/match", methods=['PATCH','GET'])
# def match_doctor():
#     # Simple check of input format and data of the request are JSON
#     if request.is_json:
#         try:
#             match = request.get_json()  #pass both assigned doctor and patient id and name, appt time
#             print("\nReceived a doctor-patient match in JSON:", match)

#             # do the actual work
#             #parse match into 4 separate values
#             appt_id = match[0]
#             did = match[1]
#             doc_name = match[2]
#             time = match[3]

#             result = updateMatchDetails(appt_id,avail_id,doc_id,doc_name,time)
#             print('\n------------------------')
#             print('\nresult: ', result)
#             return jsonify(result), result["code"]

#         except Exception as e:
#             # Unexpected error in code
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
#             print(ex_str)

#             return jsonify({
#                 "code": 500,
#                 "message": "match.py internal error: " + ex_str
#             }), 500

#     # if reached here, not a JSON request.
#     return jsonify({
#         "code": 400,
#         "message": "Invalid JSON input: " + str(request.get_data())
#     }), 400





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
