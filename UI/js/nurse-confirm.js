//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_matched_appts_URL = "http://127.0.0.1:5005/appointment/status/matched";
// var get_avail_doctors_URL = "http://localhost:5002/availdoctors";
// var match_URL = "http://localhost:5002/match";


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
        // "available_doctors": [],
        // selected: "",
        "datetime": [],
        "date": [],
        showModal: false,
        modalTitle: "Appointment has been successfully confirmed!"
        // 'selectedAppt': []
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

        successfulConfirmation: function(appt_index) {
            console.log(appt_index);
            if (this.selected != "" && Number.isInteger(appt_index)) {
                this.showModal = true;
                this.selectedAppt.push(this.appointments[appt_index].NRIC);
                this.selectedAppt.push(this.date[appt_index]);
                this.selectedAppt.push(this.appointments[appt_index].appointment_time);

                //invoke match microservice (requires avail_id, did, doc_name, appt_id, appt_time, doc_avail)
                for (var doctor of this.available_doctors[appt_index]) {
                    if (doctor.doctor_name == this.selected) {
                        this.selectedAppt.push(doctor.availability);
                        this.selectedAppt.push(doctor.aid);
                        this.selectedAppt.push(doctor.did);
                        this.selectedAppt.push(this.selected);
                        this.selectedAppt.push(appt_index);
                    }
                }                
            } 
        },
        updateConfirmDetails: function () {
            this.showModal = false;
            
            //reload page
            location.reload();
            console.log("notification successfully sent to patient!");
        },
    },
            created: function () {
            // on Vue instance created, load the appt list
            this.getMatchedAppointments();
        }
    });

