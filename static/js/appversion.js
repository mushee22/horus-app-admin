// document.addEventListener("DOMContentLoaded", function () {
//     const versionButtons = document.querySelectorAll(".version-btn");

//     versionButtons.forEach(button => {
//         button.addEventListener("click", function () {
//             const appId = this.getAttribute("data-app-id");
//             const price = this.getAttribute("data-price");
//             const description = this.getAttribute("data-description");
//             const modules = this.getAttribute("data-modules");

//             document.getElementById(`version-price-${appId}`).textContent = `$${price}`;
//             document.getElementById(`version-description-${appId}`).textContent = description;
//             document.getElementById(`version-modules-${appId}`).textContent = `Modules: ${modules}`;

//             document.querySelectorAll(`.version-btn[data-app-id='${appId}']`).forEach(btn => {
//                 btn.classList.remove("selected-version");
//                 btn.style.backgroundColor = "gray";
//             });

//             this.classList.add("selected-version");
//             this.style.backgroundColor = "orange";
//         });
//     });

//     document.querySelectorAll(".version-btn.selected-version").forEach(btn => btn.click());
// });


document.addEventListener("DOMContentLoaded", function () {
    const versionButtons = document.querySelectorAll(".version-btn");
    
    // Track the currently selected version for each app
    const selectedVersions = {};

    versionButtons.forEach(button => {
        button.addEventListener("click", function () {
            const appId = this.getAttribute("data-app-id");
            const versionId = this.getAttribute("data-version-id");
            const price = this.getAttribute("data-price");
            const description = this.getAttribute("data-description");
            const modules = this.getAttribute("data-modules");
            
            // Store the selected version ID for this app
            selectedVersions[appId] = versionId;

            document.getElementById(`version-price-${appId}`).textContent = `$${price}`;
            document.getElementById(`version-description-${appId}`).textContent = description;
            document.getElementById(`version-modules-${appId}`).textContent = `Modules: ${modules}`;

            document.querySelectorAll(`.version-btn[data-app-id='${appId}']`).forEach(btn => {
                btn.classList.remove("selected-version");
                btn.style.backgroundColor = "gray";
            });

            this.classList.add("selected-version");
            this.style.backgroundColor = "orange";
        });
    });

    // Trigger click on default selected versions
    document.querySelectorAll(".version-btn.selected-version").forEach(btn => btn.click());