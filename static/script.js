document.addEventListener("DOMContentLoaded", function () {

    var submitBtn = document.getElementById("submit");
    var inputBox = document.getElementById("url-input");

    // Make "shorten" button work
    submitBtn.addEventListener("click", function (event) {
        // get input url
        toShorten = inputBox.value;
        // submit url to API
        var xhr = new XMLHttpRequest();
        xhr.onload = function (e) {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log(xhr.responseText);
                    // redirect to info-page about the returned key
                    onUrlShortened(JSON.parse(xhr.responseText));
                } else {
                    console.error(xhr.statusText);
                }
            }
        };
        xhr.onerror = function (e) {
            console.error(xhr.statusText);
        };
        xhr.open("POST", "/api/urls", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ "url": toShorten }));
    });
});

// changes the site after shortening an url
function onUrlShortened(response) {
    window.location.assign("/urls/" + response["key"]);
}