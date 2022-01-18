$(document).ready(function() {
 
    $('.dismiss, .overlay').on('click', function() {
        $('.sidebar').removeClass('active');
        $('.overlay').removeClass('active');
        $('.line').removeClass('open');
    });
 
    $('.open-menu').on('click', function(e) {
        e.preventDefault();
        $('.sidebar').addClass('active');
        $('.overlay').addClass('active');
        $('.line').toggleClass('open');
        // close opened sub-menus
        $('.collapse.show').toggleClass('show');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
 
    /* other code */
 
});
