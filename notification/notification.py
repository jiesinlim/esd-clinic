from flask import Flask, request, jsonify
from os import environ
import requests
import os

app = Flask(__name__)

#retrieve name, email address & date\time of appt
@app.route("/notification", methods=['POST'])
def create_book():
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    #dissect the info here and put it into payload

    payload = "{\"personalizations\": [{\"to\": [{\"email\": \"lewanna.erh.2019@smu.edu.sg\"}],\"subject\": \"Hello, World!789\"}],\"from\": {\"email\": \"jiesin.lim.2019@smu.edu.sg\"},\"content\": [{\"type\": \"text/plain\",\"value\": \"Hello, World!omggg\"}]}"
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


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": notification ...")
    app.run(host='0.0.0.0', port=5003, debug=True)

