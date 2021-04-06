//var get_all_URL = "http://localhost:8000/api/v1/doctor";
// var get_all_URL = "http://localhost:5001/match";
var get_booked_appts_URL = "http://127.0.0.1:5005/appointment/status/booked";
var get_avail_doctors_URL = "http://127.0.0.1:5002/availdoctors";
var match_URL = "http://127.0.0.1:5002/match";


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
        'selectedAppt': {}
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
                for (let i=0; i<(this.appointments).length; i++) {
                    // console.log((this.datetime)[i]);
                    const response =
                        fetch(`${get_avail_doctors_URL}/${this.datetime[i]}`)
                            .then(response => response.json())
                            .then(data => {
                                console.log(response);
                                if (data.code === 404) {
                                    // no doctor available in db
                                    this.noDrs = data.noDrs;
                                    this.appointments[i].avail_doctors = [];

                                } else {
                                    var patient_availdoc = [];
                                    for (var doctor of data.data.available_doctors) {
                                        patient_availdoc.push(doctor);  // [Dr Marcus, Dr Hong Seng]
                                    }
                                    // console.log(patient_availdoc);
                                    this.available_doctors.push(patient_availdoc);
                                    this.appointments[i].avail_doctors = patient_availdoc;
                                }
                            })
                            .catch(error => {
                                // Errors when calling the service; such as network error, 
                                // service offline, etc
                                console.log(this.noDrs + error);
                            });
                }
            }
            // console.log(this.available_doctors); //[[Dr Marcus, Dr Hong Seng],[Dr Alan, Dr Marcus]]
            console.log(this.appointments); 
        },
        selectDoctor: function(appt_index) {
            console.log(appt_index);
            if (this.selected != "" && Number.isInteger(appt_index)) {

                this.selectedAppt.p_name = this.appointments[appt_index].patient_name;
                this.selectedAppt.date = this.date[appt_index];
                this.selectedAppt.time = this.appointments[appt_index].appointment_time;
                this.selectedAppt.appt_id = this.appointments[appt_index].appointment_id;
                this.selectedAppt.d_name = this.selected;

                //invoke match microservice (requires avail_id, did, doc_name, appt_id, appt_time, doc_avail)
                
                // [{doctor_name: paul,did: 2},{doctor_name: paul,did: 2},{doctor_name: paul,did: 2}]
                // for loop part not working? sometimes
                // for (var doctor of this.available_doctors[appt_index]) {
                //     if (doctor.doctor_name == this.selected) {
                //         this.selectedAppt.availslots = doctor.availability;
                //         this.selectedAppt.avail_id = doctor.aid;
                //         this.selectedAppt.did = doctor.did;
                //     }
                // } 
                if (this.available_doctors[appt_index].length > 1) {
                    var doc_idx = this.available_doctors[appt_index].findIndex(x => x.doctor_name === this.selected);
                    console.log("more than 1 doctor available");
                } else {
                    doc_idx = 0;
                    console.log("only 1 doctor available");
                }

                console.log(doc_idx);
                this.selectedAppt.availslots = this.available_doctors[appt_index][doc_idx].availability;
                this.selectedAppt.avail_id = this.available_doctors[appt_index][doc_idx].aid;
                this.selectedAppt.did = this.available_doctors[appt_index][doc_idx].did;
            } 
        },
        successfulMatch: function () {
            if ("d_name" in this.selectedAppt) {
                let jsonData = JSON.stringify(
                    {
                        appointment_id: this.selectedAppt.appt_id,
                        aid: this.selectedAppt.avail_id,
                        did: this.selectedAppt.did,
                        d_name: this.selectedAppt.d_name,
                        appt_time: this.selectedAppt.time,
                        doc_avail: this.selectedAppt.availslots
                    }
                )
                console.log(jsonData);

                const response =
                fetch(match_URL, {
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
                        this.showModal = true;
                        console.log("patient and doctor successfully matched!");
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.message + error);
                });
                
            } else {
                console.log("Select a doctor first before matching!");
            }
        },
        updateMatchDetails: function () {
            this.showModal = false;

            //reload page
            location.reload();
            console.log("details successfully updated!");
        },
    },
    mounted: function () {
        // on Vue instance created, load the appt list
        this.getBookedAppointments();
    }
});
