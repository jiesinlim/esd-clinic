var get_all_appointments = "http://localhost:5005/appointment/all";
var doctor_datetime_URL = "http://127.0.0.1:5001/doctor/datetime/";

var app = new Vue({
    el: "#app",
    computed: {
        hasAppointments: function () {
            return this.appointments.length > 0;
        },
        doctorsAvail: function() {
            return this.doctors.length > 0;
        },
    },
    data: {
        message: "There is a problem retrieving appointment data, please try again later.",
        "appointments": [],
        noDrs: "There are currently no doctors available.",
        "availableDoctors": []
    },
    methods: {
        getAllAppointments: function () {
            // on Vue instance created, load the appointment list
            const response =
                fetch(get_all_appointments)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            console.log(this.appointments);
                            this.appointments = data.data.appointments;
                        }
                    })
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.message + error);

                    });
                },
        getAvailDoctors: function() {
            //on Vue instance created, load the avail doctors list
            const response =
                fetch(findByDatetime)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no doctor available in db
                            this.message = data.message;
                        } else {
                            console.log(availableDoctors);
                            this.availableDoctors = data.data.available_doctors;
                        }
                    })
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.message + error);

                    });

            },
        },
            created: function () {
            // on Vue instance created, load the appt list
            this.getAllAppointments();
        }
    });
    
