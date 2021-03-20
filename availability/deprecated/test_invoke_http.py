# test_invoke_http.py
from invokes import invoke_http

# invoke book microservice to get all books
results = invoke_http("http://localhost:6000/doctor", method='GET')

print( type(results) )
print()
print( results )

# invoke book microservice to create a book
did = '4'
doctor_details = {"name": "Dr Strange", "date": "2021-03-24", "availability": "0900, 1000, 1300"}
create_results = invoke_http(
        "http://localhost:6000/doctor/" + did, method='POST', 
        json=doctor_details
    )

print()
print( create_results )


# invoke book microservice to get filtered available doctors for timeslot
appointment = '2021-03-23+1900'
results = invoke_http("http://localhost:6000/doctor/" + appointment, method='GET')

print( type(results) )
print()
print( results )
