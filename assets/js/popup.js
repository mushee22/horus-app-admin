

document.addEventListener("DOMContentLoaded", function () {
    const letsConnectPopup = document.getElementById("lets-connect-popup");
    const helpPopup = document.getElementById("help-popup");
    const buyNowPopup = document.getElementById("buynow-popup"); 

    const letsConnectOpenBtns = document.querySelectorAll("#lets-connect-popup-open");
    const helpOpenBtn = document.getElementById("help-popup-open");
    const buyNowOpenBtn = document.getElementById("buynow-popup-open"); 

    const letsTalk = document.getElementById("lets-talk-id")

    const closeBtns = document.querySelectorAll(".close-btn");

    function showPopup(popup,popUpBody=null,direction=null) {
        if (popup) {
            popup.style.display = "flex"; 
        }
        if(popUpBody){
            popUpBody.classList.remove("closing")
            popUpBody.classList.add('active')
        }
    }

    function hidePopup(popup,popUpBody=null) {
        if (popup) {
            popup.style.display = "none";
        }
        if(popUpBody){
            popUpBody.classList.remove("active")
            popUpBody.classList.add('closing')
        }
    }

    letsConnectOpenBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            hidePopup(helpPopup);
            hidePopup(buyNowPopup);
            showPopup(letsConnectPopup);
        });
    });

    if (helpOpenBtn) {
        helpOpenBtn.addEventListener("click", function () {
            hidePopup(letsConnectPopup);
            hidePopup(buyNowPopup);
            showPopup(helpPopup,letsTalk);
        });
    }

    if (buyNowOpenBtn) {
        buyNowOpenBtn.addEventListener("click", function () {
            hidePopup(letsConnectPopup);
            hidePopup(helpPopup);
            showPopup(buyNowPopup);
        });
    }

    closeBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            hidePopup(letsConnectPopup);
            hidePopup(helpPopup);
            hidePopup(buyNowPopup);
        });
    });

    window.addEventListener("click", function (event) {
        if (event.target.classList.contains("popup-container")) {
            hidePopup(letsConnectPopup);
            hidePopup(helpPopup);
            hidePopup(buyNowPopup);
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const buyNowPopup = document.getElementById("buynow-popup"); 
    const buyNowOpenBtns = document.querySelectorAll("#buynow-popup-open"); 

    const appSelect = buyNowPopup.querySelector('select[name="app_name"]');
    const versionSelect = buyNowPopup.querySelector('select[name="version"]');

    function showPopup(popup) {
        if (popup) popup.style.display = "flex"; 
    }

    function hidePopup(popup) {
        if (popup) popup.style.display = "none";
    }

    function fetchVersions(appId) {
        fetch(`/apps/${appId}/versions/`)
            .then(response => response.json())
            .then(data => {
                versionSelect.innerHTML = ""; 
                data.forEach(version => {
                    const option = document.createElement("option");
                    option.value = version.id;
                    option.textContent = version.version_name;
                    versionSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Error fetching versions:", error));
    }

    buyNowOpenBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            hidePopup(document.getElementById("lets-connect-popup"));
            hidePopup(document.getElementById("help-popup"));
            showPopup(buyNowPopup);

            const appId = btn.getAttribute("data-app-id");
            const appName = btn.getAttribute("data-app-name");

            // Populate app select box
            appSelect.innerHTML = `<option value="${appId}">${appName}</option>`;
            fetchVersions(appId);
        });
    });

    appSelect.addEventListener("change", function () {
        fetchVersions(this.value);
    });

    document.querySelectorAll(".close-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            hidePopup(buyNowPopup);
        });
    });

    window.addEventListener("click", function (event) {
        if (event.target.classList.contains("popup-container")) {
            hidePopup(buyNowPopup);
        }
    });
});
