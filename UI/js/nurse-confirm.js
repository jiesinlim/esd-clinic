//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_matched_appts_URL = "http://127.0.0.1:5006/confirm";
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
        index: 0,
        showModal: false,
        modalTitle: "Appointment has been successfully confirmed!",
        "date": []
    },
    methods: {
        getMatchedAppointments: function () {
            // on Vue instance created, load the appointment list

            // var tomorrow = new Date();
            // tomorrow.setDate(day.getDate() + 1);
            // tomorrow = tomorrow.toISOString().slice(0,10);

            var tomorrow = "2021-03-21";  // dummy variable for testing
            console.log(tomorrow);
            const response =
                fetch(`${get_matched_appts_URL}/${tomorrow}`)
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
        },
        updateConfirmDetails: function (index) {
            console.log(index);
            this.index = index;
            // this.confirm.patient_name = this.appointments[index].patient_name;
            // this.confirm.doctor_name = this.appointments[index].doctor_name;
            // this.confirm.appointment_date = this.date[index];
            // this.confirm.appointment_time = this.appointments[index].appointment_time;

            // this.confirm.email = this.appointments[index].email;
            // this.confirm.appointment_id = this.appointments[index].appointment_id;

            this.showModal = true;

            let jsonData = JSON.stringify(
                {
                    patient_name: this.appointments[index].patient_name,
                    email: this.appointments[index].email,
                    appointment_id: this.appointments[index].appointment_id,
                    appointment_time: this.appointments[index].appointment_time
                }
            )
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
                            
                            console.log("notification successfully sent to patient!");
                        }
                    })
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.message + error);
                    });
        },
        closeModal: function () {
            this.showModal = false;
            //reload page
            location.reload();  // page does not reload after modal closes -- find out why
        }
    },
            created: function () {
            // on Vue instance created, load the appt list
            this.getMatchedAppointments();
        }
    });

