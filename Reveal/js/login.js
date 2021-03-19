function patientlogin(){
    console.log("HIII")
    var title = document.getElementById("title")
    var request = new XMLHttpRequest()

    var fullName = document.getElementById("fullName").value
    var NRIC = document.getElementById("NRIC").value
    var loginDetails = "fullName="+fullName+"&NRIC="+NRIC
    var url = "../backend/patientLoginCheck.php?" + loginDetails

    request.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var result = this.responseText //string
            console.log(result)
           
            if(result=='true'){
                location.href = "patientUI.html"//tentative
                console.log("HELLO")
            } else{
                title.innerText = "fullName/NRIC is incorrect.";
                console.log("WHAT")

            }
        }
    }
    
    request.open("GET", url, true)
    request.send()
}