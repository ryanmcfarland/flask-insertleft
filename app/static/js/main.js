$(document).ready(function() {
    $('.dismiss, .overlay, .ham-btn').on('click', function() {
        $('.sidebar').toggleClass('active');
        $('.overlay').toggleClass('active');
        $('.line').toggleClass('open');
        $('.collapse.show').toggleClass('show');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
 
});
