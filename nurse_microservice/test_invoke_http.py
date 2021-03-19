# test_invoke_http.py
from invokes import invoke_http

# invoke book microservice to get all books
results = invoke_http("http://localhost:5000/nurse", method='GET')

print( type(results) )
print()
print( results )

# invoke nurse microservice to update assigned doctor
pid = "2"
assigned_doctor = {"did": 1, "doctor_name": "Dr. Marcus", "status": "Matched"}
update_patient = invoke_http(
        "http://localhost:5000/nurse/" + pid, method='PATCH', 
        json = assigned_doctor
    )

print()
print( update_patient )

# invoke book microservice to create a book
# pid = "6"
# patient_record = { "name": 5, "appointment_date": "21/03/2021", "appointment_time": "1500", "did": None, "doctor_name": None, "status": "booked" }
# create_patient = invoke_http(
#         "http://localhost:5000/nurse/" + pid, method='POST', 
#         json=patient_record
#     )

# print()
# print( create_patient )
