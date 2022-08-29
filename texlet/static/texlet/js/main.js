$(document).ready(function() {
    // magnification housekeeping
    $('img').magnify();

    // texapp minor flashy form functionality
    $('.card').on('click', function(event) {
        $('.card').removeClass('active');
        $(this).addClass('active');
    });
    $('.form-check-label').on('click', function(event) {
        $('.card').removeClass('active');
    });

});
    