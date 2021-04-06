//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_matched_appts_URL = "http://127.0.0.1:5005/appointment/status/matched";
// var get_avail_doctors_URL = "http://localhost:5002/availdoctors";
// var match_URL = "http://localhost:5002/match";

var confirmAppts_URL = "http://127.0.0.1:5006/confirm/confirmAppts";

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
        showModal: false,
        modalTitle: "Appointment has been successfully confirmed!",
        'confirm': {}
    },
    methods: {
        getMatchedAppointments: function () {
            // on Vue instance created, load the appointment list
            const response =
                fetch(get_matched_appts_URL)
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            this.appointments = data.data.appointments;
                            }
                      
                    })
                    
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.message + error);

                    });
        },
        updateConfirmDetails: function (index) {
            console.log(index);
            this.confirm.patient_name = this.appointments[index].patient_name;
            this.confirm.doctor_name = this.appointments[index].doctor_name;
            this.confirm.appointment_date = this.appointments[index].appointment_date;
            this.confirm.appointment_time = this.appointments[index].appointment_time;

            this.confirm.email = this.appointments[index].email;
            this.confirm.appointment_id = this.appointments[index].appointment_id;

            // let jsonData = JSON.stringify(
            //     {
            //         patient_name: this.confirm.patient_name,
            //         email: this.confirm.email,
            //         appointment_id: this.confirm.appointment_id,
            //         appointment_time: this.confirm.appointment_time
            //     }
            // )
            const response =
           
                fetch(`${confirmAppts_URL}`, {
                    method: "PATCH",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: jsonData
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment in db
                            this.message = data.message;
                        } else {
                            //reload page
                           
                            location.reload();
                            console.log("notification successfully sent to patient!");
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
            this.getMatchedAppointments();
        }
    });

