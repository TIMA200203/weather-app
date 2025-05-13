document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessageDiv = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(loginForm);

        fetch(loginForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.status === 200) {
                window.location.href = '/';
            } else if (response.status === 400) {
                return response.json()
            }
        })
            .then(data => {
                errorMessageDiv.textContent = data.error
                errorMessageDiv.classList.remove('d-none');
            })
    });
});