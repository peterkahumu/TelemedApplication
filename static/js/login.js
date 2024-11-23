document.addEventListener('DOMContentLoaded', () => {
    const username = document.querySelector('#username');
    const password = document.querySelector('#password');
    const submit = document.querySelector('#submit');

    const usernameError = document.querySelector('#username-error');
    const passwordError = document.querySelector('#password-error');

    usernameError.textContent = '';
    passwordError.textContent = '';

    submit.addEventListener('click', (event) => {
        event.preventDefault();

        let isValid = true;

        // ensure username is not empty and does not contain special characters
        if (username.value === '' || !/^[a-zA-Z]+$/.test(username.value)) {
            usernameError.textContent = 'Please enter a valid username';
            isValid = false;
        }

        // ensure password is not empty and is at least 6 characters long 
        if (password.value === '' || password.value.length < 6) {
            passwordError.textContent = 'Please enter a valid password';
            isValid = false;
        }

        // clear error messages when user starts typing
        username.addEventListener('keyup', () => {
            usernameError.textContent = '';
        });

        password.addEventListener('keyup', () => {
            passwordError.textContent = '';
        });


        if(isValid) {
            window.location.href = 'index.html';
        }
    });
});