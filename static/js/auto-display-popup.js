// document.addEventListener("DOMContentLoaded", function () {
//     const buyNowPopup = document.getElementById("lets-connect-popup");

//     function showPopup(popup) {
//         if (popup) {
//             popup.style.display = "flex";
//         }
//     }

//     setTimeout(function () {
//         showPopup(buyNowPopup);
//     }, 1000);
// });
document.addEventListener("DOMContentLoaded", function () {
    const buyNowPopup = document.getElementById("lets-connect-popup");

    function showPopup(popup) {
        if (popup) {
            popup.style.display = "flex";
        }
    }

    // Only show if not already shown in this session
    if (!sessionStorage.getItem("popupShownOnce")) {
        // Check if it's a new visit or hard refresh (type 0 or 1)
        const navType = performance.navigation.type;
        if (navType === 0 || navType === 1) {
            setTimeout(function () {
                showPopup(buyNowPopup);
                sessionStorage.setItem("popupShownOnce", "true");
            }, 30000);
        }
    }
});
