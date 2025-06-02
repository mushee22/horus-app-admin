let imageField = document.getElementById("ImageField");
if(imageField) {
    imageField?.addEventListener('change',(e)=>{
        var file = e.target.files[0];
        if(file){
            url = URL.createObjectURL(file);
            imageField.parentNode.querySelector(".image-box").style.backgroundImage = `url(${url})`;
        }
    });
    
    if (imageField.getAttribute("data-value")){
        imageField.parentNode.querySelector(".image-box").style.backgroundImage = `url(${imageField.getAttribute("data-value")})`;
    }
}
