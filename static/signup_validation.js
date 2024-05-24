document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    form.addEventListener('submit', function (event) {
        let isValid = true;

        // Username validation
        const usernamePattern = /^[A-Za-z0-9_]{3,20}$/;
        if (!usernamePattern.test(username.value)) {
            isValid = false;
            showError(username, 'Username should be 3-20 characters long and can only contain letters, numbers, and underscores.');
        } else {
            clearError(username);
        }

        // Enhanced Email validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email.value)) {
            isValid = false;
            showError(email, 'Please enter a valid email address.');
        } else {
            clearError(email);
        }

        // Password validation
        if (password.value.length < 8) {
            isValid = false;
            showError(password, 'Password should be at least 8 characters long.');
        } else {
            clearError(password);
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if there are validation errors
        }
    });

    function showError(input, message) {
        const error = input.nextElementSibling;
        if (!error || !error.classList.contains('error-message')) {
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('error-message');
            errorMessage.textContent = message;
            input.insertAdjacentElement('afterend', errorMessage);
        } else {
            error.textContent = message;
        }
        input.classList.add('error');
    }

    function clearError(input) {
        const error = input.nextElementSibling;
        if (error && error.classList.contains('error-message')) {
            error.remove();
        }
        input.classList.remove('error');
    }
});
