var get_all_URL = "http://localhost:5001/availability";

// =====================
// Vue KIV
// =====================
// var app = new Vue({
//     el: "#app",
//     data: {
//         new_appointment_date: "",
//         selected_date: "",
//         time: ['1000','1100','1200','1300','1400','1500'],
//         message: "There is a problem retrieving doctors data, please try again later.",
//         doctor_date: "",
//         doctor_time_array: []
//     },
//     methods:{
//         get_all_available_time: function(){
//             console.log("in get_all_available_time function");
//             const response =
//                 fetch(get_all_URL)
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log(response);
//                     if (data.code === 404) {
//                         // no doctors in db
//                         this.message = data.message;
//                     } else {
//                         this.doctors = data.data.doctor_availability;
//                     }
//                 })
//                 .catch(error => {
//                     // Errors when calling the service; such as network error, 
//                     // service offline, etc
//                     console.log(this.message + error);

//                 });
//         }
//     }
// })
// ================================================


//get available time by selected date
function display_available_time(){
    var selected_date = document.getElementById("selected_date").value;

    fetch("http://127.0.0.1:5001/availability/datetime/"+ selected_date)
    .then(response => response.json())
    .then(json => {
        console.log(json);
        if (json.length === 0){
            document.getElementById("no_results").innerHTML = `
            <br>
                No available time today, please choose another date.
            <br>
            `;
        } else {
            console.log("inside else function");
            console.log(json);
            //display the available time as a dropdown
            //need to see what is json first before continuing
        }
    })
}

//post new booking appointment to appointment DB
function post_new_booking(){
    console.log("inside post_new_booking function");

    var patient_name = document.getElementById("patient_fullname").value;    
    var patient_nric = document.getElementById("patient_nric").value;
    var patient_gender = getGenderValue();
    var patient_contact_number = document.getElementById("patient_contact_number").value;
    var patient_email_address = document.getElementById("patient_email").value;
    var appointment_date = document.getElementById("appointment_date").value;
    var appointment_time = document.getElementById("appointment_time").value;
    
    fetch("http://127.0.0.1:5005/appointment", { 
        method:'POST',
        headers: {
            'Accept': 'application/json',
            'Content-type':'application/json'
            },
        body:JSON.stringify({
            "patient_name" : patient_name,
            "patient_nric" : patient_nric,
            "patient_gender" : patient_gender,
            "patient_contact_number": patient_contact_number,
            "patient_email_address": patient_email_address,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time
        })
    })

    .then(response => {
        if(response.status == '200'){
            console.log((json));
            document.getElementById("booking_status").innerHTML = 'Your appointment has been booked successfully';
        }
    }
    );
}

function getGenderValue(){
    var selected = document.getElementsByName('gender');
    for(i=0; i<selected.length; i++){
        if(selected[i].checked)
            return selected[i].value;
    }
}