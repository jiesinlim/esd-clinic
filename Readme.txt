There are 3 simple microservices, 2 complex microservices and 3 UIs in this file

Simple microservices:
1. appointment
    - HTTP
    - patient uses this microservice to book their medical appointment
    - used by 'match appointments' and 'notify patients' complex microservices
2. availability
    - HTTP
    - doctor uses this microservices to indicate their availability for medical consultations
    - used by 'match appointment' complex microservice
3. notification
    - AMQP
    - sends booking confirmation email to patients once their medical appointment has been confirmed
    - used by 'notify patient' complex microservice

Complex microservices:
1. match appointments
    - nurses uses this to match patients' bookings to doctors' availability
    - updates their respective databases once a medical appointment has been matched
2. notify patients
    - nurses uses this to notify patients via email
    - updates appointment status to 'confirmed'

UI:
1. Patient UI
2. Nurse UI
3. Doctor UI

UI template credits:
Theme Name: Reveal
Theme URL: https://bootstrapmade.com/reveal-bootstrap-corporate-template/
Author: BootstrapMade.com
Author URL: https://bootstrapmade.com