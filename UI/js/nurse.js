//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_booked_appts_URL = "http://127.0.0.1:5005/appointment/booked";
var get_avail_doctors_URL = "http://localhost:5002/availdoctors";
var match_URL = "http://localhost:5002/match";


var app = new Vue({
    el: "#app",
    computed: {
        hasAppointments: function () {
            return this.appointments.length > 0;
        },
        doctorsAvail: function() {
            return this.available_doctors.length > 0;
        },
    },
    data: {
        message: "There is a problem retrieving appointment data, please try again later.",
        "appointments": [],
        noDrs: "There are currently no doctors available.",
        "available_doctors": [],
        selected: "",
        "datetime": []
    },
    methods: {
        getBookedAppointments: function () {
            // on Vue instance created, load the appointment list
            const response =
                fetch(get_booked_appts_URL)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            
                            this.appointments = data.data.appointments;
                            console.log(this.appointments);
                            for (var patient of this.appointments) {
                                var date = new Date(patient.appointment_date).toISOString();
                                date = date.slice(0,10);
                                dateTime = date + "+" + patient.appointment_time;

                                this.datetime.push(dateTime);
                            }
                            console.log(this.datetime);
                            this.getAvailDoctors();
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
            if (this.datetime.length > 0) {
                for (var i=0; i<(this.appointments).length; i++) {
                    // console.log("hello");
                    console.log((this.datetime)[i]);
                    const response =
                        fetch(`${get_avail_doctors_URL}/${this.datetime[i]}`)
                            .then(response => response.json())
                            .then(data => {
                                console.log(response);
                                if (data.code === 404) {
                                    // no doctor available in db
                                    this.noDrs = data.noDrs;
                                } else {
                                    var patient_availdoc = [];
                                    for (var doctor of data.data.available_doctors) {
                                        patient_availdoc.push(doctor);  // [Dr Marcus, Dr Hong Seng]
                                    }
                                    this.available_doctors.push(patient_availdoc);
                                    console.log(patient_availdoc);
            
                                }
                            })
                            .catch(error => {
                                // Errors when calling the service; such as network error, 
                                // service offline, etc
                                console.log(this.noDrs + error);

                            });
            
                }
                console.log(this.available_doctors);  // [[Dr Marcus, Dr Hong Seng],[Dr Alan, Dr Marcus]]
            }
        },
        deleteDrAvail: function() {
            const response =
                fetch(match_URL)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            
                            this.appointments = data.data.appointments;
                            console.log(this.appointments);
                            for (var patient of this.appointments) {
                                var date = new Date(patient.appointment_date).toISOString();
                                date = date.slice(0,10);
                                dateTime = date + "+" + patient.appointment_time;

                                this.datetime.push(dateTime);
                            }
                            console.log(this.datetime);
                            this.getAvailDoctors();
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
    
