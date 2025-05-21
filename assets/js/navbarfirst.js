// const mobileExpandIcon = document.querySelector('.mobile-expand-icon');
// const closeIcon = document.querySelector('.close-icon');
// const mobileNavOpen = document.querySelector('.mobile-nav-open');

// mobileExpandIcon.addEventListener('click', (e) => {
//     e.preventDefault();
//     mobileNavOpen.style.display = 'flex';
// });

// closeIcon.addEventListener('click', (e) => {
//     e.preventDefault();
//     mobileNavOpen.style.display = 'none';
// });

// document.addEventListener('click', (e) => {
//     if (!mobileNavOpen.contains(e.target) && 
//         !mobileExpandIcon.contains(e.target) && 
//         mobileNavOpen.style.display === 'flex') {
//         mobileNavOpen.style.display = 'none';
//     }
// });

const mobileExpandIcon = document.querySelector('.mobile-expand-icon');
const closeIcon = document.querySelector('.close-icon');
const mobileNavOpen = document.querySelector('.mobile-nav-open');
const letsTalkBtn = document.querySelector('#lets-connect-popup-open');

mobileExpandIcon.addEventListener('click', (e) => {
    e.preventDefault();
    mobileNavOpen.style.display = 'flex';
});

closeIcon.addEventListener('click', (e) => {
    e.preventDefault();
    mobileNavOpen.style.display = 'none';
});

// Close the menu when clicking the "Let's talk" button
letsTalkBtn.addEventListener('click', (e) => {
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
