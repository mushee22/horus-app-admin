// document.addEventListener("DOMContentLoaded", function () {
//     const tryItNowTop = document.getElementById("tryitnow-top");
//     const tryItNowBottom = document.getElementById("tryitnow-bottom");
//     const popup = document.getElementById("popup");
//     const closePopupBtn = document.querySelector(".close-popup-btn");

//     function openPopup() {
//         popup.style.display = "flex";
//     }

//     function closePopup() {
//         popup.style.display = "none";
//     }

//     if (tryItNowTop) {
//         tryItNowTop.addEventListener("click", openPopup);
//     }
//     if (tryItNowBottom) {
//         tryItNowBottom.addEventListener("click", openPopup);
//     }

//     if (closePopupBtn) {
//         closePopupBtn.addEventListener("click", closePopup);
//     }

//     popup.addEventListener("click", function (event) {
//         if (event.target === popup) {
//             closePopup();
//         }
//     });

//     const popupForm = document.getElementById("popup-form");
//     if (popupForm) {
//         popupForm.addEventListener("submit", function (event) {
//             event.preventDefault();
//             const firstName = document.getElementById("firstName").value;
//             const lastName = document.getElementById("lastName").value;
//             const email = document.getElementById("email").value;
//             const phone = document.getElementById("phone").value;

//             console.log("Form submitted:", { firstName, lastName, email, phone });

//             closePopup();
//         });
//     }
// });