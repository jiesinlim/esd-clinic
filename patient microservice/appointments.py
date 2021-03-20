from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/esd_clinic' or 'mysql+mysqlconnector://root:root@localhost:3306/esd_clinic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    pid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.VARCHAR(15), nullable=False)
    appointment_date = db.Column(db.Date(), nullable=False)
    appointment_time = db.Column(db.VARCHAR(15), nullable=False)
    did = db.Column(db.Integer(), nullable=True)
    doctor_name = db.Column(db.VARCHAR(15), nullable=True)
    status = db.Column(db.VARCHAR(10), nullable=False)
    

    def __init__(self, pid, name, appointment_date, appointment_time, did, doctor_name, status):
        self.pid = pid
        self.name = name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.did = did
        self.doctor_name = doctor_name
        self.status = status

    def json(self):
        return {"pid": self.pid, "name": self.name, "appointment_date": self.appointment_date, "appointment_time": self.appointment_time, "did": self.did, "doctor_name": self.doctor_name, "status": self.status}

@app.route("/doctor") # Doctor microservice also have the same code
def get_all():
    doctorlist = Doctor.query.all()
    if len(doctorlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "doctoravail": [doctor.json() for doctor in doctorlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no doctors."
        }
    ), 404

#patient creating a new appointment request
@app.route("/appointment", methods=['POST'])
def create_appointment():
    pid = request.json.get('pid', None) #to consider if one patient can only make one appt??
    appointment = Patient(pid=pid, status='NEW')

    ####### stop for a while
    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            book_id=item['book_id'], quantity=item['quantity']))


#for reference
""" customer_id = request.json.get('customer_id', None)
    order = Order(customer_id=customer_id, status='NEW')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            book_id=item['book_id'], quantity=item['quantity'])) """


    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the new appointment. " + str(e)
            }
        ), 500
    
    print(json.dumps(order.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
