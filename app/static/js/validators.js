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

function validateCaptcha(id, err){
    if($("#g-recaptcha-response").val()==null || $("#g-recaptcha-response").val()==""){
        var div = $("#"+id).closest("div");
        $("#feedback"+id).remove();
        div.after('<div id="feedback'+id+'" class="text-danger"><small>'+err+'</small></div>');
        return false;
    } else {
        var div = $("#"+id).closest("div");
        $("#feedback"+id).remove();
        div.after('<div id="feedback'+id+'" class="text-success"><small>Looks good!</small></div>');
        return true;
    };
};

function validateTextArea(id, err){
    if($("#"+id).val()==null || $("#"+id).val()==""){
        var input = $("#"+id).closest("textarea");
        input.removeClass("is-valid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-invalid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-remove form-control-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="invalid-feedback">'+err+'</div>');
        return false;
    } else {
        var input = $("#"+id).closest("textarea");
        input.removeClass("is-invalid");
        $("#glypcn"+id).remove();
        $("#feedback"+id).remove();
        input.addClass("is-valid has-feedback");
        input.append('<span id="glypcn'+id+'" class="glyphicon glyphicon-ok invalid-feedback"></span>');
        input.after('<div id="feedback'+id+'" class="valid-feedback">Looks good!</div>');
        return true;
    };
};