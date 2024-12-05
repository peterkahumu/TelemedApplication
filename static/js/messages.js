document.addEventListener('DOMContentLoaded', function() {
    const messages = document.getElementById('messages');
    if (messages) {
        const duration = messages.getAttribute('data-duration');

        // Show the messages
        messages.classList.add('show');
        messages.style.animation = 'bounce 1s';

        // Fade out after the duration
        setTimeout(() => {
            messages.classList.remove('show');
            messages.style.display = 'none';
        }, duration);
    }
});

