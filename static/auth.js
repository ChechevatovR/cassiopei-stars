function toggleview(elem) {
    let id = elem.getAttribute('target');
    if (document.getElementById(id).getAttribute('type') === 'text') {
        document.getElementById(id).setAttribute('type', 'password');
        elem.innerHTML = '<i class="far fa-eye"></i>';
    } else {
        document.getElementById(id).setAttribute('type', 'text');
        elem.innerHTML = '<i class="far fa-eye-slash"></i>';
    }
}

function checkPasswords() {
    var pass = document.getElementById('user-pass').value;
    var repeat = document.getElementById('user-pass-repeat').value;

    if (pass != repeat) {
        document.getElementById('form-submit').setAttribute('disabled', '');
        document.getElementById('form-submit').setAttribute('title', 'Пароли не совпадают');
    } else {
        document.getElementById('form-submit').removeAttribute('disabled');
        document.getElementById('form-submit').removeAttribute('title');

    }
}