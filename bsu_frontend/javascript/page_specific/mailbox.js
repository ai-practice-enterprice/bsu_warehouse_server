document.addEventListener('DOMContentLoaded', function() {
    initializeSSE();
});

function initializeSSE() {
    const mailboxContainer = document.getElementById('mailbox-container');
    const apiBaseUrl = serverURLPrefix.replace('/frontend', '');
    const eventSource = new EventSource(`${apiBaseUrl}/notification/sse`);

    eventSource.onopen = function() {
        console.log('SSE connection established');
    };

    eventSource.onmessage = function(event) {
        const data = event.data;
        displayNotification(data);
    };

    eventSource.onerror = function(error) {
        console.error('SSE connection error:', error);
        setTimeout(() => {
            console.log('Attempting to reconnect...');
            eventSource.close();
            initializeSSE();
        }, 5000);
    };

    function displayNotification(data) {
        const waitingMessage = mailboxContainer.querySelector('.text-center.p-5');
        if (waitingMessage) {
            mailboxContainer.removeChild(waitingMessage);
        }

        const notificationCard = document.createElement('div');
        notificationCard.className = 'card notification-card';
        const timestamp = new Date().toLocaleString();

        notificationCard.innerHTML = `
            <div class="card-header d-flex justify-content-between align-items-center">
                <span class="notification-title">Robot Notification</span>
                <small class="text-muted">${timestamp}</small>
            </div>
            <div class="card-body">
                <pre class="notification-content">${data}</pre>
            </div>
        `;

        mailboxContainer.insertBefore(notificationCard, mailboxContainer.firstChild);

        notificationCard.classList.add('new-notification');
        setTimeout(() => {
            notificationCard.classList.remove('new-notification');
        }, 3000);
    }
}