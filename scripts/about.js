document.addEventListener('DOMContentLoaded', () => {
    setupInternalLinks();
    initUptime();
});

function initUptime() {
    const uptimeElement = document.getElementById('uptime-display');
    if (!uptimeElement) return;

    const serverStartTime = new Date(Date.UTC(2026, 1, 4, 16, 22, 21)); // Year, Month, Day, Hour, Minute, Seconds

    const updateDisplay = () => {
        const now = new Date();
        const diff = now - serverStartTime;

        if (diff < 0) {
            uptimeElement.textContent = "SERVER UPTIME: Something Broke :(";
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);

        uptimeElement.textContent = `SERVER UPTIME: ${days}d ${hours}h ${minutes}m ${seconds}s`;
    };

    updateDisplay();
    setInterval(updateDisplay, 1000);
}

function setupInternalLinks() {
    const internalLinks = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"])');
    internalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const destination = this.href;
            if (destination === window.location.href) return;

            e.preventDefault();
            document.body.classList.add('fade-out');
            setTimeout(() => {
                window.location.href = destination;
            }, 100);
        });
    });
}