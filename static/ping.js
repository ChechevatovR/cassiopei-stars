function ping_me(url) {
    console.log(url)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.send();
}