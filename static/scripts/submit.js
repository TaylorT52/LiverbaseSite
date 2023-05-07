function submitfile(){
    console.log("file upload")
}

function retImage(arr){
    console.log("hello")
    document.getElementById("ItemPreview").src = "data:image/png;base64," + arr;
}