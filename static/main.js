$(document).ready(function() {
    $('.mobile-menu-button').on('click', function(event) {
        event.preventDefault();
        $('.main-nav').animate({ height: 'toggle' });
    });
    $('.data-policy-button').on('click', function(event) {
        event.preventDefault();
        $('.home-content, .tools-content, .contact-content').hide();
        $('.data-policy-content').show();
    });
    $('.tools-button').on('click', function(event) {
        event.preventDefault();
        $('.home-content, .data-policy-content, .contact-content').hide();
        $('.tools-content').show();
    });
    $('.contact-button').on('click', function(event) {
        event.preventDefault();
        $('.home-content, .tools-content, .data-policy-content').hide();
        $('.contact-content').show();
    });
    $('.home-button').on('click', function(event) {
        event.preventDefault();
        $('.data-policy-content, .tools-content, .contact-content').hide();
        $('.home-content').show();
    });
});
