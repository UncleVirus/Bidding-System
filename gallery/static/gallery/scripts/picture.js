// function uploadPhoto() {
//     var fileInput = document.getElementById("photoUpload");
//     var file = fileInput.files[0];
    
//     var photoContainer = document.getElementById("photoContainer");
    
//     if (file) {
//       var reader = new FileReader();
      
//       reader.onload = function(e) {
//         var img = document.createElement("img");
//         img.src = e.target.result;
//         photoContainer.appendChild(img);
//       }
      
//       reader.readAsDataURL(file);
//     }
//   }