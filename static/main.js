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

// Google analytics tracking:
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-90021344-1', 'auto');
ga('send', 'pageview');
