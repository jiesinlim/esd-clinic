#From flask import Flask, request, jsonify
from os import environ
import os
import amqp_setup

monitorBindingKey='send.email'

#app = Flask(__name__)

#retrieve name, email address & date\time of appt
#@app.route("/notification", methods=['PATCH'])
def send_notif():
    amqp_setup.check_setup()
        
    queue_name = 'Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processInfo(json.loads(body))
    print() # print a new line feed

def processInfo(data):
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    #dissect the info here and put it into payload

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
        reply = json.dumps(
        {
            "code": 200,
            "message": "The email is sent successfully."
        })
    else:
        reply = json.dumps(
        {
            "code": 500,
            "message": "The email failed to send."
        })
    
    print(reply)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    send_notif()