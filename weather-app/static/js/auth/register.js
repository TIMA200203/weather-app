document.addEventListener('DOMContentLoaded', function (){
   const RegisterForm = document.getElementById('register-form')

    RegisterForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(RegisterForm)

        fetch(RegisterForm.action, {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (response.status === 200) {
                    window.location.href = '/users/login/'
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data) {

                    const usernameErrorDiv = document.getElementById('username-error');
                    const emailErrorDiv = document.getElementById('email-error');
                    const errorMessageDiv = document.getElementById('error-message');

                    if (data.non_field_errors) {
                        errorMessageDiv.innerHTML = data.non_field_errors;
                        errorMessageDiv.classList.remove('d-none');
                    }
                    if (data.username) {
                        usernameErrorDiv.innerHTML = data.username;
                        usernameErrorDiv.classList.remove('d-none');
                    }
                    if (data.email) {
                        emailErrorDiv.innerHTML = data.email;
                        emailErrorDiv.classList.remove('d-none');
                    }
                }
            })
    });
});