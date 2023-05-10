const del_button = document.querySelectorAll("[id^='delete-btn-']")
const popup = document.getElementsByClassName("popup")[0]

del_button.forEach(button => {
    button.addEventListener("click", function(event){
        const submissionId = event.target.getAttribute("subId"); 
        deleteEntry(submissionId)
    })
})

function deleteEntry(entryId){
    console.log(popup.style)
    fetch("/savedslides/" + entryId, {
        method: "DELETE"
    })
    .then(response =>{
        if(response.ok){
            popup.classList.replace("hide-popup", "show-popup")
            setInterval(closePopup, 2000)
            console.log(popup.classList)
        }else{
            alert("Error deleting entry :(")
        }
    })
}

function closePopup(){
    popup.classList.replace("show-popup", "hide-popup")
    location.reload()
}
