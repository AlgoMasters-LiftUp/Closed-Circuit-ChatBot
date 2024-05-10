var x = document.getElementById("Login");
var z = document.getElementById("Register");
var y = document.getElementById("btn");

function register() {
    x.style.left = "-400px";
    z.style.left = "50px";
    y.style.left = "110px";
}

function login() {
    x.style.left = "50px";
    z.style.left = "450px";
    y.style.left = "0px";
}
document.addEventListener("DOMContentLoaded", function () {
    var settingsBtn = document.querySelector(".settings-btn");
    var aboutMeSection = document.querySelector(".about-me");
    var changePasswordScreen = document.querySelector(".change-password-screen");

    settingsBtn.addEventListener("click", function (event) {
        event.preventDefault();
        aboutMeSection.style.display = "none";
        changePasswordScreen.style.display = "block";
    });
});

