/*
Relies on the validators.js file to help validate and print errors for contact forms
*/

$(document).ready(function() {
    $("#submitButton").click(function() {
        if(!validateText("username", "Please provide a username.")) {
            return false;
        };
        if(!validateEmail("email", "Please provide a proper email.")) {
            return false;
        };
        if(!validateText("password", "Please input a password")) {
            return false;
        };
        if(!validateText("password2", "Please input a password")) {
            return false;
        };
        if(!validateCaptcha("g-recaptcha", "Please validate the recaptcha")) {
            return false;
        };
        $("form#register").submit();
    }
)})