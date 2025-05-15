document.addEventListener("DOMContentLoaded", function() {
    const caseStudyBtn = document.querySelector(".case-study-btn");
    const blogBtn = document.querySelector(".blog-btn");
    const caseStudySection = document.querySelector(".case-studies-section");
    const blogSection = document.querySelector(".blogs-section");

    function showSection(activeButton, sectionToShow) {
        caseStudySection.style.display = "none";
        blogSection.style.display = "none";

        caseStudyBtn.classList.remove("active");
        blogBtn.classList.remove("active");

        sectionToShow.style.display = "flex"; 

        activeButton.classList.add("active");
    }

    showSection(caseStudyBtn, caseStudySection);

    caseStudyBtn.addEventListener("click", function() {
        showSection(caseStudyBtn, caseStudySection);
    });

    blogBtn.addEventListener("click", function() {
        showSection(blogBtn, blogSection);
    });
});