// External functions

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {

  options = {
    path: '/',
    expires: 'Tue, 19 Jan 2038 03:14:07 GMT',
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}

// My function

let icodark = '<i class="fas fa-moon"></i>'
let icolight = '<i class="fas fa-sun"></i>'

function checkCookie() {
    if (getCookie('theme') === undefined) {
        setCookie('theme', 'light')
    }
}

function themeChanger() {
    checkCookie();
    if (getCookie('theme') === 'light') {
        document.body.classList.add('dark-mode')
        setCookie('theme', 'dark')
        document.getElementById('btn-theme').innerHTML = icodark
    } else {
        document.body.classList.remove('dark-mode')
        setCookie('theme', 'light')
        document.getElementById('btn-theme').innerHTML = icolight
    }
}

function pageStartTheme() {
    if (getCookie('theme') === 'dark') {
        document.body.classList.add('dark-mode')
        document.getElementById('btn-theme').innerHTML = icodark
    }
}

pageStartTheme()