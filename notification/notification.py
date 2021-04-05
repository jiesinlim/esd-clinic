from flask import Flask, request, jsonify
from os import environ
import requests
import os

app = Flask(__name__)

#retrieve name, email address & date\time of appt
@app.route("/notification", methods=['PATCH'])
def send_notif():
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    #dissect the info here and put it into payload
    data = request.get_json()

    name = data['patient_name']
    email = data['email']
    appointment_time = data['appointment_time']

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
# def updateConfirmDetails(appt_id,avail_id,doc_id,doc_name,time,doc_currentavail): 
#     #get patient appointment by appt id
#     # print('\n-----Invoking appointment microservice-----')
#     # appt_details = invoke_http(appointments_URL + str(appt_id), method='GET')
#     # print('appointment details:', appt_details)
#     # appt_obj = json.loads(appt_details)

#     #update patient appointment with assigned doctor id and name
#     # Invoke the appointment microservice
#     print('\n-----Invoking appointments microservice-----')
#     doctor_details = jsonify(
#         {
#             aid: "",
#             nric: "",
#             appointment_date: "",
#             appointment_time: "",
#             did: doc_id,
#             doctor_name: doc_name,
#             status: "Confirmed",
#             room_no: ""
#         }
#     )
#     UpdateStatus = invoke_http(appointments_URL + str(appt_id), method='PATCH', json=doctor_details)
#     print('Confirm result:', UpdateStatus)

# print('\n-----Invoking appointments microservice-----')
#     doctor_details = jsonify(
#         {
#             aid: "",
#             nric: "",
#             patient_name: "",
#             email: "",
#             appointment_date: "",
#             appointment_time: "",
#             did: doc_id,
#             doctor_name: doc_name,
#             status: "Confirmed",
#             room_no: ""
#         }
#     )
#     UpdateStatus = invoke_http(appointments_URL + str(appt_id), method='PATCH', json=doctor_details)
#     print('Confirm result:', UpdateStatus)


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": notification ...")
    app.run(host='0.0.0.0', port=5003, debug=True)

