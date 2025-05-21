const originalFontSizes = {
    'fts-60': 60,
    'fts-52': 52,
    'fts-50': 50,
    'fts-46': 46,
    'fts-43': 43,
    'fts-37': 37,
    'fts-35': 35,
    'fts-32': 32,
    'fts-30': 30,
    'fts-26': 26,
    'fts-24': 24,
    'fts-20': 20,
    'fts-17': 17,
    'fts-16': 16,
    'fts-14': 14
};

let isIncreased = false;

function increaseFontSizes() {
    if (!isIncreased) {
        Object.keys(originalFontSizes).forEach(className => {
            const elements = document.getElementsByClassName(className);
            
            Array.from(elements).forEach(element => {
                const computedStyle = window.getComputedStyle(element);
                const currentSize = parseFloat(computedStyle.fontSize);
                element.dataset.originalSize = currentSize; // store original size
                element.style.fontSize = `${currentSize + 3}px`;
            });
        });

        document.querySelector(".small-size").classList.remove("active");
        document.querySelector(".large-size").classList.add("active");

        isIncreased = true;
    }
}

function resetFontSizes() {
    if (isIncreased) {
        Object.keys(originalFontSizes).forEach(className => {
            const elements = document.getElementsByClassName(className);
            
            Array.from(elements).forEach(element => {
                if (element.dataset.originalSize) {
                    element.style.fontSize = `${element.dataset.originalSize}px`;
                    delete element.dataset.originalSize;
                }
            });
        });

        document.querySelector(".large-size").classList.remove("active");
        document.querySelector(".small-size").classList.add("active");

        isIncreased = false;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const fontSizeBtn = document.querySelector(".font-size-btn");
    const fontsContainer = fontSizeBtn.querySelector(".fonts-container");

    fontSizeBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        fontsContainer.classList.toggle("show");
    });

    document.addEventListener("click", function (event) {
        if (!fontSizeBtn.contains(event.target)) {
            fontsContainer.classList.remove("show");
        }
    });

    document.querySelector(".small-size").classList.add("active");
});
