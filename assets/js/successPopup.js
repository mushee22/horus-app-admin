// successPopup.js 
// window.showSuccessPopup = function ({
//     popupId = "successPopup",
//     closePopupId = "lets-connect-popup",
//     autoHide = true,
//     delay = 3000
// } = {}) {
//     const successPopup = document.getElementById(popupId);
//     const closePopup = document.getElementById(closePopupId);

//     if (successPopup) {
//         successPopup.classList.add("active");

//         if (autoHide) {
//             setTimeout(() => {
//                 successPopup.classList.remove("active");

//                 if (closePopup) {
//                     closePopup.classList.remove("active");
//                     closePopup.style.display = "none";
//                 }
//             }, delay);
//         }
//     }
// }
window.showSuccessPopup = function ({
    popupId = "successPopup",
    closePopupId = null,
    autoHide = true,
    delay = 3000
} = {}) {
    const successPopup = document.getElementById(popupId);
    const closePopup = closePopupId ? document.getElementById(closePopupId) : null;

    if (successPopup) {
        successPopup.classList.add("active");

        if (autoHide) {
            setTimeout(() => {
                successPopup.classList.remove("active");

                if (closePopup) {
                    closePopup.classList.remove("active");
                    closePopup.style.display = "none";
                }
            }, delay);
        }
    }
}
