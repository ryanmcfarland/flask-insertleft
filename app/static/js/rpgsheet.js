/*
Function with create variable cssHeight for the weapon and aditonal note section
if each section is too large, we create a dyanmic way to create an overflow bar in
each section
-> uses jquery to grab height of css objects within the sheet
*/

function cssHeight(){
    var HeightMain = ($("#r-att").height())+($("#r-ski").height())-($("#r-stat").height());
    var pad = ($("#r-att").height())-($("#cd-att").height());
    var HeightWeap = $("#r-weap").height();
    var HeightNote = $("#r-note").height();
    var dynaHeight = HeightMain * 0.5;
    if (dynaHeight < HeightWeap ) {
        HeightWeap = dynaHeight-pad-($("#ch-weap").outerHeight());
        $("#cb-weap").css("height", HeightWeap);
    } else {
        dynaHeight = HeightMain-HeightWeap;
    };

    if (dynaHeight < HeightNote ) {
        HeightNote = dynaHeight-pad-($("#ch-note").outerHeight());
        $("#cb-note").css("height", HeightNote);
    };
};

function updateModifiers(){
    let attributes = [ "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    attributes.forEach(function (e){
        updateModifier(e)
    })
}

function updateModifier(fieldName){
    var field = $("div[name='modifier-"+fieldName+"']");
    var currentVal = (parseInt($("input[name='"+fieldName+"']").val())) | (parseInt($("td[name='"+fieldName+"']").text()));
    var currentVal = updateAttrMods(currentVal);
    field.text(currentVal[0]);
    field.attr('style','color: '+currentVal[1])
}

function updateAttrMods(attr){
    if (attr < 4) { 
        return ['-2', '#EB1010'];
    } else if (attr < 8 ) {
        return ['-1', '#EB1010'];
    } else if (attr < 14) {
        return ['0',  'white'];
    } else if (attr < 18) {
        return ['+1', '#26EB10'];
    } else {
        return ['+2', '#26EB10'];
    }
};

function updateAttackBonus(){
    if (typeof sheet === 'undefined') { 
        var chr_class = $('#character_class').val();
    } else {
        var chr_class = $('#character_class').text();
    }
    var level = ($("input[name='level']").val()) | (parseInt($("td[id='level']").text()));
    if ('Brain' == chr_class) {
        $("input[name='attack_bonus']").val(Math.floor(level/2)).change()
    } else {
        $("input[name='attack_bonus']").val(level).change()
    };
};

$(document).ready(function() {    
    cssHeight()
    updateModifiers()
    updateAttackBonus()
});

$(window).resize(function() {
    cssHeight();
});

// -> https://bootsnipp.com/snippets/dGWP
// -> http://jsfiddle.net/0uy57p5z/

//plugin bootstrap minus and plus
//http://jsfiddle.net/laelitenetwork/puJ6G/
$('.btn-number').click(function(e){
    e.preventDefault();
    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {
            
            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            } 
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    };
    if (fieldName = 'level') { updateAttackBonus() }
    else { updateModifier(fieldName)};
});

$('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});

$('.input-number').change(function() {
    minValue =  parseInt($(this).attr('min')) || 0;
    maxValue =  parseInt($(this).attr('max')) || 20000;
    valueCurrent = parseInt($(this).val());
    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    updateModifier(name)
});

$(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

$('#character_class').change(function (){
    updateAttackBonus()});

$("input[name='level']").change(function (){
    updateAttackBonus()});
