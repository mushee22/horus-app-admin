// favorites.js

const FavoriteManager = {
    getFavorites() {
        return JSON.parse(localStorage.getItem('favorites') || '{}');
    },

    saveFavorites(favorites) {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    },

    addToFavorites(type, id) {
        console.log(`Adding to favorites: Type=${type}, ID=${id}`);
        
        let favorites = this.getFavorites(); 
        
        if (!favorites[type]) {
            favorites[type] = [];
        }
    
        if (!favorites[type].includes(id)) {
            favorites[type].push(id);
            this.saveFavorites(favorites);
        }
    
        this.updateFavoriteUI(type, id, true);
        this.updateFavoriteCounts();
    },

    removeFromFavorites(type, id) {
        console.log(`Removing from favorites: Type=${type}, ID=${id}`);
        
        let favorites = this.getFavorites();
        
        if (favorites[type]) {
            favorites[type] = favorites[type].filter(itemId => itemId.toString() !== id.toString());

            if (favorites[type].length === 0) {
                delete favorites[type];
            }
            
            this.saveFavorites(favorites);
        }
    
        // this.updateFavoriteUI(type, id, false);
        // this.updateFavoriteCounts();
        this.updateFavoriteUI(type, id, false);
        this.updateFavoriteCounts();
        loadFavorites();  // <- trigger dynamic re-render

    },

    updateFavoriteUI(type, id, isFavorite) {
        console.log(`Updating UI: Type=${type}, ID=${id}, isFavorite=${isFavorite}`);

        const favoriteIcons = document.querySelectorAll(`.${type}-favorate-icon[data-id="${id}"]`);
        const unfavoriteIcons = document.querySelectorAll(`.${type}-unfavorate-icon[data-id="${id}"]`);

        favoriteIcons.forEach(icon => {
            icon.style.display = isFavorite ? 'none' : 'block';
        });

        unfavoriteIcons.forEach(icon => {
            icon.style.display = isFavorite ? 'block' : 'none';
        });
    },

    updateFavoriteCounts() {
        const favorites = this.getFavorites();
        
        const blogCount = document.getElementById('blogCount');
        const caseStudyCount = document.getElementById('caseStudyCount');
        
        if (blogCount) {
            const count = favorites['blog'] ? favorites['blog'].length : 0;
            blogCount.textContent = count;
            blogCount.style.display = count > 0 ? 'flex' : 'none';
        }
        
        if (caseStudyCount) {
            const count = favorites['casestudy'] ? favorites['casestudy'].length : 0;
            caseStudyCount.textContent = count;
            caseStudyCount.style.display = count > 0 ? 'flex' : 'none';
        }
    },

    initializeFavoriteIcons() {
        const favorites = this.getFavorites();

        if (favorites['blog']) {
            favorites['blog'].forEach(id => {
                this.updateFavoriteUI('blog', id, true);
            });
        }

        if (favorites['casestudy']) {
            favorites['casestudy'].forEach(id => {
                this.updateFavoriteUI('casestudy', id, true);
            });
        }
        
        this.updateFavoriteCounts();
    },

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            const favoriteIcon = e.target.closest('.blog-favorate-icon, .casestudy-favorate-icon');
            if (favoriteIcon) {
                e.preventDefault();
                const id = favoriteIcon.getAttribute('data-id');
                const type = favoriteIcon.classList.contains('blog-favorate-icon') ? 'blog' : 'casestudy';
                this.addToFavorites(type, id);
                return;
            }

            const unfavoriteIcon = e.target.closest('.blog-unfavorate-icon, .casestudy-unfavorate-icon');
            if (unfavoriteIcon) {
                e.preventDefault();
                const id = unfavoriteIcon.getAttribute('data-id');
                const type = unfavoriteIcon.classList.contains('blog-unfavorate-icon') ? 'blog' : 'casestudy';
                this.removeFromFavorites(type, id);
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    console.log("Page Loaded, initializing favorites...");
    FavoriteManager.initializeFavoriteIcons();
    FavoriteManager.setupEventListeners();
    FavoriteManager.updateFavoriteCounts(); 
});