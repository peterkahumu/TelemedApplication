const first_name = document.querySelector('#first-name');
const last_name = document.querySelector('#last-name');
const username = document.querySelector('#username');
const email = document.querySelector('#email');
const password = document.querySelector('#password');
const confirm_password = document.querySelector('#confirm-password');
const role = document.querySelector('#role');

const submitButton = document.querySelector('#submit');

// error messages

const first_name_error = document.querySelector('.first-name-feedback');
const last_name_error = document.querySelector('.last-name-feedback');
const username_error = document.querySelector('.username-feedback');
const email_error = document.querySelector('.email-feedback');
const password_error = document.querySelector('.password-feedback');
const confirm_password_error = document.querySelector('.confirm-password-feedback');
const role_error = document.querySelector('.role-feedback');

// Validate username from the backend
first_name.addEventListener('keyup', (event)=>{
    const name_val = event.target.value.trim();

    if (name_val.length > 0) {
        fetch('/authenticate/validate_name', {
            body: JSON.stringify({name: name_val}),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.name_error) {

                first_name_error.style.display = "block";
                first_name_error.textContent = data.name_error;
                submitButton.setAttribute('disabled', 'disabled');
                submitButton.disabled = true;                
            } else {
                first_name_error.style.display = "none";
                submitButton.removeAttribute('disabled');
                submitButton.disabled = false;
            }
        })
    }
})

// validate last name from the backend
last_name.addEventListener('keyup', (event)=>{
    const name_val = event.target.value.trim();

    if (name_val.length > 0) {
        fetch('/authenticate/validate_name', {
            body: JSON.stringify({name: name_val}),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.name_error) {

                last_name_error.style.display = "block";
                last_name_error.textContent = data.name_error;
                submitButton.setAttribute('disabled', 'disabled');
                submitButton.disabled = true;                
            } else {
                last_name_error.style.display = "none";
                submitButton.removeAttribute('disabled');
                submitButton.disabled = false;
            }
        })
    }
})

// validate username from the backend
username.addEventListener('keyup', (event) => {
    const username_val = event.target.value.trim();

    if (username_val.length > 0) {
        fetch('/authenticate/validate_username', {
            body: JSON.stringify({username: username_val}),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.username_error) {

                username_error.style.display = "block";
                username_error.textContent = data.username_error;
                submitButton.setAttribute('disabled', 'disabled');
                submitButton.disabled = true;
            } else {

                username_error.style.display = "None";
                submitButton.removeAttribute('disabled');
                submitButton.disabled = false;
            }
        })
    }
})

// validate email from the backend
email.addEventListener('keyup', (event) => {
    const email_val = event.target.value.trim();

    if (email_val.length > 0) {
        fetch('/authenticate/validate_email', {
            body: JSON.stringify({email: email_val}),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.email_error) {

                email_error.style.display = "block";
                email_error.textContent = data.email_error;
                submitButton.setAttribute('disabled', 'disabled');
                submitButton.disabled = true;
            } else {

                email_error.style.display = "None";
                submitButton.removeAttribute('disabled');
                submitButton.disabled = false;
            }
        })
    }
})