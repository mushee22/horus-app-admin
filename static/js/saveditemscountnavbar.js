document.addEventListener('DOMContentLoaded', function() {
    function updateNotificationCount() {
        const favorites = JSON.parse(localStorage.getItem('favorites') || '{}');

        const seenBlogs = JSON.parse(sessionStorage.getItem('seenBlogs') || '[]');
        const seenCaseStudies = JSON.parse(sessionStorage.getItem('seenCaseStudies') || '[]');

        const unseenBlogs = (favorites.blog || []).filter(id => !seenBlogs.includes(id)).length;
        const unseenCaseStudies = (favorites.casestudy || []).filter(id => !seenCaseStudies.includes(id)).length;

    //     const totalUnseen = unseenBlogs + unseenCaseStudies;
        
    //     const unseenCountElements = document.querySelectorAll('.unseenCount');
    //     unseenCountElements.forEach(el => {
    //         el.textContent = totalUnseen > 99 ? '99+' : String(totalUnseen).padStart(2);
    //         el.style.display = totalUnseen > 0 ? 'flex' : 'none';
    //     });
    // }
    
    // updateNotificationCount();

    const totalUnseen = unseenBlogs + unseenCaseStudies;

    const unseenCountElements = document.querySelectorAll('.unseenCount');
    unseenCountElements.forEach(el => {
        const count = totalUnseen > 99 ? '99+' : String(totalUnseen).padStart(2, '0');
        el.textContent = count;
        el.style.display = totalUnseen > 0 ? 'inline-flex' : 'none';
    });
    
    }

    updateNotificationCount();

    setInterval(updateNotificationCount, 1200);

    const notificationEvent = new CustomEvent('updateNotifications');
    
    const favoritesObserver = new MutationObserver(function(mutations) {
        updateNotificationCount();
    });

    if (window.FavoriteManager) {
        const originalAddToFavorites = FavoriteManager.addToFavorites;
        const originalRemoveFromFavorites = FavoriteManager.removeFromFavorites;

        FavoriteManager.addToFavorites = function(type, id) {
            originalAddToFavorites.call(this, type, id);
            updateNotificationCount();
        };
        
        FavoriteManager.removeFromFavorites = function(type, id) {
            originalRemoveFromFavorites.call(this, type, id);
            updateNotificationCount();
        };
    }

    document.addEventListener('click', function(e) {
        if (e.target.closest('.blog-favorate-icon, .casestudy-favorate-icon, .blog-unfavorate-icon, .casestudy-unfavorate-icon')) {
            setTimeout(updateNotificationCount, 50);
        }
    });

    document.addEventListener('updateNotifications', updateNotificationCount);
    
    window.addEventListener('storage', function(e) {
        if (e.key === 'favorites' || e.key === 'seenBlogs' || e.key === 'seenCaseStudies') {
            updateNotificationCount();
        }
    });

    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            updateNotificationCount();
        }
    });
});