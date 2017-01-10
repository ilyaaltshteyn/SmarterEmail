$(document).ready(function() {
    $('.mobile-menu-button').on('click', function(event) {
        event.preventDefault();
        $('.main-nav').animate({ height: 'toggle' });
    });
    $('.data-policy-button').on('click', function(event) {
        event.preventDefault();
        $('.data-policy-button').css({'color':'rgba(249,93,95,1)'})
        $('.tools-button, .contact-button, .home-button').css({'color':'black'})
        $('.home-content, .tools-content, .contact-content').hide();
        $('.data-policy-content').show();
    });
    $('.tools-button').on('click', function(event) {
        event.preventDefault();
        $('.tools-button').css({'color':'rgba(249,93,95,1)'})
        $('.data-policy-button, .contact-button, .home-button').css({'color':'black'})
        $('.home-content, .data-policy-content, .contact-content').hide();
        $('.tools-content').show();
    });
    $('.contact-button').on('click', function(event) {
        event.preventDefault();
        $('.contact-button').css({'color':'rgba(249,93,95,1)'})
        $('.tools-button, .data-policy-button, .home-button').css({'color':'black'})
        $('.home-content, .tools-content, .data-policy-content').hide();
        $('.contact-content').show();
    });
    $('.home-button').on('click', function(event) {
        event.preventDefault();
        $('.home-button').css({'color':'rgba(249,93,95,1)'})
        $('.tools-button, .contact-button, .data-policy-button').css({'color':'black'})
        $('.data-policy-content, .tools-content, .contact-content').hide();
        $('.home-content').show();
    });
});
