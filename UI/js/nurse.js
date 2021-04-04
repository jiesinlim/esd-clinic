//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_booked_appts_URL = "http://127.0.0.1:5005/appointment/all/booked";
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
        "datetime": [],
        "date": [],
        showModal: false,
        modalTitle: "Appointment has been successfully matched!",
        'selectedAppt': []
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
                            
                            // console.log(this.appointments);
                            for (var patient of this.appointments) {
                                this.date.push(new Date(patient.appointment_date).toDateString());

                                var date = new Date(patient.appointment_date).toISOString();
                                date = date.slice(0,10);
                                dateTime = date + "+" + patient.appointment_time;

                                this.datetime.push(dateTime);
                            }
                            // console.log(this.datetime);
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
                    // console.log((this.datetime)[i]);
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
                                    // console.log(patient_availdoc);
            
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
        successfulMatch: function(appt_index) {
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
            else {
                console.log("Select a doctor first before matching!");
            }
        },
        updateMatchDetails: function () {
            this.showModal = false;
            //reload page
            console.log("details successfully updated!");
            this.getBookedAppointments();
            location.reload();
        },
    },
            created: function () {
            // on Vue instance created, load the appt list
            this.getBookedAppointments();
        }
    });

