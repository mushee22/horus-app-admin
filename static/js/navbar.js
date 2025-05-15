document.addEventListener('DOMContentLoaded', () => {
    fetch('navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
            initializeMobileNav();
        });
});

function initializeMobileNav() {
    const mobileExpandIcon = document.querySelector('.mobile-expand-icon');
    const closeIcon = document.querySelector('.close-icon');
    const mobileNavOpen = document.querySelector('.mobile-nav-open');

    if (mobileExpandIcon && closeIcon && mobileNavOpen) {
        mobileExpandIcon.addEventListener('click', (e) => {
            e.preventDefault();
            mobileNavOpen.style.display = 'flex';
        });

        closeIcon.addEventListener('click', (e) => {
            e.preventDefault();
            mobileNavOpen.style.display = 'none';
        });

        document.addEventListener('click', (e) => {
            if (!mobileNavOpen.contains(e.target) && 
                !mobileExpandIcon.contains(e.target) && 
                mobileNavOpen.style.display === 'flex') {
                mobileNavOpen.style.display = 'none';
            }
        });
    }
}

fetch('footer.html')
    .then(response => response.text())
    .then(data => document.getElementById('footer').innerHTML = data);