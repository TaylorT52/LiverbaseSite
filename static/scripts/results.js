const del_button = document.querySelectorAll("[id^='delete-btn-']")

del_button.forEach(button => {
    button.addEventListener("click", function(event){
        const submissionId = event.target.getAttribute("subId"); 
        deleteEntry(submissionId)
    })
})

function deleteEntry(entryId){
    console.log('hello!')
    fetch("/savedslides/" + entryId, {
        method: "DELETE"
    })
    .then(response =>{
        location.reload()
        if(response.ok){
            alert("Your entry has been deleted!")
        }else{
            alert("Error deleting entry :(")
        }
    })
}