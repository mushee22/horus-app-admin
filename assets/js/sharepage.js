// share
document.addEventListener("DOMContentLoaded", function () {
    const shareButton = document.getElementById("share-page");
    const shareBox = document.querySelector(".share-box");

    shareButton.addEventListener("click", function () {
        shareBox.style.display = (shareBox.style.display === "flex") ? "none" : "flex";

        const currentUrl = encodeURIComponent(window.location.href);

        document.getElementById("whatsapp-share").href = `https://wa.me/?text=${currentUrl}`;
        document.getElementById("instagram-share").href = `https://www.instagram.com/?url=${currentUrl}`;
        document.getElementById("twitter-share").href = `https://twitter.com/share?url=${currentUrl}`;
        document.getElementById("facebook-share").href = `https://www.facebook.com/sharer/sharer.php?u=${currentUrl}`;
    });
});
