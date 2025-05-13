document.addEventListener('DOMContentLoaded', function () {
    const subscriptionForm = document.getElementById('subscription-form');
    subscriptionForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(subscriptionForm);

        fetch(subscriptionForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${getCookie('access_token')}`
            }
        })
            .then(response => {
                if (response.ok) {
                    window.location = '/subscriptions/';
                } else if (response.status === 400) {
                    displayErrors(response)
                } else if (response.status === 401) {

                    fetch('/api/auth/v1/token/refresh/', {
                        method: 'POST',
                        body: JSON.stringify({
                            'refresh': getCookie('refresh_token')
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            } else {
                                window.location = '/users/login/';
                                throw new Error('Failed to refresh token');
                            }
                        })
                        .then(data => {
                            const newAccess = data.access;
                            document.cookie = `access_token=${newAccess}; path=/`

                            fetch(subscriptionForm.action, {
                                method: 'POST',
                                body: formData,
                                headers: {
                                    'Authorization': `Bearer ${getCookie('access_token')}`
                                }
                            })
                                .then(response => {
                                    if (response.ok) {
                                        window.location = '/subscriptions/';
                                    } else if (response.status === 401) {
                                        window.location = '/users/login/';
                                    }
                                });
                        })
                        .catch(error => {
                            console.error('Error refreshing token:', error);
                        });
                }
            });
    });
});

function displayErrors(response) {
    response.json().then(data => {
        const errors = data.non_field_errors
        const errorContainer = document.getElementById('error-display');
        errorContainer.innerHTML = ''
        errors.forEach(error => {
            const errorListItem = document.createElement('li');
            if (error === 'The fields user, city must make a unique set.'){
                error = 'You already has subscription to this city'
            }
            errorListItem.textContent = error;
            errorContainer.appendChild(errorListItem);
        });
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
