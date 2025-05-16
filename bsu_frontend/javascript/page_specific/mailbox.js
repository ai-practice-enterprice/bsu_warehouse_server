document.addEventListener('DOMContentLoaded', function() {
    loadSavedNotifications();
    initializeSSE();
    initializeClearButton();
});

function initializeClearButton() {
    const clearButton = document.getElementById('clear-notifications');
    clearButton.addEventListener('click', function() {
        localStorage.removeItem('robotNotifications');
        if (confirm('Are you sure you want to clear all notifications?')) {
            setTimeout(() => {
                location.reload();
            }, 300);
        }
    });
}

function saveNotification(content, timestamp) {
    const notifications = JSON.parse(localStorage.getItem('robotNotifications') || '[]');
    notifications.push({
        content: content,
        timestamp: timestamp
    });
    
    if(notifications.length > 100) {
        notifications.shift();
    }
    
    localStorage.setItem('robotNotifications', JSON.stringify(notifications));
}

function loadSavedNotifications() {
    const mailboxContainer = document.getElementById('mailbox-container');
    const savedNotifications = JSON.parse(localStorage.getItem('robotNotifications') || '[]');
    
    if (savedNotifications.length > 0) {
        const waitingMessage = mailboxContainer.querySelector('.text-center.p-5');
        if (waitingMessage) {
            mailboxContainer.removeChild(waitingMessage);
        }

        savedNotifications.forEach(notification => {
            displayNotification(notification.content, notification.timestamp, false);
        });
    }
}

function displayNotification(content, timestamp, isNew = true) {
    const mailboxContainer = document.getElementById('mailbox-container');

    const waitingMessage = mailboxContainer.querySelector('.text-center.p-5');
    if (waitingMessage) {
        mailboxContainer.removeChild(waitingMessage);
    }
    
    const notificationCard = document.createElement('div');
    notificationCard.className = 'card notification-card';

    notificationCard.innerHTML = `
        <div class="card-header d-flex justify-content-between align-items-center">
            <span class="notification-title">Robot Notification</span>
            <small class="text-muted">${timestamp}</small>
        </div>
        <div class="card-body">
            <pre class="notification-content">${content}</pre>
        </div>
    `;

    mailboxContainer.insertBefore(notificationCard, mailboxContainer.firstChild);
    if(isNew) {
        notificationCard.classList.add('new-notification');
        setTimeout(() => {
            notificationCard.classList.remove('new-notification');
        }, 3000);
        
        saveNotification(content, timestamp);
    }
}

function initializeSSE() {
    const apiBaseUrl = serverURLPrefix.replace('/frontend', '');
    const eventSource = new EventSource(`${apiBaseUrl}/notification/sse`);

    eventSource.onopen = function() {
        console.log('SSE connection established');
    };

    eventSource.onmessage = function(event) {
        const data = event.data;
        const timestamp = new Date().toLocaleString();
        displayNotification(data, timestamp, true);
    };

    eventSource.onerror = function(error) {
        console.error('SSE connection error:', error);
        setTimeout(() => {
            console.log('Attempting to reconnect...');
            eventSource.close();
            initializeSSE();
        }, 5000);
    };
}
