// favorites-dynamic.js
async function loadFavorites() {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '{}');

    const blogIds = favorites['blog'] || [];
    const caseStudyIds = favorites['casestudy'] || [];

    if (blogIds.length === 0 && caseStudyIds.length === 0) {
        clearFavoriteSections();
        return;
    }
 
    updateUnseenCounts();

    const queryParams = new URLSearchParams();
    blogIds.forEach(id => queryParams.append('blog_ids', id));
    caseStudyIds.forEach(id => queryParams.append('casestudy_ids', id));
    
    try {
        const response = await fetch(`/get-favorites/?${queryParams}`);
        const data = await response.json();

        renderBlogs(data.blogs);

        renderCaseStudies(data.case_studies);
    } catch (error) {
        console.error('Error fetching favorites:', error);
        clearFavoriteSections();
    }
}

function updateUnseenCounts() {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '{}');
    const seenBlogs = JSON.parse(sessionStorage.getItem('seenBlogs') || '[]');
    const seenCaseStudies = JSON.parse(sessionStorage.getItem('seenCaseStudies') || '[]');

    const unseenBlogCount = (favorites['blog'] || []).filter(id => !seenBlogs.includes(id)).length;
    const unseenCaseStudyCount = (favorites['casestudy'] || []).filter(id => !seenCaseStudies.includes(id)).length;
    const totalUnseenCount = unseenBlogCount + unseenCaseStudyCount;

    const blogCountElem = document.getElementById('blogCount');
    const caseStudyCountElem = document.getElementById('caseStudyCount');
    
    if (blogCountElem) {
        blogCountElem.textContent = unseenBlogCount > 0 ? unseenBlogCount : '';
        blogCountElem.style.display = unseenBlogCount > 0 ? 'flex' : 'none';
    }
    
    if (caseStudyCountElem) {
        caseStudyCountElem.textContent = unseenCaseStudyCount > 0 ? unseenCaseStudyCount : '';
        caseStudyCountElem.style.display = unseenCaseStudyCount > 0 ? 'flex' : 'none';
    }

    const navCountElem = document.querySelector('.notification-count');
    if (navCountElem) {
        navCountElem.textContent = totalUnseenCount > 0 ? (totalUnseenCount < 10 ? '0' + totalUnseenCount : totalUnseenCount) : '';
        navCountElem.style.display = totalUnseenCount > 0 ? 'flex' : 'none';
    }
}

function clearFavoriteSections() {
    const blogsSection = document.querySelector('.blogs-section .cards-grid');
    const caseStudiesSection = document.querySelector('.case-studies-section .cards-grid');
    
    if (blogsSection) blogsSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';
    if (caseStudiesSection) caseStudiesSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';

    sessionStorage.setItem('seenBlogs', '[]');
    sessionStorage.setItem('seenCaseStudies', '[]');

    updateUnseenCounts();
}

function renderBlogs(blogs) {
    const blogsSection = document.querySelector('.blogs-section .cards-grid');
    
    if (!blogs || !blogs.length) {
        blogsSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';
        return;
    }
    
    blogsSection.innerHTML = '';
    
    blogs.forEach(blog => {
        const blogCard = createBlogCard(blog);
        blogsSection.appendChild(blogCard);
    });
}

function renderCaseStudies(caseStudies) {
    const caseStudiesSection = document.querySelector('.case-studies-section .cards-grid');
    
    if (!caseStudies || !caseStudies.length) {
        caseStudiesSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';
        return;
    }
    
    caseStudiesSection.innerHTML = '';
    
    caseStudies.forEach(caseStudy => {
        const caseStudyCard = createCaseStudyCard(caseStudy);
        caseStudiesSection.appendChild(caseStudyCard);
    });
}

function createBlogCard(blog) {
    const cardDiv = document.createElement('div');
    cardDiv.classList.add('case-card');
    cardDiv.dataset.id = blog.id;
    cardDiv.dataset.type = 'blog';
    
    cardDiv.innerHTML = `
        <div class="p-relative">
            <a href="/blog-inner/${blog.slug}">
                <img class="case-card-img" src="${blog.image_url}" alt="Blog Image">
                <div class="fav-icon-container">
                <svg class="save-icon blog-unfavorate-icon" data-id="${blog.id}" 
                     width="19" height="23" viewBox="0 0 19 23" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1.3102 21.2837V1.72994H17.782V21.2837L10.0823 14.8673C9.77168 14.6085 9.32052 14.6085 9.00991 14.8673L1.3102 21.2837Z" 
                          fill="#EC9F06" stroke="white" stroke-width="1.6751" stroke-linejoin="round"/>
                </svg>
                </div>
            </a>
        </div>

        <div class="card-label-container d-flex ai-center gap-5 mt-20">
            ${blog.industries.map(industry => {
                const firstWord = industry.name.trim().split(' ')[0];
                return `<span class="card-labels fts-14 ftw-4 common-text bg-lt-blue ${industry.bg_class}">${firstWord}</span>`;
            }).join('')}
        </div>

        <span class="common-text fts-18 lt-black ftw-5 card-description mt-20">
            ${blog.description}
        </span>
        <div class="blog-user w-100 d-flex ai-center gap-5">
            <img src="${blog.customer_profile}" alt="User Profile">
            <span class="common-text fts-14 lt-gray ftw-4">${blog.customer_name}</span>
        </div>
    `;
    
    return cardDiv;
}

