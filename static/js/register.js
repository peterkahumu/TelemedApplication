const first_name = document.querySelector('#first_name');
const last_name = document.querySelector('#last_name');
const email = document.querySelector('#email');

const first_name_error = document.querySelector('#fname-invalid');
const last_name_error = document.querySelector('#lname-invalid');
const username_error = document.querySelector('#username-invalid');
const email_error = document.querySelector('#email-invalid');

const submitButton = document.querySelector('#submit');

let debounceTimeout;

first_name.addEventListener('keyup', (event) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        const first_name_val = event.target.value;

        if (first_name_val.length > 0) {
            fetch('/authenticate/validate_name', {
                body: JSON.stringify({ name: first_name_val }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.name_error) {
                    first_name.classList.add("is-invalid");
                    first_name_error.style.display = "block";
                    first_name_error.textContent = data.name_error;
                    submitButton.setAttribute('disabled', 'disabled');
                    submitButton.disabled = true;
                } else {
                    first_name.classList.remove("is-invalid");
                    first_name.classList.add("is-valid");
                    first_name_error.style.display = "none";
                    submitButton.removeAttribute('disabled');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            first_name.classList.remove("is-invalid", "is-valid");
            first_name_error.style.display = "none";
            submitButton.removeAttribute('disabled');
        }
    }, 300);
});

last_name.addEventListener('keyup', (event) => {
    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(()=> {
        const last_name_val = event.target.value;
         
        if (last_name_val.length > 0){
            fetch('/authenticate/validate_name', {
                body: JSON.stringify({name: last_name_val}),
                method: 'POST',               
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.name_error){
                    last_name.classList.add("is-invalid");
                    last_name_error.style.display = "block";
                    first_name_error.textContent = data.name_error;
                    submitButton.setAttribute('disabled', 'disabled');
                    submitButton.disabled = true;
                } else {
                    last_name.classList.remove("is-invalid");
                    last_name.classList.add("is-valid");
                    last_name_error.style.display = "none";
                    submitButton.removeAttribute('disabled');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        } else {
            last_name.classList.remove("is-invalid", "is-valid");
            last_name_error.style.display = "none";
            submitButton.removeAttribute('disabled');
        }
    }, 300);
})

username.addEventListener('keyup', (event) => {
    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(()=> {
        const username_val = event.target.value;
         
        if (username_val.length > 0){
            fetch('/authenticate/validate_username', {
                body: JSON.stringify({username: username_val}),
                method: 'POST',               
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error){
                    username.classList.add("is-invalid");
                    username_error.style.display = "block";
                    username_error.textContent = data.username_error;
                    submitButton.setAttribute('disabled', 'disabled');
                    submitButton.disabled = true;
                } else {
                    username.classList.remove("is-invalid");
                    username.classList.add("is-valid");
                    username_error.style.display = "none";
                    submitButton.removeAttribute('disabled');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            username.classList.remove("is-invalid", "is-valid");
            username_error.style.display = "none";
            submitButton.removeAttribute('disabled');
        }
    }, 300);
});

email.addEventListener('keyup', (event) => {
    clearTimeout(debounceTimeout);

    debounceTimeout = setTimeout(()=> {
        const email_val = event.target.value;
         
        if (email_val.length > 0){
            fetch('/authenticate/validate_email', {
                body: JSON.stringify({email: email_val}),
                method: 'POST',               
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error){
                    email.classList.add("is-invalid");
                    email_error.style.display = "block";
                    email_error.textContent = data.email_error;
                    submitButton.setAttribute('disabled', 'disabled');
                    submitButton.disabled = true;
                } else {
                    email.classList.remove("is-invalid");
                    email.classList.add("is-valid");
                    email_error.style.display = "none";
                    submitButton.removeAttribute('disabled');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            email.classList.remove("is-invalid", "is-valid");
            email_error.style.display = "none";
            submitButton.removeAttribute('disabled');
        }
    }, 300);
});

// Toogle the doctors fields when the user selects the doctor option
document.getElementById('role').addEventListener('change', function () {
    const role = this.value;
    const doctorFields = document.getElementById('doctorFields');
    if (role == '2') { // This is the id to the doctors field.
        doctorFields.style.display = 'block';
    } else {
        doctorFields.style.display = 'none';
    }
}); // when the user changes the role.

window.addEventListener('load', function () {
    const role = document.getElementById('role').value;
    const doctorFields = document.getElementById('doctorFields');
    if (role == '2') { 
        doctorFields.style.display = 'block';
    }
}); //when the form is rendered from the backend