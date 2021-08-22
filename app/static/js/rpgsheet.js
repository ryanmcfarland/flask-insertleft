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
    console.log(pad);
    console.log(HeightNote);
    console.log(HeightMain);
    console.log(HeightMain*0.5);
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

$(document).ready(function() {    
    cssHeight()
})

$(window).resize(function() {
    cssHeight();
});