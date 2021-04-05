from flask import Flask, request, jsonify
import os
from os import environ
import requests 
from invokes import invokes_http

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

matched_appointments_URL = "http://localhost:5005/appointment/all/matched"
confirmed_appointments_URL = "http://localhost:5005/appointment/all/confirmed"

#retrieve name, email address & date\time of appt
@app.route("/notification", methods=['POST'])
def create_book():
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    #dissect the info here and put it into payload

    name = 'jiesin'
    email = 'jiesin.lim.2019@smu.edu.sg'
    appointment_time = '1100'

    msg = "Dear "+name+", \\n\\nYour appointment with G9T6 clinic will take place tomorrow at "+appointment_time+". Please arrive 5 minutes before your appointment time to check in. Thank you and see you.\\n\\nBest Regards, \\nG9T6 Clinic"

    payload = "{\"personalizations\": [{\"to\": [{\"email\":\"" + email + "\"}],\"subject\": \"Upcoming appointment details\"}],\"from\": {\"email\": \"esd.g9t6clinic@gmail.com\"},\"content\": [{\"type\": \"text/plain\",\"value\":\"" + msg + "\"}]}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "ba007e6714msh5ec101f1353401cp18c367jsncafd61131b64",
        'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    
    if(response):
        return jsonify(
        {
            "code": 200,
            "message": "The email is sent successfully."
        })
    else:
        return jsonify(
        {
            "code": 500,
            "message": "The email failed to send."
        })

#updating status from matched to confirmed
def updateConfirmDetails(appt_id,avail_id,doc_id,doc_name,time,doc_currentavail): 
    #update patient appointment with assigned doctor id and name
    # Invoke the appointment microservice
    print('\n-----Invoking appointments microservice-----')
    doctor_details = jsonify(
        {
            aid: "",
            nric: "",
            appointment_date: "",
            appointment_time: "",
            did: doc_id,
            doctor_name: doc_name,
            status: "confirmed",
            room_no: ""
        }
    )
    updateStatus = invoke_http(matched_appointments_URL, method='PATCH', json=doctor_details)
    print('Update result:', updateStatus)

def getConfirmedAppointmentDetails(patient_name,email,appointment_time): 
    #update patient appointment with confirmed status
    # Invoke the appointment microservice
    
    print('\n-----Invoking appointments microservice-----')
    getDetails = invoke_http(confirmed_appointments_URL, method='GET')
    print('Get result:', getDetails)

@app.route("/appointment/confirmed", methods = ['GET'])
def get_confirmed_appointments():
   try:
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

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": notification ...")
    app.run(host='0.0.0.0', port=5003, debug=True)

