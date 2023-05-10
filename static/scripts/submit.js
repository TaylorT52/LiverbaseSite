//Js all written by me

const fileForm = document.getElementById("file")
const analyzeBtn = document.getElementById("analyzeBtn")
const popup = document.getElementsByClassName("popup")[0]

//To display image after selecting
fileForm.addEventListener("input", function(){
    var inputVal = fileForm.files[0]

    if(inputVal != ""){
        var reader  = new FileReader();
        reader.onload = function(e)  {
            document.getElementById("replaceimg").src = e.target.result;
         }
       reader.readAsDataURL(inputVal); 
    }
})

//Popup while submission running
analyzeBtn.addEventListener("click", function(){
    popup.classList.replace("hide-popup", "show-popup")
})

function closeFlash(){
    const element = document.getElementsByClassName("alert")[0]
    element.remove();
}
