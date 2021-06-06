/*
Copied from: https://www.codeply.com/go/bp/UPsVWHA9yX
jquery functions to append bootstrap validation classes 
and append / delete validation html elements
*/
function validateText(id, err){
    if($("#"+id).val()==null || $("#"+id).val()==""){
        var input = $("#"+id).closest("input");
        input.removeClass("is-valid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-invalid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-remove form-control-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="invalid-feedback">'+err+'</div>');
        return false;
    } else {
        var input = $("#"+id).closest("input");
        input.removeClass("is-invalid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-valid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-ok invalid-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="valid-feedback">Looks good!</div>');
        return true;
    };
};

function validateEmail(id, err){
  var email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
    if(!email_regex.test($("#"+id).val())){
        var input = $("#"+id).closest("input");
        input.removeClass("is-valid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-invalid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-remove form-control-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="invalid-feedback">'+err+'</div>');
        return false; 
    } else{
        var input = $("#"+id).closest("input");
        input.removeClass("is-invalid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-valid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-ok invalid-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="valid-feedback">Looks good!</div>');
        return true;
    };
};

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
        $("form#register").submit();
    }
)})