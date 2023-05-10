const fileForm = document.getElementById("file")

console.log(fileForm)

fileForm.addEventListener("input", function(){
    var inputVal = fileForm.files[0]

    if(inputVal != ""){
        document.getElementById("file-container").style.display = "None";
        document.getElementById("input-container").style.display = "block";
        var reader  = new FileReader();
        reader.onload = function(e)  {
            var image = document.createElement("img");
            image.src = e.target.result;
            document.getElementById("input-container").appendChild(image);
            image.id = "sub-img"
         }
       reader.readAsDataURL(inputVal); 
    }
})

