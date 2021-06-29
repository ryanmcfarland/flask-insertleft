/*
Relies on the validators.js file to help validate and print errors for contact forms
*/

$(document).ready(function() {
    $("#submitButton").click(function() {
        if(!validateText("name", "Please provide a name.")) {
            return false;
        };
        if(!validateEmail("email", "Please provide a proper email.")) {
            return false;
        };
        if(!validateTextArea("message", "Please provide a message")) {
            return false;
        };
        if(!validateCaptcha("g-recaptcha", "Please validate the recaptcha")) {
            return false;
        };
        $("form#contact").submit();
    }
)})