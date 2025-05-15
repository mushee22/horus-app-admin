const showValidationError = (element,msg)=>{
    let parent = element.closest('.mb-3');
    let errorMessages = document.querySelectorAll(".valid-error-message");
    errorMessages.forEach(emsg => {
        emsg.remove()
    });
    let errorMessage = document.createElement('span');
    errorMessage.textContent = msg;
    errorMessage.classList.add("valid-error-message");
    errorMessage.style.cssText = 'color:red;font-size:12px;';
    parent.insertBefore(errorMessage,element);
}

const mobileRegex = /^\d*$/;

const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

const alphabetRegex = /^[A-Za-z\W]+$/;
