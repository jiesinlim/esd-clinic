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

#doctor_URL = "http://localhost:5000/doctor"
doctoravail_URL = environ.get('doctoravail_URL') or "http://localhost:6000/doctor"
error_URL = "http://localhost:5004/error"


@app.route("/indicate_avail", methods=['POST'])
def indicate_avail():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            indicate = request.get_json()
            print("\nReceived an indicated availability in JSON:", indicate)

            # do the actual work
            # 1. Send order info {cart items}
            result = processIndicateAvail(indicate)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "indicate_avail.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processIndicateAvail(indicate):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking doctoravail microservice-----')
    doctoravail_result = invoke_http(doctoravail_URL, method='POST', json=indicate)
    print('doctoravail_results:', doctoravail_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = doctoravail_result["code"]

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Invoking error microservice as indicate_avail fails-----')
        invoke_http(error_URL, method="POST", json=doctoravail_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Doctor availability status ({:d}) sent to the error microservice:".format(code), doctoravail_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"indicate_avail_result": doctoravail_result},
            "message": "Indicate availability failure sent for error handling."
        }

    return {
        "code": 201,
        "data": {
            "doctoravail_result": doctoravail_result
        }
    }


    

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=6100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
