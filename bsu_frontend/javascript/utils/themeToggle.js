(function() {
    const storageKey = 'theme';
    const darkClass = 'dark-theme';

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add(darkClass);
        } else {
            document.body.classList.remove(darkClass);
        }
    }

    function toggleTheme() {
        const isDark = document.body.classList.toggle(darkClass);
        localStorage.setItem(storageKey, isDark ? 'dark' : 'light');
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Always use light theme on login page
        if (window.location.href.indexOf('login') > -1) {
            localStorage.setItem(storageKey, 'light');
            document.body.classList.remove(darkClass);
            return;
        }

        const savedTheme = localStorage.getItem(storageKey) || 'light';
        applyTheme(savedTheme);
        const buttons = document.querySelectorAll('.theme-toggle-btn');
        buttons.forEach(function(btn) {
            btn.addEventListener('click', toggleTheme);
        });
    });
})();