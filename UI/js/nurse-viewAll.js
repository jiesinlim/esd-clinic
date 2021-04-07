var get_all_URL = "http://127.0.0.1:5005/appointment/all";

var app = new Vue({
    el: "#app",
    computed: {
        hasAppointments: function () {
            return this.appointments.length > 0;
        },
    },
    data: {
        message: "There is a problem retrieving appointment data, please try again later.",
        "appointments": [],
        "date": []
    },
    methods: {
        getAllAppointments: function () {
            // on Vue instance created, load the appointment list

            const response =
                fetch(get_all_URL)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            this.appointments = data.data.appointments;
                            if (this.appointments) {
                                for (var patient of this.appointments) {
                                    this.date.push(new Date(patient.appointment_date).toDateString());
                                }
                            }
                        }
                    })
                    
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.message + error);
                    });
        }
    },
            created: function () {
            // on Vue instance created, load the appt list
            this.getAllAppointments();
        }
    });

