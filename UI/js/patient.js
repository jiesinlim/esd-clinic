var get_all_URL = "http://localhost:5001/availability";

var app = new Vue({
    el: "#app",
    data: {
        new_appointment_date: "",
        selected_date: "",
        time: ['1000','1100','1200','1300','1400','1500'],
        message: "There is a problem retrieving doctors data, please try again later.",
        doctor_date: "",
        doctor_time_array: []
    },
    methods:{
        get_all_available_time: function(){
            console.log("in get_all_available_time function");
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
        
        }
    }
})