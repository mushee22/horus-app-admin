document.addEventListener("DOMContentLoaded", function () {
    initializeForm({
        formId: "contactForm",
        submitBtnId: "submitBtn",
        errorMsgId: "errorMessage",
        countryDropdownId: "popupCountryDropdown",
        dropBtnSelector: "#contactForm .dropbtn",
        selectedFlagId: "selectedFlag",
        selectedCodeId: "selectedCode",
        selectedCountryIdId: "selectedCountryId",
        parentPopupId: "lets-connect-popup",
        isPopupForm: true
    });

    initializeForm({
        formId: "footerContactForm",
        submitBtnId: "footerSubmitBtn",
        errorMsgId: "footerErrorMessage",
        countryDropdownId: "footerCountryDropdown",
        dropBtnSelector: "#footerDropBtn",
        selectedFlagId: "footerSelectedFlag",
        selectedCodeId: "footerSelectedCode",
        selectedCountryIdId: "footerSelectedCountryId",
        isFooter: true
    });

    fetchCountries();

    initializeTryItNowButtons();

    function initializeForm(config) {
        const form = document.getElementById(config.formId);
        const submitBtn = document.getElementById(config.submitBtnId);
        const errorMessage = document.getElementById(config.errorMsgId);
        const dropBtn = document.querySelector(config.dropBtnSelector);
        const countryDropdown = document.getElementById(config.countryDropdownId);

        if (!form) return;

        if (dropBtn && countryDropdown) {
            dropBtn.addEventListener("click", function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (config.isFooter) {
                    dropBtn.parentElement.classList.toggle("show");
                } else {
                    countryDropdown.style.display = countryDropdown.style.display === "block" ? "none" : "block";
                }
            });
        }

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            if (submitBtn.disabled) return;
            
            if (errorMessage) errorMessage.style.display = "none";

            if (!validateForm(form, errorMessage)) return;

            submitBtn.disabled = true;
            submitBtn.textContent = "Sending...";

            const formData = new FormData(form);
            const jsonData = {};
            formData.forEach((value, key) => {
                jsonData[key] = value;
            });

            const countryIdField = document.getElementById(config.selectedCountryIdId);
            if (!jsonData.country_id && countryIdField) {
                jsonData.country_id = countryIdField.value;
            }

            submitFormData(jsonData, form, submitBtn, errorMessage, config);
        });
    }

    function validateForm(form, errorMessage) {
        const requiredFields = ['first_name', 'last_name', 'email', 'message', 'phone'];
        let isValid = true;

        requiredFields.forEach(field => {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error-field');
                } else {
                    input.classList.remove('error-field');
                }
            }
        });

        if (!isValid && errorMessage) {
            errorMessage.textContent = "Please fill in all required fields";
            errorMessage.style.display = "block";
        }

        return isValid;
    }

    function submitFormData(jsonData, form, submitBtn, errorMessage, config) {
        fetch("/api/contact/submit/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify(jsonData),
            credentials: 'include',
        })
        .then(response => response.json().catch(() => {
            throw new Error(`Server responded with status: ${response.status}`);
        }))
        .then(data => {
            if (data.status === "success") {
                // Show success popup based on form type
                if (typeof window.showSuccessPopup === 'function') {
                    if (config.isPopupForm) {
                        // For Let's Connect form (popup form)
                        window.showSuccessPopup({
                            popupId: "successPopup",
                            closePopupId: config.parentPopupId,
                            autoHide: true,
                            delay: 3000
                        });
                    } else if (config.isFooter) {
                        // For Footer form
                        window.showSuccessPopup({
                            popupId: "successPopup",
                            closePopupId: null,
                            autoHide: true,
                            delay: 3000
                        });
                    } else {
                        // Default case for other forms
                        window.showSuccessPopup({
                            popupId: "successPopup",
                            autoHide: true,
                            delay: 3000
                        });
                    }
                } else {
                    console.error("showSuccessPopup function not found! Make sure successPopup.js is loaded.");
                }
                
                form.reset();
                resetCountrySelection(config);
            } else {
                if (errorMessage) {
                    errorMessage.textContent = data.message || "Error submitting form";
                    errorMessage.style.display = "block";
                }
            }
        })
        .catch(error => {
            console.error("Submission error:", error);
            if (errorMessage) {
                errorMessage.textContent = "An error occurred. Please try again.";
                errorMessage.style.display = "block";
            }
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = "Send Message";
        });
    }


    function resetCountrySelection(config) {
        const selectedIds = [
            config.selectedFlagId, 
            config.selectedCodeId, 
            config.selectedCountryIdId
        ];
        
        selectedIds.forEach(id => {
            const element = document.getElementById(id);
            if (element && element.tagName === "INPUT") 
                element.value = "";
            else if (element)
                element.textContent = "";
        });
    }

    function getCSRFToken() {
        const cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            const [name, value] = cookie.split("=");
            if (name === "csrftoken") return value;
        }
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfInput ? csrfInput.value : "";
    }


    function initializeTryItNowButtons() {
        const emailInput = document.querySelector(".email-container input");
        const tryItNowButtons = document.querySelectorAll(".open-letsconnect");
        const popupEmailInput = document.querySelector("#lets-connect-popup input[name='email']");
    
        tryItNowButtons.forEach(button => {
            button.addEventListener("click", function (e) {
                // Check if email exists in the input field
                const enteredEmail = emailInput.value.trim();
                
                if (enteredEmail !== "" && popupEmailInput) {
                    // If email exists and popup email field is found, pre-fill it
                    popupEmailInput.value = enteredEmail;
                }
                // The popup will show regardless of whether email exists or not
            });
        });
    }



    function fetchCountries() {
        fetch('/api/countries/')
            .then(response => response.json())
            .then(data => {
                initializeCountryDropdown({
                    dropdownId: "popupCountryDropdown",
                    selectedFlagId: "selectedFlag",
                    selectedCodeId: "selectedCode",
                    selectedCountryIdId: "selectedCountryId",
                    isPopupForm: true
                }, data.countries);

                initializeCountryDropdown({
                    dropdownId: "footerCountryDropdown",
                    selectedFlagId: "footerSelectedFlag",
                    selectedCodeId: "footerSelectedCode",
                    selectedCountryIdId: "footerSelectedCountryId",
                    isFooter: true
                }, data.countries);
            })
            .catch(error => console.error("Error fetching countries:", error));
    }

    function initializeCountryDropdown(config, countries) {
        const dropdown = document.getElementById(config.dropdownId);
        if (!dropdown) return;

        dropdown.innerHTML = "";

        const selectedFlag = document.getElementById(config.selectedFlagId);
        const selectedCode = document.getElementById(config.selectedCodeId);
        const selectedCountryId = document.getElementById(config.selectedCountryIdId);

        let defaultCountry = countries.find(c => c.code === "+91" || c.name.toLowerCase() === "india");
        if (!defaultCountry && countries.length > 0) {
            defaultCountry = countries[0];
        }

        if (defaultCountry) {
            if (selectedFlag) selectedFlag.src = defaultCountry.flag;
            if (selectedCode) selectedCode.textContent = defaultCountry.code;
            if (selectedCountryId) selectedCountryId.value = defaultCountry.id;
        }

        countries.forEach(country => {
            const countryItem = document.createElement("div");
            countryItem.classList.add("country-item");
            countryItem.innerHTML = `
                <img src="${country.flag}" class="flag-img">
                <span>${country.code} ${country.name}</span>
            `;
            
            countryItem.onclick = function () {
                if (selectedFlag) selectedFlag.src = country.flag;
                if (selectedCode) selectedCode.textContent = country.code;
                if (selectedCountryId) selectedCountryId.value = country.id;

                if (config.isFooter) {
                    const footerDropBtn = document.getElementById("footerDropBtn");
                    if (footerDropBtn) footerDropBtn.parentElement.classList.remove("show");
                } else {
                    dropdown.style.display = "none";
                }
            };
            
            dropdown.appendChild(countryItem);
        });

        if (config.isPopupForm) {
            dropdown.style.display = "none";
        }
    }

    document.addEventListener("click", function(e) {
        const popupDropdown = document.getElementById("popupCountryDropdown");
        if (popupDropdown && !e.target.closest('#contactForm .dropdown')) {
            popupDropdown.style.display = "none";
        }
        
        const footerDropdown = document.getElementById("footerCountryDropdown");
        const footerDropBtn = document.getElementById("footerDropBtn");
        if (footerDropdown && footerDropBtn && !e.target.closest('.dropdown') && footerDropBtn.parentElement.classList.contains("show")) {
            footerDropBtn.parentElement.classList.remove("show");
        }
    });
});