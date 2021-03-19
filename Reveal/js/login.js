function patientlogin(){
    var title = document.getElementById("title")
    var request = new XMLHttpRequest()

    var Name = document.getElementById("Name").value
    var NRIC = document.getElementById("NRIC").value
    var loginDetails = "Name="+Name+"&NRIC="+NRIC
    var url = "../backend/patientLoginCheck.php?" + loginDetails
    console.log(loginDetails)

    request.onreadystatechange = function(){
        console.log(this.status)
        console.log(this.readyState)

        if(this.readyState == 4 && this.status == 200){
            var result = this.responseText //string
            console.log("jshduwibybc")
           
            if(result=='true'){
                location.href = "patientUI.html"//tentative
                console.log("HELLO")
            } else{
                title.innerText = "Name/NRIC is incorrect.";
                console.log("WHAT")

            }
        }
    }
    
    request.open("GET", url, true)
    request.send()
}