function createCaseStudyCard(caseStudy) {
    const cardDiv = document.createElement('div');
    cardDiv.classList.add('case-card');
    cardDiv.dataset.id = caseStudy.id;
    cardDiv.dataset.type = 'casestudy';

    cardDiv.innerHTML = `
        
            <div class="p-relative">
                <a href="/casestudy-inner/${caseStudy.slug}">
                    <img class="case-card-img" src="${caseStudy.image_url}" alt="Case Study Image">
                    <div class="fav-icon-container">
                    <svg class="save-icon casestudy-unfavorate-icon" data-id="${caseStudy.id}" 
                        width="19" height="23" viewBox="0 0 19 23" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1.3102 21.2837V1.72994H17.782V21.2837L10.0823 14.8673C9.77168 14.6085 9.32052 14.6085 9.00991 14.8673L1.3102 21.2837Z" 
                        fill="#EC9F06" stroke="white" stroke-width="1.6751" stroke-linejoin="round"/>
                    </svg>
                    </div>
                </a>
            </div>
        
        <div class="card-all-labels-container w-100 d-flex fd-column gap-5">
            <div class="card-label-container d-flex ai-center gap-5">
                <span class="card-labels fts-14 ftw-4 common-text bg-lt-gray">${caseStudy.country}</span>
            </div>
            <div class="card-label-container d-flex ai-center gap-5">
                ${caseStudy.industries.map(industry => {
                    const firstWord = industry.name.trim().split(' ')[0];
                    return `<span class="card-labels fts-14 ftw-4 common-text bg-lt-blue ${industry.bg_class}">${firstWord}</span>`;
                }).join('')}
            </div>
        </div>
        <span class="common-text fts-18 lt-black ftw-5 card-description">
            ${caseStudy.client_says}
        </span>
    `;
    
    return cardDiv;
}

function removeFromFavorites(type, id, clickedElement) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '{}');

    if (favorites[type]) {
        favorites[type] = favorites[type].filter(favId => favId !== id);

        if (favorites[type].length === 0) {
            delete favorites[type];
        }

        localStorage.setItem('favorites', JSON.stringify(favorites));

        let seenItems = JSON.parse(sessionStorage.getItem(type === 'blog' ? 'seenBlogs' : 'seenCaseStudies') || '[]');
        seenItems = seenItems.filter(seenId => seenId !== id);
        sessionStorage.setItem(type === 'blog' ? 'seenBlogs' : 'seenCaseStudies', JSON.stringify(seenItems));

        const cardElement = clickedElement.closest('.case-card');
        if (cardElement) {
            cardElement.remove();
        }

        updateUnseenCounts();

        checkEmptySections(type);
    }
}

function checkEmptySections(type) {
    if (type === 'blog') {
        const blogsSection = document.querySelector('.blogs-section .cards-grid');
        if (blogsSection && !blogsSection.querySelector('.case-card')) {
            blogsSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';
        }
    } else if (type === 'casestudy') {
        const caseStudiesSection = document.querySelector('.case-studies-section .cards-grid');
        if (caseStudiesSection && !caseStudiesSection.querySelector('.case-card')) {
            caseStudiesSection.innerHTML = '<div class="no-favorites ftw-4 fts-16 common-text"><p>Looks like your reading list is empty.</p><p>Whenever you find something worth a second look, just tap Save and we’ll add it here</p></div>';
        }
    }
}

function setupRemoveListeners() {
    document.addEventListener('click', function (event) {
        if (event.target.closest('.blog-unfavorate-icon')) {
            const icon = event.target.closest('.blog-unfavorate-icon');
            const id = icon.getAttribute('data-id');
            removeFromFavorites('blog', id, icon);
            event.preventDefault();
            event.stopPropagation();
        } 
        else if (event.target.closest('.casestudy-unfavorate-icon')) {
            const icon = event.target.closest('.casestudy-unfavorate-icon');
            const id = icon.getAttribute('data-id');
            removeFromFavorites('casestudy', id, icon);
            event.preventDefault();
            event.stopPropagation();
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadFavorites();
    setupRemoveListeners();

    document.querySelector('.case-study-btn').addEventListener('click', function() {
        document.querySelector('.case-studies-section').style.display = 'flex';
        document.querySelector('.blogs-section').style.display = 'none';
        this.classList.add('active');
        document.querySelector('.blog-btn').classList.remove('active');

        const favorites = JSON.parse(localStorage.getItem('favorites') || '{}');
        sessionStorage.setItem('seenCaseStudies', JSON.stringify(favorites['casestudy'] || []));
        updateUnseenCounts();
    });
    
    document.querySelector('.blog-btn').addEventListener('click', function() {
        document.querySelector('.blogs-section').style.display = 'flex';
        document.querySelector('.case-studies-section').style.display = 'none';
        this.classList.add('active');
        document.querySelector('.case-study-btn').classList.remove('active');
        
        const favorites = JSON.parse(localStorage.getItem('favorites') || '{}');
        sessionStorage.setItem('seenBlogs', JSON.stringify(favorites['blog'] || []));
        updateUnseenCounts();
    });
    
    document.querySelector('.case-study-btn').click();
});