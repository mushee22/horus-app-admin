// const toggleButton = document.querySelector(".toggle-button");
// const wholeContainer = document.querySelector(".whole_container");

// document.addEventListener("DOMContentLoaded", function() {
//     if (!toggleButton.classList.contains("active")) {
//         wholeContainer.classList.add("bg-white");
//         wholeContainer.classList.remove("read-mode-on");
//     }
// });

// toggleButton.addEventListener("click", function() {
//     this.classList.toggle("active");
    
//     if (this.classList.contains("active")) {
//         wholeContainer.classList.remove("bg-white");
//         wholeContainer.classList.add("read-mode-on");
//     } else {
//         wholeContainer.classList.add("bg-white");
//         wholeContainer.classList.remove("read-mode-on");
//     }
    
//     const isToggleEnabled = this.classList.contains("active");
//     localStorage.setItem("toggleState", isToggleEnabled);
// });

// document.addEventListener("DOMContentLoaded", function() {
//     const savedToggleState = localStorage.getItem("toggleState");
    
//     if (savedToggleState === "true") {
//         toggleButton.classList.add("active");
//         wholeContainer.classList.remove("bg-white");
//         wholeContainer.classList.add("read-mode-on");
//     } else {
//         toggleButton.classList.remove("active");
//         wholeContainer.classList.add("bg-white");
//         wholeContainer.classList.remove("read-mode-on");
//     }
// });
const toggleButton = document.querySelector(".toggle-button");
const wholeContainer = document.querySelector(".whole_container");
const paginationContainer = document.getElementById("pagination-container");

function updateReadingModeUI(isReadingModeOn) {
    if (isReadingModeOn) {
        wholeContainer.classList.remove("bg-white");
        wholeContainer.classList.add("read-mode-on");
        paginationContainer?.classList.add("reading-mode-pagination");
    } else {
        wholeContainer.classList.add("bg-white");
        wholeContainer.classList.remove("read-mode-on");
        paginationContainer?.classList.remove("reading-mode-pagination");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const savedToggleState = localStorage.getItem("toggleState") === "true";
    toggleButton.classList.toggle("active", savedToggleState);
    updateReadingModeUI(savedToggleState);
});

toggleButton.addEventListener("click", function() {
    const isActive = this.classList.toggle("active");
    updateReadingModeUI(isActive);
    localStorage.setItem("toggleState", isActive);
});
