//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_all_appts_URL = "http://127.0.0.1:5005/appointment/all";
var get_avail_doctors_URL = "http://localhost:5002/availdoctors";
var match_URL = "http://localhost:5002/match";


var app = new Vue({
    el: "#app",
    computed: {
        hasAppointments: function () {
            return this.appointments.length > 0;
        },
        doctorsAvail: function() {
            return this.availableDoctors.length > 0;
        },
    },
    data: {
        message: "There is a problem retrieving appointment data, please try again later.",
        "appointments": [],
        noDrs: "There are currently no doctors available.",
        "availableDoctors": [],
        selected: ""
    },
    methods: {
        getAllAppointments: function () {
            // on Vue instance created, load the appointment list
            const response =
                fetch(get_all_appts_URL)
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
            // converting GMT to YYYY-MM-DD format
            for (appointment in this.appointments) {
                console.log(this.appointments);
                var new_date = appointment.appointment_date;
                console.log(new_date);
                var new_time = appointment.appointment_time;
                console.log(new_time);
                var date = new Date(new_date).toISOString();
                var date = date.slice(0,10);
                var datetime = date + "+" + (new_time).toString();
                console.log(datetime);
                const response =
                    fetch(`${get_avail_doctors_URL}/${datetime}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log(response);
                            if (data.code === 404) {
                                // no doctor available in db
                                this.noDrs = data.noDrs;
                            } else {
                    
                                this.availableDoctors = data.data.available_doctors;
                                console.log(availableDoctors);
                            }
                        })
                        .catch(error => {
                            // Errors when calling the service; such as network error, 
                            // service offline, etc
                            console.log(this.message + error);

                        });

                
            }
        },
            
        },
            created: function () {
            // on Vue instance created, load the appt list
            this.getAllAppointments();
            this.getAvailDoctors();
        }
    });
    
