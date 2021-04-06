# test_invoke_http.py
from invokes import invoke_http

# invoke appointment microservice to get all matched appointments
results = invoke_http("http://localhost:5005/appointment/status/matched", method='GET')

print( type(results) )
print()
print( results )

confirmed = invoke_http("http://localhost:5005/appointment/status/confirmed", method='GET')
print( confirmed )