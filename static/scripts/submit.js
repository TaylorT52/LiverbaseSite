const fileForm = document.getElementById("file")

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

