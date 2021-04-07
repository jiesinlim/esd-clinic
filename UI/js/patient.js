var get_all_URL_5001 = "http://localhost:5001/availability";
var get_all_URL_5005 = "http://localhost:5005/appointment";

// =====================
// Vue
// =====================
var app1 = new Vue({
    el: "#app1",
    computed: {
        hasAppointments: function(){
            return this.appointments.length >0;
        }
    },
    data: {
        "appointments": [],
        all_appointments: [],
        
        message: "There is a problem retrieving appointment data, please try again later.",
        statusMessage: "",
        appointment_id: "",
        searchStr: "",

        newFullname: "",
        newNRIC: "",
        selected_gender: null,
        newContactNumber: "",
        newEmail: "",
        newAppointmentDate: "",
        newAppointmentTime: "",
        newDid: null,
        newAid: null,
        newDoctorName: null,
        newStatus: "booked",
        newRoom_No: null,

        selected_date: "",
        all_available_time_string: "",
        all_available_time_array: [],

        appointmentAdded: false,
        addAppointmentError: "",

        searchStr: "",
        searchError: "",
        searchBar: false,

        edit: false,
        editSuccessful: false,
        editAppointmentError: "",

        editCurrentAppointment: "",
        editCurrentDate: "",
        editCurrentTime: "",

        editDate: "",
        editTime: "",

        appointment_deleted: false,
        hasAppointment: true,

        no_avail_time: false
    },
    methods:{
        getAllAppointments: function(){
            const response =
                fetch(`${get_all_URL_5005}/all`)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no appointments in db
                        this.message = data.message;
                    } else {
                        this.all_appointments = data.data.appointments;
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.message + error);

                });
        },

        get_avail_time_by_date: function(){
            // reset data
            this.all_available_time_string = "";
            this.all_available_time_array = [];
            this.no_avail_time = false;

            console.log("in get_avail_time_by_date function");
            console.log(this.newAppointmentDate, typeof(this.newAppointmentDate));

            const response =
                fetch(`${get_all_URL_5001}/datetime/${this.newAppointmentDate}`)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no available time for this selected date
                        console.log("in the 404 block");
                        this.message = data.message;
                        this.no_avail_time = true;
                        console.log(this.no_avail_time);
                    } else {
                        console.log("in else block");
                        this.all_available_time_string = data.data.available_doctors[0].availability;
                        console.log("time string",this.all_available_time_string);
                        this.all_available_time_array = this.all_available_time_string.split(',');
                        console.log("time array",this.all_available_time_array);
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log("in catch error block");
                    console.log(this.message + error);

                });
        },
        get_avail_time_by_date_for_edit_form: function(){
            // reset data
            this.all_available_time_string = "";
            this.all_available_time_array = [];
            this.no_avail_time = false;

            console.log("in get_avail_time_by_date_for_edit_form function");
            console.log(this.editDate, typeof(this.editDate));

            const response =
                fetch(`${get_all_URL_5001}/datetime/${this.editDate}`)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no available time for this selected date
                        console.log("in the 404 block");
                        this.message = data.message;
                        this.no_avail_time = true;
                        console.log(this.no_avail_time);
                    } else {
                        console.log("in else block");
                        this.all_available_time_string = data.data.available_doctors[0].availability;
                        console.log("time string",this.all_available_time_string);
                        this.all_available_time_array = this.all_available_time_string.split(',');
                        console.log("time array",this.all_available_time_array);
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log("in catch error block");
                    console.log(this.message + error);

                });
        },

        addAppointment: function(){
            //reset data to original setting
            this.appointmentAdded = false;
            this.addAppointmentError = "";
            this.statusMessage = "";
            this.appointment_deleted = false;

            let jsonData = JSON.stringify({
                NRIC: this.newNRIC,
                patient_name: this.newFullname,
                gender: this.selected_gender,
                contact_number: this.newContactNumber,
                email: this.newEmail,
                appointment_date: this.newAppointmentDate,
                appointment_time: this.newAppointmentTime,
                did: this.newDid,
                aid: this.newAid,
                doctor_name: this.newDoctorName,
                status: this.newStatus,
                room_no: this.newRoom_No,

            });
            console.log(jsonData);

            fetch(`${get_all_URL_5005}`,{
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: jsonData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                result = data.data;
                console.log(result);
                // 3 cases
                switch (data.code) {
                    case 201:
                        this.appointmentAdded = true;
                        this.statusMessage = "Your appointment has been successfully booked!"

                        // refresh page
                        this.pageRefresh();

                        break;
                    case 400:
                    case 500:
                        this.addAppointmentError = data.message;
                        this.statusMessage = "There is a problem booking this new appointment:"
                        break;
                    default:
                        throw `${data.code}: ${data.message}`;
                }
            })
        },

        findAppointmentByNRIC: function(){
            // this.searchBar = false;
            console.log("in findappointmentsbynric function");
            console.log("searchBar:", this.searchBar);
            console.log("searchStr:", this.searchStr);
            var searchStr = this.searchStr.toUpperCase();
            console.log(searchStr);

            const response =
                fetch(`${get_all_URL_5005}/nric/${searchStr}`)
                .then(response => response.json())
                    .then(data => {
                        console.log(response);
                        if (data.code === 404) {
                            // no appointment details found in db
                            this.searchError = data.message;
                            console.log("in findappointmentsbynric if block");
                        } else {
                            this.appointments = data.data.appointments;
                            console.log(this.appointments);
                            this.searchError = "";
                            this.searchBar = true;
                            console.log("in findappointmentsbynric else block");
                        }
                    })
                    .catch(error => {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        console.log(this.searchError + error);
                        console.log("in findappointmentsbynric catch error block");

                    });
            console.log("after function searchBar:", this.searchBar);
            console.log("after searchStr:", this.searchStr);
        },
        editAppointmentForm: function(appointment){
            //resets the data setting
            this.editSuccessful = false;
            this.editCurrentAppointment = appointment;
            this.edit = true;

            this.editDate ="";
            this.editTime ="";
        },
        editAppointmentDateTime: function(appointment){
            //reset data
            this.editAppointmentError = "";

            let jsonData = JSON.stringify({
                NRIC: this.editCurrentAppointment.NRIC,
                aid: this.editCurrentAppointment.aid,
                appointment_date: this.editDate, //Edited Date
                appointment_time: this.editTime, //Edited Time
                contact_number: this.editCurrentAppointment.contact_number,
                did: this.editCurrentAppointment.did,
                doctor_name: this.editCurrentAppointment.doctor_name,
                email: this.editCurrentAppointment.email,
                gender: this.editCurrentAppointment.gender,
                patient_name: this.editCurrentAppointment.patient_name,
                room_no: this.editCurrentAppointment.room_no,
                status: this.editCurrentAppointment.status
            });

            fetch(`${get_all_URL_5005}`, {
                    method: "PATCH",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: jsonData
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    result = data.data;
                    console.log(result);
                    // 3 cases
                    switch (data.code) {
                        case 200:
                            this.editSuccessful = true;

                            this.getAllAppointments();

                            this.editAppointmentError = 'Edit successfully changed';

                            break;
                        case 404:
                            this.editAppointmentError = data.message;
                        case 500:
                            this.editAppointmentError = data.message;
                            break;
                        default:
                            throw `${data.code}: ${data.message}`;
                    }
                })
        },
        delAppointmentBooked: function(appointment_id){
            //reset all data to original setting
            this.appointment_id = appointment_id;
            this.appointment_deleted = false;

            this.appointmentAdded = false;
            this.addAppointmentError= "";
            this.statusMessage = "";

            const response =
                fetch(`${get_all_URL_5005}/${this.appointment_id}`, {
                    method: "DELETE",
                })
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no appointment in db
                        this.message = data.message;
                        this.appointments = [];
                    } else {
                        this.appointment_deleted = true;
                        this.statusMessage = "The appointment booked has been successfully deleted!";
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error,
                    // service offline, etc
                    console.log(this.message + error);

                });

            // Front end Vue
            var idx = 0
            for (appointment of this.appointments) {
                if (appointment.appointment_id == appointment_id) {
                    this.appointments.splice(idx, 1) // remove this element
                    break
                }
                idx++
            }
        },
        pageRefresh: function () {
            this.getAllAppointments(); //?
            this.edit = false;
            this.searchError = "";
            this.appointment_id = "";
            this.searchStr = "";
            this.searchBar = false;
        }
    },
    created: function () {
        // on Vue instance created, load the list
        this.getAllAppointments(); //?
    }
});