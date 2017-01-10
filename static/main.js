// --------------------------------------------------------------------------
// -----Generate and set a cookie, so we know who has been here before.------

function randomString(length) {
    return Math.round((Math.pow(36, length + 1) - Math.random() *
    Math.pow(36, length))).toString(36).slice(1);
};

function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        var expires = "; expires=" + date.toUTCString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
};

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
};

function eraseCookie(name) {
    createCookie(name,"",-1);
};

// Set a cookie if there isn't already one set:
if (readCookie('smartrEmailVisit')){}
else { createCookie('smartrEmailVisit', randomString(20), 365); };


// --------------------------------------------------------------------------
// --------------Make page content and links work.---------------------------
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
