
document.addEventListener("DOMContentLoaded", function () {
    const tagSections = document.querySelectorAll('.multi-tag');
    tagSections.forEach(section=>{
        updateTagVisibility(section)
        const dropdownOptions = section.querySelector('.dropdown-menu');
        dropdownOptions.addEventListener("click", function (event) {
            event.preventDefault();
            const value = event.target.getAttribute("data-value");
            const text = event.target.textContent;
            if (value) addTag(value, text,section);
        });
        // Handle pre-selected values
        const selectedValues = section.querySelector('.selected_values');
        if (selectedValues && selectedValues.dataset.value) {

            // const values = selectedValues.dataset.value
            // console.log(typeof values)
            // values.forEach(([value, text]) => {
            //     console.log(value, text, "Adding pre-selected tag.");
            //     // addTag(value, text, section);
            // });

        }
    })
});

// Function to update visibility of selected tags section
function updateTagVisibility(section) {
    selectedTags = section.querySelector('.tagsShowSection')
    if(selectedTags.children.length > 0){
        selectedTags.classList.add('d-flex');
        selectedTags.classList.remove('d-none');
    }else{
        selectedTags.classList.remove('d-flex');
        selectedTags.classList.add('d-none');
    }
}

 // Function to add a tag
function addTag(value,text,section) {
    const tagSelection = section.querySelector(".tagSelection");
    let selectedTags = section.querySelector('.tagsShowSection');

    // Check if already selected
    if ([...tagSelection.options].some(opt => opt.value === value && opt.selected)) return;
    
    const tag = document.createElement("span");
    tag.setAttribute("data-value",value)
    tag.className = "badge bg-primary p-2";
    tag.innerHTML = `${text} <span class="ms-1 text-white fw-bold" style="cursor:pointer;">&times;</span>`;
    tag.addEventListener("click",()=>removeTag(value,section))
    
    selectedTags.appendChild(tag);

    [...tagSelection.options].forEach(opt => {
        if (opt.value === value) opt.selected = true;
    });

    updateTagVisibility(section);
}

// Function to remove a tag
window.removeTag = function (value,section) {
    const tagSelection = section.querySelector(".tagSelection");
    let selectedTags = section.querySelector('.tagsShowSection');

    [...tagSelection.options].forEach(opt => {
        if (opt.value === value) opt.selected = false;
    });

    [...selectedTags.children].forEach(tag => {
        if (tag.dataset.value.includes(value)) tag.remove();
    });

    updateTagVisibility(section); // Hide tags section if empty
};