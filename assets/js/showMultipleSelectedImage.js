let imageFields = document.querySelectorAll(".ImageField");

imageFields.forEach(imageField => {
    
    const imageBox = imageField.parentNode.querySelector(".image-box");

    if (imageField.getAttribute("data-value")) {
        imageBox.style.backgroundImage = `url(${imageField.getAttribute("data-value")})`;
    }
    imageField.addEventListener('change', (e) => {

        const file = e.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            imageBox.style.backgroundImage = `url(${url})`;
        }
    });
});
