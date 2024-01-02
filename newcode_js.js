const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

window.addEventListener("load", function () {
    const loader = document.getElementById("loader-wrapper");
    loader.style.visibility = "hidden";
});

$('.form-box.login form').submit(function(event) {
    event.preventDefault();
    const identifiant = $('#login-identifiant').val(); // Assurez-vous d'avoir des ID correspondants dans votre HTML
    const motdepasse = $('#login-motdepasse').val();
    seConnecter({ identifiant: identifiant, motdepasse: motdepasse });
});

$('.form-box.register form').submit(function(event) {
    event.preventDefault();
    const identifiant = $('#register-identifiant').val();
    const email = $('#register-email').val();
    const motdepasse = $('#register-motdepasse').val();
    inscrireUtilisateur({ identifiant: identifiant, email: email, motdepasse: motdepasse });
});

function inscrireUtilisateur(userData) {
    fetch('/api/inscription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.message === "Inscription réussie") {
            $('.wrapper').hide(); // Cache l'interface d'inscription
        }
    });
}

function createUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/create_user', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "username": username,
        "password": password,
        "email": email
    }));
}

function seConnecter() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "username": username,
        "password": password
    }));
}



