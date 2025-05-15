// document.addEventListener("DOMContentLoaded", function () {
//     const contactForm = document.getElementById("contactForm");
//     const submitBtn = document.getElementById("submitBtn");
//     const successMessage = document.getElementById("successMessage");
//     const errorMessage = document.getElementById("errorMessage");
//     const popupDropdownBtn = document.querySelector("#contactForm .dropbtn");
//     const popupCountryDropdown = document.getElementById("popupCountryDropdown");
//     const successPopup = document.getElementById("successPopup");
//     const letsConnectPopup = document.getElementById("lets-connect-popup");

//     if (popupDropdownBtn && popupCountryDropdown) {
//         popupDropdownBtn.addEventListener("click", function(e) {
//             e.preventDefault();
//             e.stopPropagation();
//             popupCountryDropdown.style.display = popupCountryDropdown.style.display === "block" ? "none" : "block";
//         });

//         document.addEventListener("click", function(e) {
//             if (!e.target.closest('#contactForm .dropdown')) {
//                 popupCountryDropdown.style.display = "none";
//             }
//         });
//     }

//     function showSuccessPopupAndCloseLetsConnect() {
//         if (successPopup) {
//             successPopup.classList.add("active");
            
//             // Auto-hide the success popup and close lets-connect popup after 3 seconds
//             setTimeout(function() {
//                 successPopup.classList.remove("active");
                
//                 if (letsConnectPopup) {
//                     letsConnectPopup.classList.remove("active");
//                     letsConnectPopup.style.display = "none";
//                 }
//             }, 3000);
//         }
//     }

//     if (contactForm) {
//         contactForm.addEventListener("submit", function (event) {
//             event.preventDefault();

//             if (submitBtn.disabled) {
//                 return;
//             }

//             if (successMessage) successMessage.style.display = "none";
//             if (errorMessage) errorMessage.style.display = "none";

//             const requiredFields = ['first_name', 'last_name', 'email', 'message', 'phone'];
//             let isValid = true;

//             requiredFields.forEach(field => {
//                 const input = contactForm.querySelector(`[name="${field}"]`); 
//                 if (input) {
//                     if (!input.value.trim()) {
//                         isValid = false;
//                         input.classList.add('error-field');
//                     } else {
//                         input.classList.remove('error-field');
//                     }
//                 }
//             });

//             if (!isValid) {
//                 if (errorMessage) {
//                     errorMessage.textContent = "Please fill in all required fields";
//                     errorMessage.style.display = "block";
//                 }
//                 return;
//             }

//             submitBtn.disabled = true;
//             submitBtn.textContent = "Sending...";

//             const formData = new FormData(contactForm);
//             const jsonData = {};
//             formData.forEach((value, key) => {
//                 jsonData[key] = value;
//             });

//             if (!jsonData.country_id && document.getElementById('selectedCountryId')) {
//                 jsonData.country_id = document.getElementById('selectedCountryId').value;
//             }

//             fetch("/api/contact/submit/", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": getCSRFToken(),
//                 },
//                 body: JSON.stringify(jsonData),
//                 credentials: 'include',
//             })
//                 .then(response => response.json().catch(() => {
//                     throw new Error(`Server responded with status: ${response.status}`); 
//                 }))
//                 .then(data => {
//                     if (data.status === "success") {
//                         // Show success popup and close lets-connect popup after delay
//                         showSuccessPopupAndCloseLetsConnect();
                        
//                         if (successMessage) successMessage.style.display = "none";
//                         if (errorMessage) errorMessage.style.display = "none";
//                         contactForm.reset();

//                         ["selectedFlag", "selectedCode", "selectedCountryId"].forEach(id => {
//                             const element = document.getElementById(id);
//                             if (element && element.tagName === "INPUT") 
//                                 element.value = "";
//                             else if (element)
//                                 element.textContent = "";
//                         });
//                     } else {
//                         if (errorMessage) {
//                             errorMessage.textContent = data.message || "Error submitting form";
//                             errorMessage.style.display = "block";
//                         }
//                     }
//                 })
//                 .catch(error => {
//                     console.error("Submission error:", error);
//                     if (errorMessage) {
//                         errorMessage.textContent = "An error occurred. Please try again.";
//                         errorMessage.style.display = "block";
//                     }
//                 })
//                 .finally(() => {
//                     submitBtn.disabled = false;
//                     submitBtn.textContent = "Send Message";
//                 });
//         });
//     }

//     function getCSRFToken() {
//         const cookies = document.cookie.split("; ");
//         for (let cookie of cookies) {
//             const [name, value] = cookie.split("=");
//             if (name === "csrftoken") return value;
//         }
//         const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
//         return csrfInput ? csrfInput.value : "";
//     }

//     const emailInput = document.querySelector(".email-container input");
//     const tryItNowButtons = document.querySelectorAll(".open-letsconnect");
//     const popupEmailInput = document.querySelector("#lets-connect-popup input[name='email']");

//     tryItNowButtons.forEach(button => {
//         button.addEventListener("click", function () {
//             if (emailInput && emailInput.value.trim() !== "") {
//                 sessionStorage.setItem("letsconnect_email", emailInput.value.trim());
//             }
//         });
//     });

//     fetch('/api/countries/')
//     .then(response => response.json())
//     .then(data => {
//         const dropdown = document.getElementById("popupCountryDropdown");
//         if (!dropdown) return;

//         dropdown.innerHTML = "";

//         const selectedFlag = document.getElementById("selectedFlag");
//         const selectedCode = document.getElementById("selectedCode");
//         const selectedCountryId = document.getElementById("selectedCountryId");

//         let defaultCountry = data.countries.find(c => c.code === "+91" || c.name.toLowerCase() === "india");

//         if (!defaultCountry && data.countries.length > 0) {
//             defaultCountry = data.countries[0]; // fallback
//         }

//         if (defaultCountry) {
//             if (selectedFlag) selectedFlag.src = defaultCountry.flag;
//             if (selectedCode) selectedCode.textContent = defaultCountry.code;
//             if (selectedCountryId) selectedCountryId.value = defaultCountry.id;
//         }

//         data.countries.forEach(country => {
//             const countryItem = document.createElement("div");
//             countryItem.classList.add("country-item");
//             countryItem.innerHTML = `
//                 <img src="${country.flag}" class="flag-img">
//                 <span>${country.code}</span>
//             `; 
//             countryItem.onclick = function () {
//                 if (selectedFlag) selectedFlag.src = country.flag;
//                 if (selectedCode) selectedCode.textContent = country.code;
//                 if (selectedCountryId) selectedCountryId.value = country.id;

//                 dropdown.style.display = "none";
//             };
//             dropdown.appendChild(countryItem);
//         });
//     })
//     .catch(error => console.error("Error fetching countries:", error));



// });