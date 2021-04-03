//var get_all_URL = "http://localhost:8000/api/v1/doctor";
var get_all_URL = "http://localhost:5001/availability";

var app = new Vue({
    el: "#app",
    computed: {
        hasDoctors: function () {
            return this.doctors.length > 0;
        }
    },
    data: {
        aid: "",
        datetime: "",
        "doctors": [],
        message: "There is a problem retrieving doctors data, please try again later.",
        statusMessage: "",

        searchError: "",

        newAid: "",
        newDid: "",
        newName: "",
        newDate: "",
        newAvailability: "",
        doctorAdded: false,
        addDoctorError: "",
        
        availDeleted: false,

        edit: false,
        editCurrentDoctor: "",
        editSuccessful: false,
        editDoctorError: "",
        editAid: "",
        editDid: "",
        editName: "",
        editDate: "",
        editAvailability: "",
        editDoctorError: "",
    },
    methods: {
        getAllDoctors: function () {
            // on Vue instance created, load the book list
            const response =
                fetch(get_all_URL)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no doctors in db
                        this.message = data.message;
                    } else {
                        this.doctors = data.data.doctor_availability;
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.message + error);

                });

        },
        findDoctor: function () {
            console.log(this.aid);
            const response =
                fetch(`${get_all_URL}/${this.aid}`)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no doctor found in db
                        this.searchError = data.message;
                    } else {
                        this.doctors = [data.data];
                        this.searchError = "";
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.searchError + error);

                });

        },
        findByDateTime: function () {
            const response =
                fetch(`${get_all_URL}/datetime/${this.datetime}`)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no doctor found in db
                        this.searchError = data.message;
                    } else {
                        this.doctors = data.data.available_doctors;
                        console.log(this.doctors)
                        this.searchError = "";
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.searchError + error);

                });

        },
        addDoctor: function () {
            // reset data to original setting
            this.doctorAdded = false;
            this.addDoctorError = "";
            this.statusMessage = "";
            this.availDeleted = false;

            let jsonData = JSON.stringify({
                aid: this.newAid,
                did: this.newDid,
                name: this.newName,
                date: this.newDate,
                availability: this.newAvailability
            });

            fetch(`${get_all_URL}`, {
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
                            this.doctorAdded = true;
                            this.statusMessage = "The doctor availability has been successfully added!"

                            // refresh page
                            this.pageRefresh();

                            break;
                        case 400:
                        case 500:
                            this.addDoctorError = data.message;
                            this.statusMessage = "There is a problem adding this new availability:"
                            break;
                        default:
                            throw `${data.code}: ${data.message}`;
                    }
                })
        },
        editDoctorForm: function (doctor) {
            //resets the data setting
            this.editSuccessful = false
            this.editCurrentDoctor = doctor;
            this.edit = true;

            this.editAid = ""
            this.editDid = ""
            this.editName = ""
            this.editDate = ""
            this.editAvailability = ""
        },
        editDoctor: function (doctor) {
            // reset data

            this.editDoctorError = "";

            let jsonData = JSON.stringify({
                aid: this.editCurrentDoctor.aid,
                did: this.editDid,
                name: this.editName,
                date: this.editDate,
                availability: this.editAvailability
            });

            fetch(`${get_all_URL}`, {
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

                            this.getAllDoctors();

                            this.editDoctorError = 'Edit successfully changed';

                            break;
                        case 404:
                            this.editDoctorError = data.message;
                        case 500:
                            this.editDoctorError = data.message;
                            break;
                        default:
                            throw `${data.code}: ${data.message}`;
                    }
                })
        },
        del: function (aid) {
            //reset all data to original setting
            this.aid = aid;
            this.availDeleted = false;
            
            this.doctorAdded = false;
            this.addDoctorError = "";
            this.statusMessage = "";

            const response =
                fetch(`${get_all_URL}/${this.aid}`, {
                    method: "DELETE",
                })
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                    if (data.code === 404) {
                        // no book in db
                        this.message = data.message;
                        this.doctors = [];
                    } else {
                        this.availDeleted = true;
                        this.statusMessage = "The doctor availability has been successfully deleted!";
                    }
                })
                .catch(error => {
                    // Errors when calling the service; such as network error,
                    // service offline, etc
                    console.log(this.message + error);

                });

            //Front end Vue
            var idx = 0
            for (doctor of this.doctors) {
                if (doctor.aid == aid) {
                    this.doctors.splice(idx, 1) // remove this element
                    break
                }
                idx++
            }
        },
        pageRefresh: function () {
            this.getAllDoctors();
            this.edit = false;
            this.searchError = "";
            this.aid = "";
            this.datetime = "";
        }
    },
    created: function () {
        // on Vue instance created, load the book list
        this.getAllDoctors();
    }
});