from flask import Flask, request, jsonify
from os import environ
import requests

app = Flask(__name__)

#retrieve name, email address & date\time of appt
@app.route("/book/<string:info>", methods=['POST'])
def create_book(info):
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    #dissect the info here and put it into payload

    payload = "{\"personalizations\": [{\"to\": [{\"email\": \"kameolimjiesin@gmail.com\"}],\"subject\": \"Hello, World!789\"}],\"from\": {\"email\": \"jiesin.lim.2019@smu.edu.sg\"},\"content\": [{\"type\": \"text/plain\",\"value\": \"Hello, World!omggg\"}]}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "ba007e6714msh5ec101f1353401cp18c367jsncafd61131b64",
        'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

