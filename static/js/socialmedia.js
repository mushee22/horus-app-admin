document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/social/")
        .then(response => response.json())
        .then(data => {
            const socialMediaIcons = data.socialmedias;

            const sections = {
                "navbar": document.querySelector("[data-section='navbar']"),
                "footer": document.querySelector("[data-section='footer']"),
                "popup": document.querySelector("[data-section='popup']")
            };

            if (socialMediaIcons.length > 0) {
                Object.keys(sections).forEach(section => {
                    const container = sections[section];
                    if (container) {
                        container.innerHTML = "";  // Clear previous icons

                        socialMediaIcons.forEach(social => {
                            const imgClass =
                                section === "navbar" ? "cw8-white-img" :
                                section === "footer" ? "social-icons-footer-img" :
                                "small-social";

                            const socialLink = document.createElement("a");
                            socialLink.href = social.link;
                            socialLink.target = "_blank";

                            const socialImg = document.createElement("img");
                            socialImg.src = social.icon_image;
                            socialImg.classList.add(imgClass);

                            socialLink.appendChild(socialImg);
                            container.appendChild(socialLink);
                        });
                    }
                });
            }
        })
        .catch(error => console.error("Error loading social media icons:", error));
});
