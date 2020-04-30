checkAge()
                        
function setAge(value){
    window.localStorage.setItem("AgeOkay", value==1 ? true : false)
    checkAge()
}

function checkAge(){

    let AgeOkay = window.localStorage.getItem("AgeOkay")
    let ageGate = document.getElementById("age-gate")
    // let content = document.getElementById("content")
    let body = document.getElementById("body")
    let reject = document.getElementById("reject")
    let ask = document.getElementById("ask")

    if(AgeOkay=="true"){                
        ageGate.style.display = "none"
        body.style.display = "block"
    }
    else if(AgeOkay==null){
        ageGate.style.display = "block"
        body.style.display = "none"
    }
    else{
        ageGate.style.display = "block"
        ask.style.display = "none"
        body.style.display = "none"
        reject.style.display = "block"
    }

}