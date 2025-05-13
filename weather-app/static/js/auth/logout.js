document.addEventListener('DOMContentLoaded', function (){
   const logOutForm = document.getElementById('logout-form')

    logOutForm.addEventListener("submit", function (event){
        event.preventDefault();
        fetch(logOutForm.action, {
            method: 'POST',
        })
            .then(response => {
                 window.location.href = '/'
            })
    })
});